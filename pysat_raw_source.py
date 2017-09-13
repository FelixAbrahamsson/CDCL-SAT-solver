#!/usr/bin/python -OO
## This is the raw source code for pysat, from
## https://github.com/cocuh/pysat

'''
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

"License" shall mean the terms and conditions for use, reproduction,
and distribution as defined by Sections 1 through 9 of this document.

"Licensor" shall mean the copyright owner or entity authorized by
the copyright owner that is granting the License.

"Legal Entity" shall mean the union of the acting entity and all
other entities that control, are controlled by, or are under common
control with that entity. For the purposes of this definition,
"control" means (i) the power, direct or indirect, to cause the
direction or management of such entity, whether by contract or
otherwise, or (ii) ownership of fifty percent (50%) or more of the
outstanding shares, or (iii) beneficial ownership of such entity.

"You" (or "Your") shall mean an individual or Legal Entity
exercising permissions granted by this License.

"Source" form shall mean the preferred form for making modifications,
including but not limited to software source code, documentation
source, and configuration files.

"Object" form shall mean any form resulting from mechanical
transformation or translation of a Source form, including but
not limited to compiled object code, generated documentation,
and conversions to other media types.

"Work" shall mean the work of authorship, whether in Source or
Object form, made available under the License, as indicated by a
copyright notice that is included in or attached to the work
(an example is provided in the Appendix below).

"Derivative Works" shall mean any work, whether in Source or Object
form, that is based on (or derived from) the Work and for which the
editorial revisions, annotations, elaborations, or other modifications
represent, as a whole, an original work of authorship. For the purposes
of this License, Derivative Works shall not include works that remain
separable from, or merely link (or bind by name) to the interfaces of,
the Work and Derivative Works thereof.

"Contribution" shall mean any work of authorship, including
the original version of the Work and any modifications or additions
to that Work or Derivative Works thereof, that is intentionally
submitted to Licensor for inclusion in the Work by the copyright owner
or by an individual or Legal Entity authorized to submit on behalf of
the copyright owner. For the purposes of this definition, "submitted"
means any form of electronic, verbal, or written communication sent
to the Licensor or its representatives, including but not limited to
communication on electronic mailing lists, source code control systems,
and issue tracking systems that are managed by, or on behalf of, the
Licensor for the purpose of discussing and improving the Work, but
excluding communication that is conspicuously marked or otherwise
designated in writing by the copyright owner as "Not a Contribution."

"Contributor" shall mean Licensor and any individual or Legal Entity
on behalf of whom a Contribution has been received by Licensor and
subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
this License, each Contributor hereby grants to You a perpetual,
worldwide, non-exclusive, no-charge, royalty-free, irrevocable
copyright license to reproduce, prepare Derivative Works of,
publicly display, publicly perform, sublicense, and distribute the
Work and such Derivative Works in Source or Object form.

3. Grant of Patent License. Subject to the terms and conditions of
this License, each Contributor hereby grants to You a perpetual,
worldwide, non-exclusive, no-charge, royalty-free, irrevocable
(except as stated in this section) patent license to make, have made,
use, offer to sell, sell, import, and otherwise transfer the Work,
where such license applies only to those patent claims licensable
by such Contributor that are necessarily infringed by their
Contribution(s) alone or by combination of their Contribution(s)
with the Work to which such Contribution(s) was submitted. If You
institute patent litigation against any entity (including a
cross-claim or counterclaim in a lawsuit) alleging that the Work
or a Contribution incorporated within the Work constitutes direct
or contributory patent infringement, then any patent licenses
granted to You under this License for that Work shall terminate
as of the date such litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the
Work or Derivative Works thereof in any medium, with or without
modifications, and in Source or Object form, provided that You
meet the following conditions:

(a) You must give any other recipients of the Work or
Derivative Works a copy of this License; and

(b) You must cause any modified files to carry prominent notices
stating that You changed the files; and

(c) You must retain, in the Source form of any Derivative Works
that You distribute, all copyright, patent, trademark, and
attribution notices from the Source form of the Work,
excluding those notices that do not pertain to any part of
the Derivative Works; and

(d) If the Work includes a "NOTICE" text file as part of its
distribution, then any Derivative Works that You distribute must
include a readable copy of the attribution notices contained
within such NOTICE file, excluding those notices that do not
pertain to any part of the Derivative Works, in at least one
of the following places: within a NOTICE text file distributed
as part of the Derivative Works; within the Source form or
documentation, if provided along with the Derivative Works; or,
within a display generated by the Derivative Works, if and
wherever such third-party notices normally appear. The contents
of the NOTICE file are for informational purposes only and
do not modify the License. You may add Your own attribution
notices within Derivative Works that You distribute, alongside
or as an addendum to the NOTICE text from the Work, provided
that such additional attribution notices cannot be construed
as modifying the License.

You may add Your own copyright statement to Your modifications and
may provide additional or different license terms and conditions
for use, reproduction, or distribution of Your modifications, or
for any such Derivative Works as a whole, provided Your use,
reproduction, and distribution of the Work otherwise complies with
the conditions stated in this License.

5. Submission of Contributions. Unless You explicitly state otherwise,
any Contribution intentionally submitted for inclusion in the Work
by You to the Licensor shall be under the terms and conditions of
this License, without any additional terms or conditions.
Notwithstanding the above, nothing herein shall supersede or modify
the terms of any separate license agreement you may have executed
with Licensor regarding such Contributions.

6. Trademarks. This License does not grant permission to use the trade
names, trademarks, service marks, or product names of the Licensor,
except as required for reasonable and customary use in describing the
origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or
agreed to in writing, Licensor provides the Work (and each
Contributor provides its Contributions) on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied, including, without limitation, any warranties or conditions
of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
PARTICULAR PURPOSE. You are solely responsible for determining the
appropriateness of using or redistributing the Work and assume any
risks associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory,
whether in tort (including negligence), contract, or otherwise,
unless required by applicable law (such as deliberate and grossly
negligent acts) or agreed to in writing, shall any Contributor be
liable to You for damages, including any direct, indirect, special,
incidental, or consequential damages of any character arising as a
result of this License or out of the use or inability to use the
Work (including but not limited to damages for loss of goodwill,
work stoppage, computer failure or malfunction, or any and all
other commercial damages or losses), even if such Contributor
has been advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing
the Work or Derivative Works thereof, You may choose to offer,
and charge a fee for, acceptance of support, warranty, indemnity,
or other liability obligations and/or rights consistent with this
License. However, in accepting such obligations, You may act only
on Your own behalf and on Your sole responsibility, not on behalf
of any other Contributor, and only if You agree to indemnify,
defend, and hold each Contributor harmless for any liability
incurred by, or claims asserted against, such Contributor by reason
of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

Copyright 2017 cocuh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
"""
Python Sat Solver
To use simply, $ {this} {cnf file}
or $ python -OO {cnf file}
If possible, you should use pypy.
"""
import logging
import random
import argparse
import re

RESULT_FILE = None

if __debug__:
    logging.basicConfig(level=logging.DEBUG)


class Solver(object):
    """
    Solver object
    """
    def __init__(self):
        self.litlist = LitList()
        self.clause_list = []
        self.learnt_list = []

        self.level = 0
        self.root_level = 0

        # key -> level, value -> literal list
        self.propagate_history = {}
        self.decide_history = {}

        # True  -> satisfied
        # False -> unsatisfied
        # None  -> running
        self.status = None

        self.conflict_count = 0
        self.decide_count = 0

        # sign when literal decided.
        self.ASSIGN_DEFAULT = True
        self.pickup_type = "random"

    def solve(self):
        """start solving
        try solving while unsat or sat
        return sat or unsat as solver.status
        """
        logging.debug("solve")
        logging.info(str(self))
        while self.is_running():
            self._solve()

    def _solve(self):
        """main solving function"""
        while True:
            conflict_clause = self.propagate()
            if isinstance(conflict_clause, Clause):
                self.conflict_count += 1
                if self.level == self.root_level:
                    # CONTRADICTION
                    self.status = False
                    return
                backjump_level, learnt_clause = self.analyze(conflict_clause)
                self.add_clause(learnt_clause)
                self.cancel_until(backjump_level)
                self.level = backjump_level
            else:
                self.decide_count += 1

                # restart here
                if self.decide_count % 1000 == 0:
                    save_result(self)

                # NO CONFLICT
                next_lit = self.popup_literal()
                if next_lit is None:
                    # ALL ASSIGNED, SATISFIED
                    self.status = True
                    return
                else:
                    self.decide(next_lit)

        pass

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
                elif isinstance(tmp, BindLit):
                    propagatable_list.append((tmp,c))
                elif tmp is False:
                    return c

            if len(propagatable_list) == 0:
                return None

            #propagate literals
            for blit, reason in propagatable_list:
                sign = blit.get_raw_sign()
                blit.lit.assign(sign,self.level,reason)
                if self.level != 0:
                    self.propagate_history[self.level].append(blit)

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
        LIT_HISTORY = [self.decide_history[self.level]]+[x.lit for x in self.propagate_history[self.level]]
        def _pop_next_pointer(blit_set):
            # pop latest literal on implication graph from blit_set
            #
            # Arguments:
            #   blit_set(set) : BindLit set
            # Returns:
            #   (next_literal, bind_literal_list)
            #   next_literal(Lit) : latest literal on implication graph
            #   bind_literal_list(list) : other bind literals
            data = [x.lit for x in blit_set]
            for lit in reversed(LIT_HISTORY):
                if lit in data:
                    others = [x for x in blit_set if lit is not x.lit]
                    return lit, others
            assert False, "not reachable"

        logging.debug(self)
        logging.debug("analyze %s"%str(conflict_clause))
        logging.debug("level %d %s"%(self.level, self.decide_history[self.level]))
        logging.debug("propagate_history lv.%d: %s"%(self.level,', '.join([str(x)for x in self.propagate_history[self.level]])))

        lower_level_blit = set()
        current_level_blit = set()
        done_lit = set()
        pool_blit = [x for x in conflict_clause.get_bindlit_list()]

        while True:
            #SEPARATING
            for blit in pool_blit:
                assert blit.lit.get_level() <= self.level, "future level is reachable"
                if blit.lit.get_level() == self.level:
                    current_level_blit.add(blit)
                else:
                    lower_level_blit.add(blit)

            # if you need simplify blit list, write here.

            logging.debug('done: '+', '.join([str(x.id) for x in done_lit]))
            logging.debug('pool: '+', '.join([str(x) for x in pool_blit]))
            logging.debug('lower: '+', '.join([str(x) for x in lower_level_blit]))
            logging.debug('current: '+', '.join([str(x) for x in current_level_blit]))
            assert len(current_level_blit) >= 1, "arienai"
            if len(current_level_blit) == 1:
                # find UIP
                break

            head_lit, tail_blit = _pop_next_pointer(current_level_blit)

            done_lit.add(head_lit)
            pool_blit = set([x for x in head_lit.get_reason().get_bindlit_list()if x.lit not in done_lit])
            current_level_blit = set(tail_blit)

        learnt_list = [x.lit for x in list(current_level_blit) + list(lower_level_blit)]
        if lower_level_blit:
            backjump_level = max([x.lit.get_level()for x in lower_level_blit])
        else:
            backjump_level = self.level-1
        learnt_clause = self._gen_learnt_clause(learnt_list)
        return backjump_level, learnt_clause

    def _gen_learnt_clause(self, lit_list):
        """generate learnt clause from literal list.
        Arguments:
            lit_list(list) : literal list, it will convert to learnt clause
        Returns:
            learnt_clause(Clause)
        """
        blit_list = []
        for lit in lit_list:
            sign = lit.get_sign()
            assert isinstance(sign, bool), 'unassigned is arienai %s'%sign
            blit_list.append(lit.get_bind_lit(not sign))
        return Clause(blit_list, is_learnt=True)

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
        for lit in self.litlist:
            if not lit.is_unassigned() and (lit.get_level() > backjump_level):
                lit.set_default()

    def decide(self, decide_literal):
        """decide literal as ASSIGN_DEFAULT
        Arguments:
            decide_literal(Lit)
        """
        assert isinstance(decide_literal, Lit)
        self.level += 1
        decide_literal.assign(self.ASSIGN_DEFAULT, self.level)
        self.decide_history[self.level] = decide_literal
        self.propagate_history[self.level] = []
        logging.debug('decide: %s'%decide_literal)
        logging.debug(str(self))

    def add_clause(self, clause):
        """add clause to solver
        if one literal clause is given,
            assign literal without adding solver's clause list.
        if learnt clause is given, add learnt clause list.
        Arguments:
            clause(Clause)
        """
        assert isinstance(clause, Clause)
        if len(clause) == 1:
            blit = clause.get_bindlit_list()[0]
            sign = blit.get_raw_sign()
            blit.lit.assign(sign, self.root_level)
            return
        clause.set_watching_literal((0,1))
        if clause.is_learnt():
            self.learnt_list.append(clause)
        else:
            self.clause_list.append(clause)

    def popup_literal(self):
        """select next decide literal from unassigned literal.
        """

        if self.pickup_type == 'random':
            # random
            l = [x for x in self.litlist if x.is_unassigned()]
            if len(l) == 0:
                return None
            else:
                i = random.randint(0,len(l)-1)
                return l[i]
        else:
            # order
            for lit in self.litlist:
                if lit.is_unassigned():
                    return lit
            return None

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
            lit = self.decide_history[key]
            string += 'lv.%03d '%key
            string += '% 7d: '%lit.get_id()
            string += ', '.join([str(x)for x in line])
            string += '\n'
        return string

    def __str__(self):
        string = "###############level:%d root_level:%d\n"%(self.level, self.root_level)
        string += "####Literals\n"+"\n".join([str(x)for x in self.litlist])
        string += "\n\n"
        string += "####Clauses\n"+"\n".join([str(x)for x in self.clause_list])
        string += "\n\n"
        string += "####Learnts\n"+"\n".join([str(x)for x in self.learnt_list])
        string += "\n\n"
        string += "####Tree\n"
        string += self._str_history()
        return string


class Lit(object):
    """Literal Object
    Attributes:
        id(id): unique id
        bindlits(dict): the literal's bind literal, key is True or False
        sign(None or bool): literal's sign
            None -- unassigned
            True -- assigned True
            False -- assigned False
        level(int): level when assigned
        reason(None or Clause): if the literal is propagated, the reason clause
    """
    def __init__(self, id):
        """initialize literal
        Arguments:
            id: literal unique id
        """
        self.id = id
        self.bindlits = self._gen_bindlit()
        self.set_default()

    def assign(self, sign, level, reason=None):
        """assign literal
        if propagated, set reason
        Arguments:
            sign(bool): literal sign
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

    def get_bind_lit(self, sign):
        assert isinstance(sign, bool)
        return self.bindlits[sign]

    def get_id(self):
        return self.id

    def get_reason(self):
        return self.reason

    def get_level(self):
        return self.level

    def is_unassigned(self):
        return self.sign is None

    def _gen_bindlit(self):
        res = {}
        res[True] = BindLit(self, True)
        res[False] = BindLit(self, False)
        return res

    def __str__(self):
        return "{var:10d}:{level}-{sign}{propagated}".format(
            var=self.get_id(),
            sign="unassigned" if self.sign is None else self.sign,
            propagated= "-propagated"+str(self.reason.id) if self.get_reason()else "",
            level=self.level
        )



class LitList(object):
    """literal list
    this object is one-index list.
    so you can use literal.id and cnf number as index, when you generate this as expected.
    """
    def __init__(self):
        self.data = []
        pass
    def get(self, id):
        """get literal from list
        Arguments:
            id(int): literal id, don't mind positive or negative
        Returns:
            Lit
        """
        assert isinstance(id, int)
        idx = abs(id)
        assert idx >= 1
        if len(self.data) < idx:
            self._gen_lit(idx)
        return self.data[idx-1]

    def get_bind_lit(self, id):
        """get binded literal from list
        Arguments:
            id(int): literal id. if negative, returns False bind_lit.
        Returns:
            BindLit
        """
        lit = self.get(id)
        if id < 0:
            return lit.get_bind_lit(False)
        else:
            return lit.get_bind_lit(True)

    def _gen_lit(self, num):
        while len(self.data) < num:
            next_id = len(self.data)+1 # for 1-index
            self.data.append(Lit(next_id))

    def __iter__(self):
        return iter(self.data)


class Clause(object):
    """Clause Object
    Attributes:
        id(int): unique id
        bindlit_list(list): component bind literals
        _is_learnt(bool)
        watching_literal(tuble or None):
            None -- not initialized
            tuple(int, int) -- bindlit_list's index
    """
    _num = 0
    # self.id : int
    # self.learnt : bool

    def __init__(self, bindlit_list, is_learnt=False):
        assert isinstance(is_learnt, bool)
        self.id = self._gen_id()
        self.bindlit_list = sorted(bindlit_list,key=lambda y:y.lit.get_id())
        self._is_learnt = is_learnt
        self.watching_literal = None
        pass

    def reload_watching_literal(self):
        """reload watching literal
        Returns:
            bool or BindLit
            BindLit -- propagatable literal
            True    -- the clause is satisfied or unassigned
            False   -- conflict
        """
        res = self._check_watching_literal()
        for i, idx in enumerate(res):
            if idx is None:
                for new_idx, blit in enumerate(self.bindlit_list):
                    if (blit.get_sign() is not False) and (new_idx not in res):
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
            propagatable_blit = self.bindlit_list[idx]
            if propagatable_blit.get_sign() is None:
                # UNASSIGNED
                return propagatable_blit
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

    def get_bindlit_list(self):
        return self.bindlit_list

    def is_learnt(self):
        return self._is_learnt is True

    def _check_watching_literal(self):
        """check watching literal
        Returns:
            [int or None, int or None]
            int -- the literal index
            None -- the literal is assigned False, so the literal need reload
        """
        return [None if self.bindlit_list[x].get_sign()is False else x for x in self.watching_literal]

    @classmethod
    def _gen_id(cls):
        cls._num += 1
        return cls._num

    def __len__(self):
        return len(self.bindlit_list)

    def __str__(self):
        return "{id:3d} :{watching}:{learnt}: {lits}".format(
            id=self.id,
            watching=self.watching_literal,
            lits=", ".join([str(x)for x in self.bindlit_list]),
            learnt="l"if self._is_learnt else "-"
        )


class BindLit(object):
    """bind literal and sign for clause
    Attributes:
        lit(Lit)
        _sign(bool)
    """
    def __init__(self, lit, sign):
        self.lit = lit
        self._sign = sign

    def get_sign(self):
        """return bindlit's sign and the literal's sign
        Returns:
            bool
        """
        s = self.lit.get_sign()
        if s is None:
            return None
        elif self._sign:
            return s
        else:
            return not s

    def get_raw_sign(self):
        """return the bindlit's sign
        Returns:
            bool
        """
        return self._sign

    def __str__(self):
        if self._sign:
            return " %2d"%self.lit.get_id()
        else:
            return "-%2d"%self.lit.get_id()


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
        bll = [solver.litlist.get_bind_lit(x)for x in s]
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
                        help='cnf file name',
                        )
    parser.add_argument('--choose-type',
                        choices=['random','order'],
                        help='how decide literal choose',
                        default='random',
                        )
    parser.add_argument('--assign-default',
                        type=bool,
                        help='default decide',
                        default=True
                        )
    parser.add_argument('--result-path',
                        type=open,
                        help='ouptput result path',
                        default=None,
                        )
    return parser.parse_args()

if __name__ == '__main__':
    arguments = argument_parse()
    string = arguments.file.read()
    solver = parse(string)

    solver.ASSIGN_DEFAULT = arguments.assign_default
    solver.choose_type = arguments.choose_type
    RESULT_FILE = arguments.result_path

    solver.solve()
    print(solver)

    solver.print_result()
    save_result(solver)