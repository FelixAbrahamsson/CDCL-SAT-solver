from DataStructures import SATInstance
import os

# cur_dir = os.path.abspath(os.path.join("./", os.pardir)+'/CDCL-SAT-solver')
# filepath = cur_dir+'/Benchmarks/SAT09/RANDOM/MEDIUM/3SAT/SATISFIABLE/360/unif-k3-r4.25-v360-c1530-S144043535-002.cnf'
filepath = 'example-3sat.cnf'

sat = SATInstance()
sat.readInstanceFromFile(filepath)

# Print all the clauses in which literal 1 is watched
for cl in sat.watchlist[1]:
  for lit in cl.literals:
    print(str(lit.sign*lit.var), end=' ')
  print('')
