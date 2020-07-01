import sys
import copy
import random
import time

def parsing_file(filename):
    file = open(filename, 'r')
    f = []
    k = 1
    for l in file:
        if l[0] == 'c':
            continue
        elif l[0] == 'p':
            p = l.split(" ")
            while '' in p:
                p.remove('')
            var = int(p[2])
            clause = int(p[3])
        elif l[0] == '0' or l[0] == '%' or l[0] == '\n':
            continue
        else:
            l1 = l.split(" ")
            f1 = []
            for i in l1:
                if i != '' and i != '\n':
                    if int(i) != 0:
                        f1.append(int(i))
            f1.append(str(k))
            f.append(f1)
            k += 1
    return f, var, clause

def resolution(A, B):
    C = []
    del B[-1]
    for i in range(len(A)):
        for j in range(len(B)):
            if A[i] == -B[j]:
                A.remove(A[i])
                B.remove(B[j])
                for k in range(len(B)):
                    if B[k] not in A:
                        A.append(B[k])
                return A
    for i in range(len(B)):
        if B[i] not in A:
            A.append(B[i])
    return A

def learning_procedure(A, k, formula):
    D = formula[k-1][:]
    del D[-1]
    for i in range(len(A)):
        i1 = -i-1
        b = True
        for j in D:
            for m in A:
                if j in m or -j in m:
                    if m[1] == 'i':
                        b = False
                        break
            if b == False:
                break
        if b == True:
            return D
        if A[i1][1] == 'd' or (A[i1][0] not in D and -A[i1][0] not in D):
            continue
        elif A[i1][1] == 'i':
            n = A[i1][2]
            D1 = resolution(D, formula[int(n)-1][:])
            D = D1[:]
            if len(D) == 0:
                return D
    return D

def backtrack(C, formula, A):
    B = []
    y = C[-1]
    del C[-1]
    x = 0
    for i in range(len(A)):
        i1 = -i-1
        if -A[i1][0] in C:
            x = -A[i1][0]
            break
    for i in range(len(A)):
        if A[i][0] == -x:
            B.append([x, 'i', y])
            break
        B.append([A[i][0], A[i][1], A[i][2]])
    return B

def DPLL2(formula, F, A, di):
    if di == True:
        x = A[-1][0]
        F1 = F[:]
        for i in F1:
            if x in i:
                F.remove(i)
            elif -x in i:
                F[F.index(i)].remove(-x)
    if len(F) == 0:
        B = copy.deepcopy(A)
        return [True, B]
    for i in F:
        if len(i) == 2:
            k = i[0]
            A.append([k, 'i', i[1]])
            F2 = F[:]
            for j in F2:
                if k in j:
                    F.remove(j)
                elif -k in j:
                    F[F.index(j)].remove(-k)
            return DPLL2(formula, F, A, False)
    for i in F:
        if len(i) == 1:
            C = learning_procedure(A, int(i[0]), formula[:])
            if len(C) == 0:
                return ["unsat", []]
            else:
                C.append(str(int(formula[-1][-1])+1))
                formula.append(C)
                F.append(C)
                A = backtrack(C[:], formula[:], A)
                return [False, len(A), A[-1]]
    x1 = random.randint(0, len(F)-1)
    x = F[x1][0]
    A.append([x, 'd', F[x1][-1]])
    k = len(A)
    #FF = copy.deepcopy(F)
    b = DPLL2(formula, F, A, True)
    if b[0] == "unsat":
        return b
    elif b[0] == False:
        if b[1] == k:
            A = A[:k-1]
            A.append(b[2][:])
            AA = []
            for i in A:
                AA.append(i[0]) 
            F5 = []
            for i in formula:
                bbb = False
                F6 = i[:]
                for j in range(len(i)-1):
                    if i[j] in AA:
                        bbb = True
                        break
                    elif -i[j] in AA:
                        F6.remove(i[j])
                if bbb == False:
                    F5.append(F6)
            return DPLL2(formula, F5, A, True)
        else:
            return b
    return b

filename = sys.argv[1]
f, var, clause = parsing_file(filename)

A = []
s = ""
f2 = copy.deepcopy(f)
b = DPLL2(f2, f, A, False)

if b[0] == False:
    s = "s UNSATISFIABLE"
elif b[0] == "unsat":
    s = "s UNSATISFIABLE"
else: 
    s = "s SATISFIABLE\n"
    s += "v "
    for j in b[1]:
        s += str(j[0])
        s += " "
    s += "0"
print(s)

