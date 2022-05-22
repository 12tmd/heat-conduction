# -*- coding: utf-8 -*-

import numpy as np
from sympy import *

pi = np.pi

def One_dimensional_steady_state_solutions(shape = 0 , L = symbols('L') , T1 = symbols('T1') , T2 = symbols('T2'), qdot = symbols('qdot')
        , k = symbols('k') , r1 = symbols('r1') , r2 =symbols('r2') , x = symbols('x') , r = symbols('r') , A = symbols('A')) :

    """
    Table C.1 
    One dimensional steady state solutions to the Heat Equation for 
    plane, cylinder and spherical walls with uniform generation and 
    asymmetrical surface conditions
    """

    def plane_temperature(x, L, T1, T2, qdot, k):
        d1 = qdot*L**2/(2*k)
        d2 = 1 - (x/L)**2
        d3 = (T2 - T1)/2
        d4 = (T2 + T1)/2
        T = d1*d2 + d3*x/L + d4
        return T

    def plane_heatflux(x, L, T1, T2, qdot, k):
        qf = qdot*x - k/(2*L)*(T2 - T1)
        return qf

    def cylinder_temperature(r, r1, r2, T1, T2, qdot, k):
        d1 = qdot*r2**2/(4*k)
        d2 = 1 - (r/r2)**2
        d3 = 1 - (r1/r2)**2
        d4 = np.log(r2/r)/np.log(r2/r1)
        T = T2 + d1*d2 - (d1*d3 + (T2-T1))*d4    
        return T

    def cylinder_heatflux(r, r1, r2, T1, T2, qdot, k):
        d1 = qdot*r/2
        d2 = qdot*r2**2/(4*k)
        d3 = 1 - (r1/r2)**2
        d4 = r*np.log(r2/r1)
        qf = d1 - k*(d2*d3 + (T2-T1))/d4
        return qf

    def sphere_temperature(r, r1, r2, T1, T2, qdot, k):
        d1 = qdot*r2**2/(6*k)
        d2 = (1/r -1/r2)/(1/r1 - 1/r2)
        d3 = 1 - (r1/r2)**2
        T = T2 + d1*(1-(r/r2)**2) - (d1*d3 + (T2-T1))*d2    
        return T

    def sphere_heatflux(r, r1, r2, T1, T2, qdot, k):
        d1 = qdot*r2**2/(6*k)
        d3 = 1 - (r1/r2)**2
        qf = qdot*r/3 - k*(d1*d3 + (T2-T1))/(r**2*(1/r1 - 1/r2))
        return qf
        
    if shape == 'plane':

        print('T(x) = ' , plane_temperature(x,L,T1,T2,qdot,k))
        print('q''  = ' , plane_heatflux(x, L, T1, T2, qdot, k))
        print('q    = ' , A*plane_heatflux(x, L, T1, T2, qdot, k))

        return (plane_temperature(x,L,T1,T2,qdot,k) , plane_heatflux(x, L, T1, T2, qdot, k) , A*plane_heatflux(x, L, T1, T2, qdot, k))

    elif shape == 'cylinder':

        print('T(x) = ' ,cylinder_temperature(r, r1, r2, T1, T2, qdot, k))
        print('q''  = ' ,cylinder_heatflux(r, r1, r2, T1, T2, qdot, k))
        print('q    = ' ,2*pi*r2*L*cylinder_heatflux(r, r1, r2, T1, T2, qdot, k))


        return (cylinder_temperature(r, r1, r2, T1, T2, qdot, k) ,cylinder_heatflux(r, r1, r2, T1, T2, qdot, k) , 2*pi*r2*L*cylinder_heatflux(r, r1, r2, T1, T2, qdot, k))

    elif shape == 'sphere':

        print('T(x) = ' ,sphere_temperature(r, r1, r2, T1, T2, qdot, k))
        print('q''  = ' ,sphere_heatflux(r, r1, r2, T1, T2, qdot, k))
        print('q    = ' ,4*pi*r2**2*sphere_heatflux(r, r1, r2, T1, T2, qdot, k))

        return (sphere_temperature(r, r1, r2, T1, T2, qdot, k) , sphere_heatflux(r, r1, r2, T1, T2, qdot, k) , 4*pi*r2**2*sphere_heatflux(r, r1, r2, T1, T2, qdot, k))

    elif shape == 0:
        print("please enter shape among , plane , cylinder , sphere")


def One_dimensional_steady_state_One_Adiabatic_Surface_uniform_heatgeneration_solutions(shape = 0 , L = symbols('L') , Ts = symbols('Ts') , qdot = symbols('qdot')
        , k = symbols('k') , r1 = symbols('r1') , ro =symbols('ro') , x = symbols('x') , r = symbols('r') , A = symbols('A')) :

    """
    Table C.3
    One-Dimensional, Steady-State solutions to the heat equation for 
    Uniform Generation in a Plane Wall with One Adiabatic Surface, 
    a Solid Cylinder, and a Solid Sphere 
    """

    def plane_temp(x, L, qdot, k, Ts): # C.22
        return qdot*L**2/(2*k)*(1-(x/L)**2) + Ts

    def plane_heatflux(qdot, x):
        return qdot*x

    def cylinder_temp(r, ro, qdot, k, Ts): # C.23
        return qdot*ro**2/(4*k)*(1-(r/r)**2) + Ts

    def cylinder_heatflux(qdot, r):
        return qdot*r/2

    def sphere_temp(r, ro, qdot, k, Ts): # C.24
        return qdot*ro**2/(6*k)*(1-(r/ro)**2) + Ts

    def sphere_heatflux(qdot, r):
        return qdot*r/3

    if shape == 'plane':

        print('T(x) = ' , plane_temp(x, L, qdot, k, Ts))
        print('q''  = ' , plane_heatflux(qdot, k))
        print('q    = ' , A*plane_heatflux(qdot, k))

        return (plane_temp(x, L, qdot, k, Ts) , plane_heatflux(qdot, k) , A*plane_heatflux(qdot, k))

    elif shape == 'cylinder':
       
        print('T(x) = ' , cylinder_temp(r, ro, qdot, k, Ts))
        print('q''  = ' , cylinder_heatflux(qdot, r))
        print('q    = ' , 2*pi*ro*L*cylinder_heatflux(qdot, r))

        return (cylinder_temp(r, ro, qdot, k, Ts) ,cylinder_heatflux(qdot, r) , 2*pi*ro*L*cylinder_heatflux(qdot, r))
    
    elif shape == 'sphere':

        print('T(x) = ' , sphere_temp(r, ro, qdot, k, Ts))
        print('q''  = ' , sphere_heatflux(qdot, r))
        print('q    = ' , 4*pi*ro**2*sphere_heatflux(qdot, r))

        return ( sphere_temp(r, ro, qdot, k, Ts) , sphere_heatflux(qdot, r) , 4*pi*ro**2*sphere_heatflux(qdot, r))

    elif shape == 0:
        print("please enter shape among , plane , cylinder , sphere")

def Uniform_cross_section_fins_Temturature_distribution(case = 0 , x = symbols('x'), L = symbols('L') , h = symbols('h'), P = symbols('P'),
    A = symbols('A'), k = symbols('k'),theta_L = symbols('theta_L'), theta_b = (' theta_b')):

    """
    Table 3.4 Temperature distribution and heat rates 
    for fins of uniform cross section

    case1 = convection at the end of tip
    case2 = adiabatic at the end of tip
    case3 = Regulated Temperature at the end of tip
    case4 = endless fin

    """

    def fun_m(h,P,k,A):
        return np.sqrt((h*P)/(k*A))

    def fun_M(h,P,k,A,theta_b):
        return np.sqrt(h*P*k*A)*theta_b

    m = fun_m(h,P,k,A)
    M = fun_M(h,P,k,A,theta_b)

    def Case_A_temperature(x, m, L, k, h):    
        # convection
        d1 = np.cosh(m*(L-x)) + (h/(m*k))*np.sinh(m*(L-x))
        d2 = np.cosh(m*L) + (h/(m*k))*np.sinh(m*L)
        return d1/d2

    def Case_A_heatrate(M, m, L, k, h):    
        # convection
        d1 = np.sinh(m*L) + (h/(m*k))*np.cosh(m*L)
        d2 = np.cosh(m*L) + (h/(m*k))*np.sinh(m*L)
        return M*d1/d2

    def Case_B_temperature(x, m, L):    
        # adiabatic
        return np.cosh(m*(L-x))/np.cosh(m*L)

    def Case_B_heatrate(M, m, L):    
        # adiabatic
        return M*np.tanh(m*L)

    def Case_C_temperature(x, m, L, theta_L, theta_b):    
        # prescribed temperature
        d1 = (theta_L/theta_b)*np.sinh(m*x) + np.sinh(m*(L-x))    
        return d1/np.sinh(m*L)

    def Case_C_heatrate(M, m, L, theta_L, theta_b):    
        # prescribed temperature
        q0 = M/np.sinh(m*L) * (np.cosh(m*L) - (theta_L/theta_b))
        qL = M/np.sinh(m*L) * (1 - np.cosh(m*L)*(theta_L/theta_b))
        return q0, qL

    def Case_D_temperature(x, m):
        # infinite fin
        return np.exp(-m*x)

    def Case_D_heatrate(M):
        # infinite fin
        return M


    if case == 1:

        print('T(x) = ' , Case_A_temperature(x, m, L, k, h))
        print('q''  = ' , Case_A_heatrate(M, m, L, k, h))

        return (Case_A_temperature(x, m, L, k, h) ,Case_A_heatrate(M, m, L, k, h))

    elif case == 2:

        print('T(x) = ' , Case_B_temperature(x, m, L))
        print('q''  = ' , Case_B_heatrate(M, m, L))

        return (Case_B_temperature(x, m, L),Case_B_heatrate(M, m, L))
    
    elif case == 3:

        print('T(x) = ' , Case_C_temperature(x, m, L, theta_L, theta_b))
        print('q''  = ' , Case_C_heatrate(M, m, L, theta_L, theta_b))

        return (Case_C_temperature(x, m, L, theta_L, theta_b) ,Case_C_heatrate(M, m, L, theta_L, theta_b))

    elif case == 4:

        print('T(x) = ' , Case_D_temperature(x, m))
        print('q''  = ' , Case_D_heatrate(M))

        return (Case_D_temperature(x, m) ,Case_D_heatrate(M))

    else:
        print("please enter correct case \n case1 = convection at the end of tip \n case2 = adiabatic at the end of tip \n case3 = Regulated Temperature at the end of tip \n case4 = endless fin ")

def Fin_effeciency(case = 0 , eta_f = symbols('eta_f'), N = symbols('N') , Af = symbols('Af'), At = symbols('At'),
    Rtc = symbols('Rtc'),k = symbols('k'), t = symbols('t'), h = symbols('h'), Ab = symbols('Ab'), theta_b = (' theta_b'),
    r1 = symbols("r1"), r2 = symbols('r2')):

    """
    Table 3.5 Fin efficiency
    
    """

    def overall_effeciency(eta_f, N, Af, At, Rtc=0, h=0, Ab=0):
        if Rtc == 0:
            C1 = 1
        else:
            C1 = 1 + eta_f*h*Af*Rtc/Ab
        return 1 - N*Af/At*(1 - eta_f/C1)


    def straight_rectangular(k, h, L, t, w=1, is_convection_tip=True):
        if is_convection_tip: 
            Lc = L + t/2
        else:
            Lc = L
        m = np.sqrt((2*h)/(k*t))
        Af = 2*w*Lc
        Ap = t*L
        eta = np.tanh(m*Lc)/(m*Lc)
        return eta, m, Af, Ap


    def straight_triangular(k, h, L, t, w=1):
        m = np.sqrt((2*h)/(k*t))
        Af = 2*w*np.sqrt(L**2 + (t/2)**2)
        Ap = t*L/2
        eta = 1/(m*L)*i1(2*m*L)/i0(2*m*L)
        return eta, m, Af, Ap


    def straight_parabolic(k, h, L, t, w=1):
        m = np.sqrt((2*h)/(k*t))
        C1 = np.sqrt(1 + (t/L)**2)
        Af = w*(C1*L + L**2/t*np.log(t/L + C1))
        Ap = t/3*L
        eta = 2/(np.sqrt(4*(m*L)**2 + 1) + 1)
        return eta, m, Af, Ap


    def annular_fin(k, h, r1, r2, t, is_convection_tip=True):
        if is_convection_tip:
            r2c = r2 + t/2
        else:
            r2c = r2
        m = np.sqrt((2*h)/(k*t))
        Af = 2*pi*(r2c**2 - r1**2)
        V = pi*(r2**2 - r1**2)*t
        C2 = (2*r1/m)/(r2c**2 - r1**2)
        d1 = k1(m*r1)*i1(m*r2c) - i1(m*r1)*k1(m*r2c)
        d2 = i0(m*r1)*k1(m*r2c) + k0(m*r1)*i1(m*r2c)
        eta = C2*d1/d2

        return eta, m, Af, V

    def pin_fin_rectangular(k, h, L, D, is_convection_tip=True):
        if is_convection_tip:
            Lc = L + D/4
        else:
            Lc = L
        m = np.sqrt((4*h)/(k*D))
        Af = pi*D*Lc
        V = pi*D**2/4 * L
        eta = np.tanh(m*Lc)/(m*Lc)
        return eta, m, Af, V

