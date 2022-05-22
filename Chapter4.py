import numpy as np
from sympy import*

A,r1,r2,L,k,D,d,w,z,D1,D2,W,h = symbols("A r1 r2 L,k D d w z D1 D2 W h")

def Thermal_resistance(shape, A = 1 , r1 = 1, r2 = 1 , L = 1 , k = 1 ):

    if shape == 'cylinder' :

        return(np.log(r2/r1)/(2*np.pi*L*k))

    elif shape == 'planewall':

        return L/k/A


def Shape_factor(case , D = 1 , d =1 , L = 1 , w  = 1 , z = 0 , D1 = 1, D2 = 1, W = 1):

    '''
    shape factor for chapter 4
    all variables are based on Incropera Heat transfer

    Table 4.1
    '''

    if case == 1:
        return 2*np.pi*D/(1-D/4/z)

    elif case ==2:
        return 2*np.pi*L/(np.arccosh(2*z/D))

    elif case ==3:
        return 2*np.pi*L/np.log(4*L/D)

    elif case ==4:
        return 2*np.pi*L/np.arccosh((4*w**2-D1**2-D2**2)/(2*D1*D2))

    elif case ==5:
        return 2*np.pi*L/np.log(8*z/np.pi/D)

    elif case ==6:
        return 2*np.pi*L/np.log(1.08*w/D)      

    elif case == 7:
        return 2*np.pi*L/np.arccosh((D**2+d**2 -4*z**2)/(2*D*d))

    elif case == 8:
        return 20.54*D

    elif case == 9:
        return 0.15*L

    elif case == 10:
        return 2*D

    elif case == 11:
        if W/w < 1.4:
            return 2*np.pi*L/(0.785*np.log(W/w))
        else:
            return 2*np.pi*L/(0.93*np.log(W/w)-0.05)
    else:
        print("case 값이 잘못 되었습니다. " )


def Thermal_resistance_shapefacetor(k, S = 1, case = 0 , D = 1 , d = 1 , L = 1 , w  = 1 , z = 0 , D1 = 1, D2 = 1, W = 1 ):

    '''
    get Thermal_resistance_shape factor by Shape_factor function
    or just put in shpae factor this function 
    

    all variables are based on Incropera Heat transfer
    '''

    if case == 0:
           return 1/k/S

    else:
        shape_factor = Shape_factor(case , D = 1 , d =1 , L = 1 , w  = 1 , z = 0 , D1 = 1, D2 = 1, W = 1)
        return 1/k/shape_factor


def Critical_insulation_radius(k,h):

    return k/h


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