import numpy as np
from sympy import*

k,T1,T2,A,L,h,Ts,Tair = symbols("k T1 T2 A L h Ts Tair")

def Convection(h,A,Tair,Ts):
    return h*A*(Ts - Tair)

def Conduction(k,Th,TL,A,L):
    return k*(Th-TL)*A/L

def Gause_seidel(A,b):

    ITERATION_LIMIT = 1000
    print("System of equations:") 
    for i in range(A.shape[0]):     
        row = ["{0:3g}*x{1}".format(A[i, j], j + 1) for j in range(A.shape[1])]     
        print("[{0}] = [{1:3g}]".format(" + ".join(row), b[i]))
        x = np.zeros_like(b) 

    for it_count in range(1, ITERATION_LIMIT):     
        x_new = np.zeros_like(x)     
        print("Iteration {0}: {1}".format(it_count, x))   
        
        for i in range(A.shape[0]):         
            s1 = np.dot(A[i, :i], x_new[:i])         
            s2 = np.dot(A[i, i + 1:], x[i + 1:])         
            x_new[i] = (b[i] - s1 - s2) / A[i, i]   
                
        if np.allclose(x, x_new, rtol=1e-8):         
            break     

        x = x_new 

    print("Solution: {0}".format(x)) 
    error = np.dot(A, x) - b 
    print("Error: {0}".format(error))