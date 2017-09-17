import sys
import logging
import random
import argparse
import re
from multiprocessing import Pool, TimeoutError
import time

RESULT_FILE = open('result.txt','w')

## Added code:
# Solver.check_pure_literal()
# Solver.assign_pure_literal
# Solver.precompute_jw()
# Solver.check_for_conflicts()
# Solver.jw_heuristic()
# Solver.dlis_heuristic()

## Modified code
# Solver._solve()
# Solver.__init__()


if __debug__:
    logging.basicConfig(level=logging.WARNING)


class Solver(object):
    """
    Solver object
    """
    def __init__(self):
        self.varlist = VarList()
        self.clause_list = []
        self.learnt_list = []

        self.level = 0
        self.root_level = 0

        # key -> level, value -> literal list
        self.propagate_history = {}
        self.decide_history = {}
        self.previous_assignments = {} # key -> level, value -> {(variable,sign) -> True}

        # True  -> satisfied
        # False -> unsatisfied
        # None  -> running
        self.status = None

        self.conflict_count = 0
        self.decide_count = 0

        # sign when variable chosen to branch on (only affects 'order' and 'random' selection heuristics).
        self.ASSIGN_DEFAULT = True
        self.choose_type = "random"

        # J function for the Jeroslow-Wang heuristic
        # represented as a dictionary from l = (variable id, sign) to J(l)
        self.jw = {}

        # True/False determines whether to print the solution after solving
        self.print_solution = False

        # Integer, determines how often pure literal rule should be applied
        # If None, it's never applied
        self.PL_interval = 5
        self.PL_interval_counter = 1

        # Determines how often unit propagation is applied
        # If None, it's never applied
        self.UP_interval = 1
        self.UP_interval_counter = 1

        # Restart settings
        self.use_random_restart = True
        self.restart_interval = 1000 # after this many conflicts a restart will be performed
        self._restarts = 0 # amount of restarts performed so far

        # If a learnt clause exceeds this length it will not be retained
        # Determines amount of CDCL to be used
        self.max_learnt_clause_length = 1000


    def precompute_jw(self):
        for var in self.varlist:
            var_id = var.get_id()
            self.jw[(var_id, False)] = 0.0
            self.jw[(var_id,  True)] = 0.0
        for c in self.clause_list+self.learnt_list:
            length = len(c)
            for lit in c.lit_list:
                key = (lit.var.get_id(), lit.get_raw_sign())
                self.jw[key] = self.jw[key] + 2**(-length)

    def solve(self):
        """start solving
        try solving while unsat or sat
        return sat or unsat as solver.status
        """
        if self.choose_type == "jw" :
            self.precompute_jw()
        logging.debug("solve")
        logging.info(str(self))
        while self.is_running():
            self._solve()


    def _solve(self):
        """main solving function"""

        while True:

            ## Keep previous_assignments updated with an empty dictionary
            if self.level not in self.previous_assignments:
                self.previous_assignments[self.level] = {}

            ## Start by applying unit propagation
            if self.UP_interval != None and self.UP_interval == self.UP_interval_counter:
                ## Apply unit propagation
                conflict_clause = self.propagate()
                self.UP_interval_counter = 1
            else:
                ## No UP, must still check for conflicts
                conflict_clause = self.check_for_conflicts()
                self.UP_interval_counter += 1

            if isinstance(conflict_clause, Clause):
                self.conflict_count += 1
                if self.level == self.root_level:
                    ## CONTRADICTION
                    self.status = False
                    return

                if (self.use_random_restart and self.conflict_count >= 
                        (self._restarts + 1) * self.restart_interval):
                    ## Restart from 0 if too many backjumps have been performed
                    backjump_level = self.root_level
                    save_result(self)
                    self._restarts += 1
                    print("Restarting search from decision level "+str(backjump_level))
                else:
                    ## Backjump to the conflict
                    backjump_level, learnt_clause = self.analyze(conflict_clause)
                    if (len(learnt_clause) <= self.max_learnt_clause_length):
                        ## Only add clause if it does not exceed max length
                        self.add_clause(learnt_clause)
                self.cancel_until(backjump_level)
                self.level = backjump_level

            else:
                ## No conflict, or no UP applied
                ## Try to apply the pure literal rule
                found_PL = False
                if self.PL_interval != None:
                    if self.PL_interval == self.PL_interval_counter:
                        # Apply pure literal rule
                        found_PL = self.check_pure_literal()
                        self.PL_interval_counter = 1
                    else:
                        self.PL_interval_counter += 1
                if found_PL:
                    continue
                else:
                    ## Pure literal rule inapplicable, decide a variable via heuristic
                    self.decide_count += 1

                    (next_var, sign) = self.popup_variable()
                    if next_var is None:
                        unassigned_variables = [x for x in self.varlist if x.is_unassigned()]
                        if len(unassigned_variables) == 0:
                            ## ALL ASSIGNED, SATISFIED
                            self.status = True
                            return
                        else:
                            ## Tried everything at this level, backjump 1 level
                            backjump_level = self.level-1
                            self.cancel_until(backjump_level)
                            self.level = backjump_level
                    else:
                        self.decide(next_var, sign)


    def check_for_conflicts(self):
        for c in self.clause_list+self.learnt_list:
            tmp = c.reload_watching_literal()
            if tmp is False:
                return c
        return None

    def propagate(self):
        """propagate clause, reloading watching literal
        Returns:
            Clause or None
            Clause : Conflicting Clause
            None   : No conflicting, propagated successfully
        """
        while True:
            propagatable_list = []
            # reloading watching ltieral
            for c in self.clause_list+self.learnt_list:
                tmp = c.reload_watching_literal()
                if tmp is True:
                    continue
                elif isinstance(tmp, Lit):
                    propagatable_list.append((tmp,c))
                elif tmp is False:
                    return c

            if len(propagatable_list) == 0:
                return None

            #propagate variables
            for bvar, reason in propagatable_list:

                sign = bvar.get_raw_sign()
                bvar.var.assign(sign,self.level,reason)

                if self.level != 0:
                    self.propagate_history[self.level].append(bvar)

    def check_pure_literal(self):
        """ 
        Tries to find a pure literal, if one is found the variable
        is assigned the value that satisfies the clauses
        Returns:
            True if a pure literal was found
            False otherwise
        """

        ## variable_counts is a map from variable id to a 2x1 array
        ## First element in the array is a count over nr of occurances
        ## of the negated literal in clauses, second element is a count
        ## over occurances of the positive literal in clauses
        ## This can be made more efficient by not recreating the objects
        ## every time the function is executed, but I think the 
        ## improvement would be negligible
        variable_counts = {}
        for var in self.varlist:
            # Indexed by id
            if var.is_unassigned():
                var_id = var.get_id()
                variable_counts[var_id] = [0,0]

        for c in self.clause_list+self.learnt_list:

            ## Check if clause is not already satisfied:
            clause_satisfied = False
            for bvar in c.lit_list:
                var = bvar.var
                if not var.is_unassigned():
                    if var.get_sign() == bvar._sign:
                        ## Vareral is True ==> clause satisfied
                        clause_satisfied = True
                        break

            if not clause_satisfied:
                for bvar in c.lit_list:
                    ## Clause is not satisfied yet, go through every unassigned 
                    ## variable in the clause and add it to the counter
                    if bvar.var.is_unassigned():
                        var_id = bvar.var.get_id()
                        if bvar._sign == False:
                            # Negated variable
                            variable_counts[var_id][0] = variable_counts[var_id][0] + 1
                        else:
                            variable_counts[var_id][1] = variable_counts[var_id][1] + 1

        ## Now check if any of the variables are pure
        found_pure_literal = False
        for key in variable_counts:
            count = variable_counts[key]
            var = self.varlist.get(key)
            if (var,True) not in self.previous_assignments[self.level] and (
                    count[0] == 0 and count[1] != 0):
                ## Strictly positive variable, assign it True
                self.assign_pure_literal(var, True)
                found_pure_literal = True
            elif (var,False) not in self.previous_assignments[self.level] and (
                    count[1] == 0 and count[0] != 0):
                ## Strictly negative variable, assignedn it False
                self.assign_pure_literal(var, False)
                found_pure_literal = True

        return found_pure_literal

    def assign_pure_literal(self, var, sign):

        ## Remember this assignment before incrementing level
        if self.level not in self.previous_assignments:
            self.previous_assignments[self.level] = {}

        self.previous_assignments[self.level][(var,sign)] = True

        self.level += 1
        self.previous_assignments[self.level] = {}

        var.assign(sign, self.level)
        self.decide_history[self.level] = var
        self.propagate_history[self.level] = []
        logging.debug('pure_literal: %s'%var)
        logging.debug(str(self))


    def analyze(self, conflict_clause):
        """analyze conflicting clause
        Arguments:
            conflict_clause(Clause): conflicting clause
        Returns:
            (backjump_level, learnt_clause)
            backjump_level(int)  : backjump level
            learnt_clause(clause) : learnt clause by analyzing conflicting clause
        """

        # implication graph in the level
        VAR_HISTORY = [self.decide_history[self.level]]+[x.var for x in self.propagate_history[self.level]]
        def _pop_next_pointer(bvar_set):
            # pop latest variable on implication graph from bvar_set
            #
            # Arguments:
            #   bvar_set(set) : Var set
            # Returns:
            #   (next_variable, bind_variable_list)
            #   next_variable(Var) : latest variable on implication graph
            #   bind_variable_list(list) : other bind variables
            data = [x.var for x in bvar_set]
            for var in reversed(VAR_HISTORY):
                if var in data:
                    others = [x for x in bvar_set if var is not x.var]
                    return var, others
            assert False, "not reachable"

        logging.debug(self)
        logging.debug("analyze %s"%str(conflict_clause))
        logging.debug("level %d %s"%(self.level, self.decide_history[self.level]))
        logging.debug("propagate_history lv.%d: %s"%(self.level,', '.join([str(x)for x in self.propagate_history[self.level]])))

        lower_level_bvar = set()
        current_level_bvar = set()
        done_var = set()
        pool_bvar = [x for x in conflict_clause.get_lit_list()]

        while True:
            #SEPARATING
            for bvar in pool_bvar:
                assert bvar.var.get_level() <= self.level, "future level is reachable"
                if bvar.var.get_level() == self.level:
                    current_level_bvar.add(bvar)
                else:
                    lower_level_bvar.add(bvar)

            # if you need simplify bvar list, write here.
            logging.debug('done: '+', '.join([str(x.id) for x in done_var]))
            logging.debug('pool: '+', '.join([str(x) for x in pool_bvar]))
            logging.debug('lower: '+', '.join([str(x) for x in lower_level_bvar]))
            logging.debug('current: '+', '.join([str(x) for x in current_level_bvar]))
            assert len(current_level_bvar) >= 1, "arienai"
            if len(current_level_bvar) == 1:
                # find UIP
                break

            head_var, tail_bvar = _pop_next_pointer(current_level_bvar)

            done_var.add(head_var)
            pool_bvar = set([x for x in head_var.get_reason().get_lit_list()if x.var not in done_var])
            current_level_bvar = set(tail_bvar)

        learnt_list = [x.var for x in list(current_level_bvar) + list(lower_level_bvar)]
        if lower_level_bvar:
            backjump_level = max([x.var.get_level()for x in lower_level_bvar])
        else:
            backjump_level = self.level-1
        learnt_clause = self._gen_learnt_clause(learnt_list)
        return backjump_level, learnt_clause

    def _gen_learnt_clause(self, var_list):
        """generate learnt clause from variable list.
        Arguments:
            var_list(list) : variable list, it will convert to learnt clause
        Returns:
            learnt_clause(Clause)
        """
        bvar_list = []
        for var in var_list:
            sign = var.get_sign()
            assert isinstance(sign, bool), 'unassigned is arienai %s'%sign
            bvar_list.append(var.get_bind_var(not sign))
        return Clause(bvar_list, is_learnt=True)

    def cancel_until(self, backjump_level):
        """rollback to backjump_level
        Arguments:
            backjump_level(int) : rollback to the backjump level
        """
        keys = list(self.decide_history.keys())
        for key in keys:
            if key > backjump_level:
                del self.propagate_history[key]
        for key in keys:
            if key > backjump_level:
                del self.decide_history[key]
        for var in self.varlist:
            if not var.is_unassigned() and (var.get_level() > backjump_level):
                var.set_default()
        keys = list(self.previous_assignments)
        for key in keys:
            if key > backjump_level+1:
                del self.previous_assignments[key]

    def decide(self, decide_variable, sign):
        """decide variable as ASSIGN_DEFAULT
        Arguments:
            decide_variable(Var)
        """
        assert isinstance(decide_variable, Var)

        ## Remember this assignment before incrementing level
        if self.level not in self.previous_assignments:
            self.previous_assignments[self.level] = {}

        self.previous_assignments[self.level][(decide_variable,sign)] = True

        self.level += 1
        if sign == None:
            sign = self.ASSIGN_DEFAULT
        decide_variable.assign(sign, self.level)
        self.decide_history[self.level] = decide_variable
        self.propagate_history[self.level] = []
        logging.debug('decide: %s'%decide_variable)
        logging.debug(str(self))

    def add_clause(self, clause):
        """add clause to solver
        if one variable clause is given,
            assign variable without adding solver's clause list.
        if learnt clause is given, add learnt clause list.
        Arguments:
            clause(Clause)
        """
        assert isinstance(clause, Clause)
        if len(clause) == 1:
            bvar = clause.get_lit_list()[0]
            sign = bvar.get_raw_sign()
            bvar.var.assign(sign, self.root_level)
            return
        clause.set_watching_literal((0,1))
        if clause.is_learnt():
            self.learnt_list.append(clause)
        else:
            self.clause_list.append(clause)

    def popup_variable(self):
        """select next variable and possibly its sign from unassigned variable.
        """

        if self.choose_type == 'random':
            # random
            l = [x for x in self.varlist if x.is_unassigned()]
            if len(l) == 0:
                return (None, None)
            else:
                i = random.randint(0,len(l)-1)
                return (l[i], None)
        elif self.choose_type == 'order':
            # order
            for var in self.varlist:
                if var.is_unassigned():
                    return (var, None)
            return (None, None)
        elif self.choose_type == 'jw':
            return self.jw_heuristic()
        elif self.choose_type == 'dlis':
            return self.dlis_heuristic()
            
    def jw_heuristic(self):
        best = float("-inf")
        best_var = (None, None)
        for var in self.varlist:
            if var.is_unassigned():
                for sign in [False, True]:
                    score = self.jw[(var.get_id(),sign)]
                    if score > best and (var,sign) not in self.previous_assignments[self.level]:
                        best = score
                        best_var = (var, sign)
        return best_var

    def dlis_heuristic(self):
        ## Keep a count for each variable+sign how many new clauses
        ## an assignment would satisfy
        variable_counts = {}
        for var in self.varlist:
            # Indexed by id
            if (var.is_unassigned()):
                var_id = var.get_id()
                variable_counts[var_id] = [0,0]

        for c in self.clause_list+self.learnt_list:

            ## Check if clause is not already satisfied:
            clause_satisfied = False
            for bvar in c.lit_list:
                var = bvar.var
                if not var.is_unassigned():
                    if var.get_sign() == bvar._sign:
                        ## Vareral is True ==> clause satisfied
                        clause_satisfied = True
                        break

            if not clause_satisfied:
                for bvar in c.lit_list:
                    ## Clause is not satisfied yet, go through every unassigned 
                    ## variable in the clause and add it to the counter
                    if bvar.var.is_unassigned():
                        var_id = bvar.var.get_id()
                        if bvar._sign == False:
                            # Negated variable
                            variable_counts[var_id][0] = variable_counts[var_id][0] + 1
                        else:
                            variable_counts[var_id][1] = variable_counts[var_id][1] + 1
        ## Find the variable + assignment with largest nr of satisfiable clauses
        max_clauses = 0
        best_var = (None, None)
        for key in variable_counts:
            var = self.varlist.get(key)
            if (var,False) not in self.previous_assignments[self.level] and (
                variable_counts[key][0] > max_clauses):

                best_var = (var, False)
                max_clauses = variable_counts[key][0]
            if (var,True) not in self.previous_assignments[self.level] and (
                variable_counts[key][1] > max_clauses):

                best_var = (var, True)
                max_clauses = variable_counts[key][1]

        if best_var[0] != None:
            return best_var
        else:
            # Instance already satisfied, just assign arbitrarily
            for key in variable_counts:
                return (self.varlist.get(key), True)
            # No variables left, return None
            return best_var


    def print_result(self):
        """print satisfied or unsatisfied"""
        if self.status is True:
            print("")
            print("#############")
            print("#satisfied!!#")
            print("#############")
            print("")
        elif self.status is False:
            print("")
            print("-------------")
            print("-Unsatisfied-")
            print("-------------")
            print("")

    def is_running(self):
        return self.status is None

    def is_sat(self):
        return self.status is True

    def _str_history(self):
        string = ""
        for key in sorted(self.propagate_history.keys()):
            line = self.propagate_history[key]
            var = self.decide_history[key]
            string += 'lv.%03d '%key
            string += '% 7d: '%var.get_id()
            string += ', '.join([str(x)for x in line])
            string += '\n'
        return string

    def __str__(self):
        string = "###############level:%d root_level:%d\n"%(self.level, self.root_level)
        string += "####Varerals\n"+"\n".join([str(x)for x in self.varlist])
        string += "\n\n"
        string += "####Clauses\n"+"\n".join([str(x)for x in self.clause_list])
        string += "\n\n"
        string += "####Learnts\n"+"\n".join([str(x)for x in self.learnt_list])
        string += "\n\n"
        string += "####Tree\n"
        string += self._str_history()
        return string


class Var(object):
    """Variable Object
    Attributes:
        id(id): unique id
        lits(dict): the variable's bind variable, key is True or False
        sign(None or bool): variable's sign
            None -- unassigned
            True -- assigned True
            False -- assigned False
        level(int): level when assigned
        reason(None or Clause): if the variable is propagated, the reason clause
    """
    def __init__(self, id):
        """initialize variable
        Arguments:
            id: variable unique id
        """
        self.id = id
        self.lits = self._gen_lit()
        self.set_default()

    def assign(self, sign, level, reason=None):
        """assign variable
        if propagated, set reason
        Arguments:
            sign(bool): variable sign
            level(int): decide or propagated level
            reason(Clause):(optical)if propagated, the reason clause
        """
        assert isinstance(sign, bool)
        assert isinstance(level, int)
        assert reason is None or isinstance(reason, Clause)
        self.sign = sign
        self.level = level
        self.reason = reason

    def set_default(self):
        """reset to default attribute
        """
        self.sign = None
        self.level = None
        self.reason = None

    def get_sign(self):
        return self.sign

    def get_bind_var(self, sign):
        assert isinstance(sign, bool)
        return self.lits[sign]

    def get_id(self):
        return self.id

    def get_reason(self):
        return self.reason

    def get_level(self):
        return self.level

    def is_unassigned(self):
        return self.sign is None

    def _gen_lit(self):
        res = {}
        res[True] = Lit(self, True)
        res[False] = Lit(self, False)
        return res

    def __str__(self):
        return "{var:10d}:{level}-{sign}{propagated}".format(
            var=self.get_id(),
            sign="unassigned" if self.sign is None else self.sign,
            propagated= "-propagated"+str(self.reason.id) if self.get_reason()else "",
            level=self.level
        )



class VarList(object):
    """variable list
    this object is one-index list.
    so you can use variable.id and cnf number as index, when you generate this as expected.
    """
    def __init__(self):
        self.data = []
        pass
    def get(self, id):
        """get variable from list
        Arguments:
            id(int): variable id, don't mind positive or negative
        Returns:
            Var
        """
        assert isinstance(id, int)
        idx = abs(id)
        assert idx >= 1
        if len(self.data) < idx:
            self._gen_var(idx)
        return self.data[idx-1]

    def get_bind_var(self, id):
        """get bound variable from list
        Arguments:
            id(int): variable id. if negative, returns False bind_var.
        Returns:
            Var
        """
        var = self.get(id)
        if id < 0:
            return var.get_bind_var(False)
        else:
            return var.get_bind_var(True)

    def _gen_var(self, num):
        while len(self.data) < num:
            next_id = len(self.data)+1 # for 1-index
            self.data.append(Var(next_id))

    def __iter__(self):
        return iter(self.data)


class Clause(object):
    """Clause Object
    Attributes:
        id(int): unique id
        lit_list(list): component bind variables
        _is_learnt(bool)
        watching_literal(tuple or None):
            None -- not initialized
            tuple(int, int) -- lit_list's index
    """
    _num = 0
    # self.id : int
    # self.learnt : bool

    def __init__(self, lit_list, is_learnt=False):
        assert isinstance(is_learnt, bool)
        self.id = self._gen_id()
        self.lit_list = sorted(lit_list,key=lambda y:y.var.get_id())
        self._is_learnt = is_learnt
        self.watching_literal = None
        pass

    def reload_watching_literal(self):
        """reload watching variable
        Returns:
            bool or Var
            Var -- propagatable variable
            True    -- the clause is satisfied or unassigned
            False   -- conflict
        """
        res = self._check_watching_literal()
        for i, idx in enumerate(res):
            if idx is None:
                for new_idx, bvar in enumerate(self.lit_list):
                    if (bvar.get_sign() is not False) and (new_idx not in res):
                        res[i] = new_idx
        assert len(res) == 2
        c = res.count(None)
        if c == 0:
            #ok
            self.set_watching_literal(tuple(res))
            return True
        elif c == 1:
            #propagatable
            idx = [x for x in res if x is not None][0]
            propagatable_bvar = self.lit_list[idx]
            if propagatable_bvar.get_sign() is None:
                # UNASSIGNED
                return propagatable_bvar
            else:
                # ASSIGNED TRUE
                return True
        elif c == 2:
            #conflict
            return False
        assert False, "not reachable"

    def set_watching_literal(self, wl):
        """
        Arguments:
            wl(tuple): (int, int) -- watching literal indexes
        """
        assert isinstance(wl, tuple)
        assert None not in wl, str(wl)
        assert len(wl) == 2, str(wl)
        assert all([isinstance(x,int)for x in wl]), str(wl)
        self.watching_literal = wl

    def get_lit_list(self):
        return self.lit_list

    def is_learnt(self):
        return self._is_learnt is True

    def _check_watching_literal(self):
        """check watching literal
        Returns:
            [int or None, int or None]
            int -- the literal index
            None -- the literal is assigned False, so the variable need reload
        """
        return [None if self.lit_list[x].get_sign() is False else x for x in self.watching_literal]

    @classmethod
    def _gen_id(cls):
        cls._num += 1
        return cls._num

    def __len__(self):
        return len(self.lit_list)

    def __str__(self):
        return "{id:3d} :{watching}:{learnt}: {vars}".format(
            id=self.id,
            watching=self.watching_literal,
            vars=", ".join([str(x)for x in self.lit_list]),
            learnt="l"if self._is_learnt else "-"
        )


class Lit(object):
    """bind variable and sign for clause
    Attributes:
        var(Var)
        _sign(bool)
    """
    def __init__(self, var, sign):
        self.var = var
        self._sign = sign

    def get_sign(self):
        """return lit's sign and the variable's sign
        Returns:
            bool
        """
        s = self.var.get_sign()
        if s is None:
            return None
        elif self._sign:
            return s
        else:
            return not s

    def get_raw_sign(self):
        """return the lit's sign
        Returns:
            bool
        """
        return self._sign

    def __str__(self):
        if self._sign:
            return " %2d"%self.var.get_id()
        else:
            return "-%2d"%self.var.get_id()


def parse(string):
    """parse string as CNF file
    Returns:
        Solver
    """
    solver = Solver()
    def parse_clause(inp):
        """parse cnf line to clause
        Arguments:
            inp(str)
        Returns:
            Clause
        """
        s = set()
        for x in inp.split(' '):
            if x == '':
                continue
            elif x == '0':
                break

            try:
                num = int(x)
            except ValueError:
                continue

            s.add(num)
        if len(s) == 0:
            return
        bll = [solver.varlist.get_bind_var(x)for x in s]
        return Clause(bll)
    pat = re.compile('\A[^pc]+')
    for line in string.splitlines():
        c_result = pat.search(line)
        if c_result is None:
            continue
        clause = parse_clause(c_result.group())
        if clause:
            solver.add_clause(clause)
    return solver

def save_result(solver):
    """save solver status as RESULT_FILE
    Arguments:
        solver(Solver)
    """
    string = str(solver)
    if RESULT_FILE:
        RESULT_FILE.write(string)

def argument_parse():
    parser = argparse.ArgumentParser(description="Sat Solver on Python")
    parser.add_argument('file',
                        type=open,
                        help='Filename of formula in CNF'
                        )
    parser.add_argument('--choose-type',
                        choices=['random','order','jw','dlis'],
                        help='The variable selection heuristic. (default "random")',
                        default='random'
                        )
    parser.add_argument('--assign-default',
                        type=bool,
                        help='The default truth value to assign to a variable when branching. Only affects "random" and "order" heuristics. (default True)',
                        default=True
                        )
    parser.add_argument('--PL-interval',
                        type=int,
                        help='How often to apply pure literal: 0 for never, 1 for always, k >= 1 for every kth level. (default 1)',
                        default=1
                        )
    parser.add_argument('--UP-interval',
                        type=int,
                        help='How often to apply unit propagation: 0 for never, 1 for always, k >= 1 for every kth level. (default 1)',
                        default=1
                        )
    parser.add_argument('--restart-interval',
                        type=int,
                        help='How many conflicts before a random restart is applied: 0 for no random restarts. (default 1000)',
                        default=1000,
                        )
    parser.add_argument('--max-learnt-clause-length',
                        type=int,
                        help='The maximum length of learnt clauses. This is used to vary the amount of CDCL applied. (default 1000)',
                        default=1000,
                        )
    parser.add_argument('--time-out',
                        type=int,
                        help='Time-out in seconds. (default 300)',
                        default=300,
                        )
    parser.add_argument('--result-path',
                        type=open,
                        help='Filepath to output solution. (optional)',
                        default=None,
                        )
    return parser.parse_args()

def solve(solver):
    solver.solve()
    if solver.print_solution:
        print(solver)
    solver.print_result()
    save_result(solver)
    
if __name__ == '__main__':
    arguments = argument_parse()
    string = arguments.file.read()
    solver = parse(string)

    solver.ASSIGN_DEFAULT = arguments.assign_default
    solver.choose_type = arguments.choose_type
    solver.PL_interal  = None if arguments.PL_interval == 0 else arguments.PL_interval
    solver.UP_interval = None if arguments.UP_interval == 0 else arguments.UP_interval
    solver.restart_interval = arguments.restart_interval
    solver.use_random_restart = (solver.restart_interval > 0)
    solver.max_learnt_clause_length = arguments.max_learnt_clause_length
    RESULT_FILE = arguments.result_path

    pool = Pool(1)
    res = pool.apply_async(solve, (solver,))
    try:
        res.get(timeout=arguments.time_out)
        sys.exit(0)
    except TimeoutError:
        print("Timed out!")
        sys.exit(1)
