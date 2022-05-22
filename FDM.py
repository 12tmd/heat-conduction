from sympy import*
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [12, 10]

Tem_S = ["Tem_S1","Tem_S2","Tem_S3","Tem_S4"]
Tem_A = ["Tem_A1","Tem_A2","Tem_A3","Tem_A4"]
h =     ["h1","h2","h3","h4"]
q =     ["q1","q2","q3","q4"]

value = ["dx","dy","k"]

EQ4view = []

def Tem_array(i,j):
    
    global Tem_S, Tem_A, h, q

    #모두 flaot으로 변경
    for a,b in zip(Tem_S,range(4)):
        if type(a) == int or type(a) == float:
            Tem_S[b] = float(a)
        else:
            pass
        
    for a,b in zip(Tem_A,range(4)):
        if type(a) == int or type(a) == float:
            Tem_A[b] = float(a)
        else:
            pass

    for a,b in zip(h,range(4)):
        if type(a) == int or type(a) == float:
            h[b] = float(a)
        else:
            pass

    for a,b in zip(q,range(4)):
        if type(a) == int or type(a) == float:
            q[b] = float(a)
        else:
            pass
        
    # 3차원 array 생성함 (z,x,y)축임....

    # z = 0 --> 각 지점별 표면온도
    # z = 1 --> 공기온도
    # z = 2 --> h 
    # z = 3 --> q
    # z = 4 --> qgen
    # z = 5 --> Node
    # z = 6 --> symbols

    arr = np.full((7,i,j),"x" , dtype= O)

    #Symbols 생성....
    n = 0
    for a in range(i):
        for b in range(j):
            if n < 10:
                arr[5,a,b] = symbols("T0{0}".format(n))
                arr[6,a,b] = symbols("T0{0}".format(n))
                n += 1

            else:
                arr[5,a,b] = symbols("T{0}".format(n))
                arr[6,a,b] = symbols("T{0}".format(n))
                n += 1

    # 조건 대입하기
    for a,b,c,d,e in zip(Tem_S,Tem_A,h,q,range(4)):

        if e == 0 :
            arr[0,0,:] = a  
            arr[1,0,:] = b
            arr[2,0,:] = c
            arr[3,0,:] = d

        elif e == 1:
            arr[0,:,j-1] = a  
            arr[1,:,j-1] = b
            arr[2,:,j-1] = c
            arr[3,:,j-1] = d

        elif e == 2:
            arr[0,i-1,:] = a
            arr[1,i-1,:] = b
            arr[2,i-1,:] = c
            arr[3,i-1,:] = d

        else:
            arr[0,:,0] = a
            arr[1,:,0] = b
            arr[2,:,0] = c
            arr[3,:,0] = d

    for a in range(i):
        for b in range(j):
            if type(arr[0,a,b]) == int or type(arr[0,a,b]) == float:
                arr[5,a,b] = arr[0,a,b]
            else:
                pass
    
    arr[5,0,0] = arr[6,0,0]
    arr[5,0,j-1] = arr[6,0,j-1]
    arr[5,i-1,j-1] = arr[6,i-1,j-1]
    arr[5,i-1,0] = arr[6,i-1,0]

    print(arr)
    print("----------------------------------------")
    
    return arr

def Eq_array(arr , EQ_num = (0,0)):

    #식을 세우는데 필요한 변수들은 global을 이용할것

    i = arr.shape[1]  
    j = arr.shape[2]
    
    global value
    global Tem_S, Tem_A, h, q 

    dx,dy,k = value
    Ts_1 ,Ts_2, Ts_3, Ts_4 = Tem_S
    Ta_1,Ta_2,Ta_3,Ta_4 = Tem_A
    h1,h2,h3,h4 = h
    q1,q2,q3,q4 = q

    ## Tem_array와 같은 형상의 array를 만들고 각각 위치에 온도를 구하는데 필요한 식을 넣는다.
    Eq_arr = np.zeros((i,j), dtype= O)

    # 표면의 식

    for a in range(0,i):
        for b in range(0,j):
            if type(arr[1,a,b]) == float:      #표면대류조건... 일때 공기온도 type으로 판별
                
                if (a,b) != (0,0) and (a,b) != (i-1,0) and (a,b) != (0,j-1) and (a,b) != (i-1,j-1):    #꼭지점 제외...
                    
                    if   a == 0: 

                        Eq_arr[a,b] = h1*dx*(Ta_1 - arr[6,a,b]) + k*dy*(arr[6,a,b-1]-arr[6,a,b])/dx + k*dy*(arr[6,a,b+1]-arr[6,a,b])/dx + k*dx*(arr[6,a+1,b]-arr[6,a,b])/dy

                    elif b == j-1:

                        Eq_arr[a,b] = h2*dy*(Ta_2 - arr[6,a,b]) + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy + k*dx*(arr[6,a+1,b]-arr[6,a,b])/dy + k*dy*(arr[6,a,b-1]-arr[6,a,b])/dx

                    elif a == i-1:

                        Eq_arr[a,b] = h3*dx*(Ta_3 - arr[6,a,b]) + k*dy*(arr[6,a,b-1]-arr[6,a,b])/dx + k*dy*(arr[6,a,b+1]-arr[6,a,b])/dx + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy

                    elif b == 0:

                        Eq_arr[a,b] = h4*dx*(Ta_4 - arr[6,a,b]) + k*dx*(arr[6,a+1,b]-arr[6,a,b])/dy + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy + k*dy*(arr[6,a,b+1]-arr[6,a,b])/dx

                    else:
                        pass
                else:
                    pass

            elif type(arr[3,a,b]) == float:      #q 있을때 type 판별

                if (a,b) != (0,0) and (a,b) != (i-1,0) and (a,b) != (0,j-1) and (a,b) != (i-1,j-1):     #꼭지점 제외...
                    
                    if   a == 0:

                        Eq_arr[a,b] =  q1*dx + k*dy*(arr[6,a,b-1] - arr[6,a,b]) / dx + k * dy * (arr[6,a,b+1] - arr[6,a,b] ) / dx + k * dx * (arr[6,a+1,b] - arr[6,a,b])/dy

                    elif b == j-1:

                        Eq_arr[a,b] =  q2*dy + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy + k*dx*(arr[6,a+1,b]-arr[6,a,b])/dy + k*dy*(arr[6,a,b-1]-arr[6,a,b])/dx

                    elif a == i-1:

                        Eq_arr[a,b] =  q3*dx + k*dy*(arr[6,a,b-1]-arr[6,a,b])/dx + k*dy*(arr[6,a,b+1]-arr[6,a,b])/dx + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy

                    elif b == 0:

                        Eq_arr[a,b] =  q4*dy + k*dx*(arr[6,a+1,b]-arr[6,a,b])/dy + k*dx*(arr[6,a-1,b]-arr[6,a,b])/dy + k*dy*(arr[6,a,b+1]-arr[6,a,b])/dx

                    else:
                        pass
                else:
                    pass

            else:
                pass

    #내부 온도 식

    for a in range(1,i-1):
        for b in range(1,j-1):
            Eq_arr[a,b] = (arr[5,a-1,b] + arr[5,a+1,b] + arr[5,a,b-1] + arr[5,a,b+1]) / 4 - arr[5,a,b]


    #꼭지점의 식

    #Coner1

        #case1 --> 표면온도 + 표면온도
    if type(Ts_1) == float and type(Ts_4) == float:

        Eq_arr[0,0] = (Ts_1 + Ts_4)/2 - arr[6,0,0]

        #case2 --> 대류 + 대류
    elif type(Ta_1) == float and type(Ta_4) == float:

        Eq_arr[0,0] = h1 * dx/2*(Ta_1 - arr[5,0,0]) + h4 * dy/2 * (Ta_4-arr[5,0,0]) + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 
        
        #case3 --> q'' + q''
    elif type(q1) == float and type(q4) == float:

        Eq_arr[0,0] = q1 * dx/2 + q4 * dy/2 + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

        #case4 --> 표면온도 + 대류
    elif type(Ts_1) == float and type(Ta_4) == float or type(Ts_4) == float and type(Ta_1) == float:

        if  type(Ts_1) == float and type(Ta_4) == float:

            Eq_arr[0,0] = h4 * dy/2 * (Ta_4 - arr[5,0,0]) + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 
        else:

            Eq_arr[0,0] = h1 * dx/2 * (Ta_1 - arr[5,0,0]) + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

        #case5 --> 표면온도 +  q''

    elif type(Ts_1) == float and type(q4) == float or type(Ts_4) == float and type(q1) == float:

        if  type(Ts_1) == float and type(q4) == float:

            Eq_arr[0,0] = q4*dy/2 + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

        else: 
            Eq_arr[0,0] = q1*dx/2 + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

        #case6 --> 대류 +  q''

    elif type(Ta_1) == float and type(q4) == float or type(Ta_4) == float and type(q1) == float:

        if  type(Ta_1) == float and type(q4) == float:

            Eq_arr[0,0] = h1 * dx/2 * (Ta_1 - arr[5,0,0]) + q4 * dy/2 + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

        else: 
            Eq_arr[0,0] = q1 * dx/2 + h4 * dy/2 * (Ta_4 - arr[5,0,0]) + k*dy/2*(arr[5,0,1]-arr[5,0,0])/dx + k * dx/2 * (arr[5,1,0]-arr[5,0,0])/dy 

    else:

        print("Coner1 ERROR")

    #Coner2
        #case1 --> 표면온도 + 표면온도
    if type(Ts_1) == float and type(Ts_2) == float:

        Eq_arr[0,j-1] = (Ts_1 + Ts_2)/2 - arr[6,0,j-1]

        #case2 --> 대류 + 대류

    elif type(Ta_1) == float and type(Ta_2) == float:

        Eq_arr[0,j-1] = h1 * dx/2 * (Ta_1 - arr[5,0,j-1]) + h2 * dy/2 * (Ta_2 - arr[5,0,j-1]) + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy 
        
        #case3 --> q'' + q''
    elif type(q1) == float and type(q2) == float:

        Eq_arr[0,j-1] = q1 * dx/2 + q2 * dy/2 + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy  

        #case4 --> 표면온도 + 대류

    elif type(Ts_1) == float and type(Ta_2) == float or type(Ts_2) == float and type(Ta_1) == float:

        if  type(Ts_1) == float and type(Ta_2) == float:

            Eq_arr[0,j-1] = h2 * dy/2 * (Ta_2 - arr[5,0,j-1]) + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy

        else:
            
            Eq_arr[0,j-1] = h1 * dx/2 * (Ta_1 - arr[5,0,j-1]) + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy

        #case5 --> 표면온도 +  q''

    elif type(Ts_1) == float and type(q2) == float or type(Ts_2) == float and type(q1) == float:

        if  type(Ts_1) == float and type(q4) == float:

            Eq_arr[0,j-1] = q2 * dy/2 + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy

        else: 
            Eq_arr[0,j-1] = q1 * dx/2 + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy 

        #case6 --> 대류 +  q''

    elif type(Ta_1) == float and type(q2) == float or type(Ta_2) == float and type(q1) == float:

        if  type(Ta_1) == float and type(q2) == float:

            Eq_arr[0,j-1] =  h1 * dx/2 * (Ta_1 - arr[5,0,j-1]) + q2 * dy/2 + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy

        else:
             Eq_arr[0,j-1] = h2 * dy/2 * (Ta_1 - arr[5,0,j-1]) + q1 * dx/2 + k * dy / 2 * (arr[5,0,j-2]-arr[5,0,j-1])/dx + k * dx/2 * (arr[5,1,j-1]-arr[5,0,j-1]) /dy

    else:
        print("Coner2 ERROR")


    #Coner3
        #case1 --> 표면온도 + 표면온도
    if type(Ts_2) == float and type(Ts_3) == float:

        Eq_arr[i-1,j-1] = (Ts_2 + Ts_3)/2 - arr[6,i-1,j-1]

        #case2 --> 대류 + 대류
    elif type(Ta_2) == float and type(Ta_3) == float:

        Eq_arr[i-1,j-1] = h2 * dy/2*(Ta_2 - arr[5,i-1,j-1]) + h3 * dx/2 * (Ta_3 - arr[5,i-1,j-1]) + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx 
        
        #case3 --> q'' + q''
    elif type(q2) == float and type(q3) == float:

        Eq_arr[i-1,j-1] = q2 * dy/2 + q3 * dx/2 + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx  

        #case4 --> 표면온도 + 대류

    elif type(Ts_2) == float and type(Ta_3) == float or type(Ts_3) == float and type(Ta_2) == float:

        if  type(Ts_2) == float and type(Ta_3) == float:
            Eq_arr[i-1,j-1] = h3 * dx/2 * (Ta_3 - arr[5,i-1,j-1]) + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx  
 
        else:
            Eq_arr[i-1,j-1] = h2 * dy/2 * (Ta_2 - arr[5,i-1,j-1]) + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx 

        #case5 --> 표면온도 +  q''

    elif type(Ts_2) == float and type(q3) == float or type(Ts_3) == float and type(q2) == float:

        if  type(Ts_2) == float and type(q3) == float:

            Eq_arr[i-1,j-1] = q3 * dx/2 + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx  

        else: 
            Eq_arr[i-1,j-1] = q2 * dy/2 + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx  

        #case6 --> 대류 +  q''

    elif type(Ta_2) == float and type(q3) == float or type(Ta_3) == float and type(q2) == float:

        if  type(Ta_2) == float and type(q3) == float:

            Eq_arr[i-1,j-1] = h2 * dy/2 * (Ta_2 - arr[5,i-1,j-1]) + q3*dx + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx

        else: 

            Eq_arr[i-1,j-1] = h3 * dx/2 * (Ta_3 - arr[5,i-1,j-1]) + q2*dy + k * dx / 2 * (arr[5,i-2,j-1] -arr[5,i-1,j-1]) / dx + k * dy / 2 * (arr[5,i-1,j-2]-arr[5,i-1,j-1]) / dx
 
    else:
        
        print("Coner3 ERROR")

    #Coner4       
        #case1 --> 표면온도 + 표면온도
    if type(Ts_3) == float and type(Ts_4) == float:

        Eq_arr[i-1,0] = (Ts_3 + Ts_4)/2 - arr[6,i-1,0]

        #case2 --> 대류 + 대류

    elif type(Ta_3) == float and type(Ta_4) == float:

        Eq_arr[i-1,0] =  h3 * dx/2 * (Ta_3 - arr[5,i-1,0]) + h4 * dy/2*(Ta_4 - arr[5,i-1,0]) + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx 
        
        #case3 --> q'' + q''
    elif type(q3) == float and type(q4) == float:

         Eq_arr[i-1,0] =  q3 * dx/2 + q4 * dy/2 + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx 

        #case4 --> 표면온도 + 대류

    elif type(Ts_3) == float and type(Ta_4) == float or type(Ts_4) == float and type(Ta_3) == float:

        if  type(Ts_3) == float and type(Ta_4) == float:
            Eq_arr[i-1,0] =  h4 * dy/2 * (Ta_4 - arr[5,i-1,0]) + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx  
 
        else:
            Eq_arr[i-1,0] =  h3 * dx/2 * (Ta_3 - arr[5,i-1,0]) + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx 

        #case5 --> 표면온도 +  q''

    elif type(Ts_3) == float and type(q4) == float or type(Ts_4) == float and type(q3) == float:

        if  type(Ts_3) == float and type(q4) == float:

            Eq_arr[i-1,0] =  q4 * dy/2 + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx

        else: 
            Eq_arr[i-1,0] =  q3 * dx/2 + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx

        #case6 --> 대류 +  q''

    elif type(Ta_3) == float and type(q4) == float or type(Ta_4) == float and type(q3) == float:

        if  type(Ta_3) == float and type(q4) == float:

            Eq_arr[i-1,0]=   h3 * dx/2 * (Ta_3 - arr[5,i-1,0]) + q4 * dy/2  + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx  

        else: 

            Eq_arr[i-1,0] =  h4 * dy/2 * (Ta_4 - arr[5,i-1,0]) + q3 * dx/2  + k * dx / 2 * (arr[5,i-2,0] -arr[5,i-1,0]) / dy + k * dy / 2 * (arr[5,i-1,1] - arr[5,i-1,0]) / dx  
 
    else:
        print("Coner4 ERROR")


    if EQ_num != (0,0):

        Eq_i = EQ_num[0] - 1
        Eq_j = EQ_num[1] - 1
        print(Eq_arr[Eq_i,Eq_j])

    global EQ4view
    EQ4view.append(Eq_arr) 

    Eq_arr = flatten(list(Eq_arr))
    return tuple(Eq_arr)


def Ploting(n,m):

    A = Tem_array(n,m)
    B = Eq_array(A)
    C = solve(B)

    Node_array = A[5]
    Node_array = flatten(Node_array)

    for a,b in zip(Node_array,range(n*m)):

        if type(a) == type(symbols("T")):
            Node_array[b] = float("{:.1f}".format(C[symbols("{0}".format(a))]))

        else:
            pass

    Ans_array = np.array(Node_array).reshape(n,m)
    ax = sns.heatmap(Ans_array, linewidth=0.000001, cmap= plt.cm.jet, fmt='0.2f', annot=True)  # annot=True
    plt.show()


def FDM_practice(s1,s2,s3,s4,qgen = 0):


    T = symbols("T")
    k = symbols("k")

    T1 , T2 , T3 , T4 = symbols("T1 T2 T3 T4")
    T_a1 , T_a2, T_a3 , T_a4 = symbols("T_a1 T_a2 T_a3 T_a4")
    h_1 , h_2 , h_3 , h_4 = symbols("h1 h2 h3 h4")
    q1, q2, q3, q4 = symbols("q1 q2 q3 q4 ")
    dx , dy = symbols("dx dy")

    def Conduction(k,Th,TL,A,L):
        return (k)*(Th-TL)*A/L

    def Convection(h,A,Tair,Ts):
        return h*(A)*(Ts - Tair)

    def Q_flux(q,A):
        return q*A

    boundry =[s1,s2,s3,s4]                  #conduction1 convection2 qflux3
    Temperature = [T1, T2, T3, T4]
    Tem_air = [ T_a1 , T_a2, T_a3 , T_a4]
    h = [ h_1 , h_2 , h_3 , h_4]
    q = [q1, q2, q3, q4]
    A_s = [dx*1,dy*1,dx*1,dy*1]
    L_s = [dy,dx,dy,dx]

    EQ = []

    for a,Ts,Ta,hs,qs,A,L in zip(boundry,Temperature,Tem_air,h,q,A_s,L_s):
        if a == 1:
            EQ.append(Conduction(k,Ts,T,A,L))
        
        elif a == 2:
            EQ.append(Convection(hs,A,Ta,T))

        elif a ==3:
            EQ.append(Q_flux(qs,A))

        else:
            print("ERROR")
            continue
    
    if qgen == 0:
        pass
    else:
        EQ.append(qgen*dx*dy)
        return EQ[0]+EQ[1]+EQ[2]+EQ[3]+EQ[4]

    return EQ[0]+EQ[1]+EQ[2]+EQ[3]