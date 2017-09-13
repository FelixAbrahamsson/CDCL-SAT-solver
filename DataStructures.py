class SATInstance():
  def __init__(self):
    self.clauses = []
    self.watchlist = {} # variable idx : clause
    self.variables = []
    self.n_vars = 0 # nr of variables
    self.n_clauses = 0 # nr of clauses

  def readInstanceFromFile(self, filename):
    ## Expects a .cnf file that may start with comments, then
    ## followed by a line starting with 'p', then followed by
    ## lines of integers where each line represents a clause, 
    ## each clause delimited by the integer 0
    data = open(filename, 'r')
    # Read all comment lines
    while True:
      line = data.readline().split() # split on whitespace
      if line[0] != 'c':
        break
    if line[0] != 'p':
      print ('ERROR: Incorrect format, missing descriptive p line.')
      return

    try:
      self.n_vars = int(line[2])
      self.n_clauses = int(line[3])

      ## Create all variables
      for i in range(1,self.n_vars+1): ## Numbered 1->n_vars
        self.variables.append(Variable(i))
        self.watchlist[i] = [] ## Create empty watchlist for each variable

      ## Create all the clauses and the watchlist
      for line in data:
        literals = line.split()
        literals = [int(x) for x in literals] ## Convert to int
        clause = Clause()
        ## Loop over every literal except last one which is expected to
        ## be a delimiter
        for i in range(len(literals)-1):
          val = literals[i]
          sign = (1,-1)[val<0]
          literal = Literal(abs(val), sign)
          clause.addLiteral(literal) # add literal to clause

        self.clauses.append(clause) # add clause to clauses

        ## Make the first two literals watched (arbitrary selection)
        self.watchlist[abs(literals[0])].append(clause)
        if len(literals) > 2: 
          ## Expected to always happen, but just in case
          self.watchlist[abs(literals[1])].append(clause)

    except ValueError:
      print ('ERROR: Incorrect format.')

  def satisfied(self):
    # TODO: checks if the SAT instance is satisfied
    # Returns: True/False
    pass

class Clause():
  def __init__(self):
    self.literals = []

  def addLiteral(self, l):
    self.literals.append(l)

class Literal():
  def __init__(self, var, sign):
    self.var = var # Integer, references a variable
    self.sign = sign # sign of the literal, -1 or 1

class Variable():
  def __init__(self, idx):
    self.idx = idx # Index of this variable
    self.assigned = False
    self.value = None # -1 or 1