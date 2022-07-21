from tkinter import Variable
from pysat.formula import CNF
from pysat.solvers import Solver
from time import time

def un_prop(formula):
    global varList
    ul = [0]*len(varList)
    for clause in formula:
        if(len(clause) == 1):
            ul[abs(clause[0]) - 1] = 1 if clause[0] > 0 else -1
            varList[abs(clause[0]) -1] = clause[0]
    f = []
    for clause in formula:
        x = []
        flag = True
        for i in clause:
            if(not(ul[abs(i) - 1])):
                x.append(i)
            else:
                if(i*ul[abs(i) - 1] > 0):
                    flag = False
                    break
        if flag:
            f.append(x)
    return f

def lit_elem(formula):
    global varList
    n = len(varList)
    pos = [0]*n
    neg = [0]*n
    for clause in formula:
        for x in clause:
            if(x > 0):
                pos[x-1] += 1
            else:
                neg[-x-1] += 1
    f = []
    for clause in formula:
        x = []
        flag = True
        for i in clause:
            if pos[abs(i) - 1]*neg[abs(i) -1] != 0:
                x.append(i)
            else:
                varList[abs(i) - 1] = i
                flag = False
                break
        if flag:
            f.append(x)
    
    return f
        
    

def solve(formula):
    formula = un_prop(formula)
    if [] in formula:
        return False
    formula = lit_elem(formula)
    if len(formula) == 0:
        return True
    x = formula[0][0]
    if(solve([[x]] + formula)):
        return True
    else:
        return solve([[-x]] + formula)

url = "test2.cnf"
file = CNF(from_file=url)

formula = file.clauses
N = file.nv
varList = [0]*N
del file

s = Solver()
s.append_formula(formula)
t1 = time()
if(s.solve()):
    print(s.get_model())
else:
    print("Unsat")
t2 = time()
print(t2-t1)

t1 = time()
check = solve(formula)
if(check):
    print("Satisfiable")
    print([x for x in varList if x != 0])
else:
    print("Unsatisfiable")
t2 = time()
print(t2-t1)