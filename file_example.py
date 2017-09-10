from satispy import Variable, Cnf
from satispy.solver import Minisat
from satispy.io import DimacsCnf

with open("example.dimacs", "r") as satfile:
    s = satfile.read().rstrip("\n")
    exp = DimacsCnf().fromstring(s)

print (exp)

solver = Minisat()
solution = solver.solve(exp)

if solution.success:
    print ("Found a solution:") 
    for v in solution.varmap:
        print (v.name + ": " + str(solution[v]))
else:
    print ("The expression cannot be satisfied")
