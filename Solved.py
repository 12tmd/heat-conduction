from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
from PyQt5.QtWidgets import *
from PyQt5 import*
from PyQt5 import uic
import numpy as np
from sympy import*
from sympy.simplify.fu import TR10i

form_class5 = uic.loadUiType("Solved.ui")[0]

class Solved(QMainWindow, form_class5):

    eq4else = ['Eq자리','x1위치','x2위치', '대류표면온도']

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        #메인윈도우로 옮길거....
        self.graphwindow = Graphwindow()
        self.opengl = Opengl()


        #라디오 버튼 선택...
        Radiosel = np.zeros(2,dtype= np.int0)
        Radiobutton1 = [self.radioButton_1,self.radioButton_2,self.radioButton_3
        ,self.radioButton_4]

        Radiobutton2 = [self.radioButton_5,self.radioButton_6,self.radioButton_7
        ,self.radioButton_8]


        for a,b in zip(Radiobutton1,Radiobutton2):
            a.setAutoExclusive(False)   
            b.setAutoExclusive(False)   

        def BC1():
            for a,b in zip(Radiobutton1,range(4)):
                if a.isChecked():
                    Radiosel[0] = b
                    print(Radiosel)

        def BC2():
            for a,b in zip(Radiobutton2,range(4)):
                if a.isChecked():
                    Radiosel[1] = b
                    print(Radiosel)

        for a in Radiobutton1:
            a.toggled.connect(BC1)

        for a in Radiobutton2:
            a.toggled.connect(BC2)

        #k값 목록
        k = ["Material"
        , "Aluminum Pure , k = 237W/m*k"
        , "Berylium , k = 200W/m*k" 
        , "Bismuth , k = 7.86W/m*k"
        , "Boron , k = 27.0W/m*k"
        , "Cadmium , k = 96.8W/m*k"
        , "Chromium , k = 93.7W/m*k"
        , "Cobalt , k = 99.2W/m*k"
        , "Copper Pure , k = 401W/m*k"
        , "Germanium , k = 59.9W/m*k"
        , "Gold , k = 317W/m*k"
        , "Iridium , k = 147W/m*k"
        , "Iron Pure , k = 80.2W/m*k"
        , "Carbon steeels , k = 60.5W/m*k"
        , "Carbon silicon, k = 51.9W/m*k"
        , "Carbon-manganese-silicon, k = 41.0W/m*k"
        , "Stainless steels AISI 302, k = 15.1W/m*k"
        , "Stainless steels AISI 304, k = 14.9W/m*k"
        , "Stainless steels AISI 316, k = 13.4W/m*k"
        , "Stainless steels AISI 347, k = 14.2W/m*k"
        , "Lead, k = 35.3W/m*k"
        , "Magnesium, k = 156W/m*k"
        , "Molybdenum, k = 138W/m*k"
        , "Nickel Pure, k = 90.7W/m*k"
        , "Niobium, k = 53.7W/m*k"
        , "Palladium, k = 71.8W/m*k"
        , "Platinum Pure, k = 71.6W/m*k"
        , "Rhenium, k = 47.9W/m*k"
        , "Rhodium, k = 150W/m*k"
        , "Silicon, k = 148W/m*k"
        , "Silver, k = 429W/m*k"
        , "Tantalum, k = 57.5W/m*k"
        , "Thorium, k = 54.0W/m*k"
        , "Tin, k = 66.6W/m*k"
        , "Titanium, k =21.9 W/m*k"
        , "Tungsten, k = 174W/m*k"
        , "Uranium, k = 27.6W/m*k"
        , "Vanadium, k = 30.7W/m*k"
        , "Zinc, k = 116W/m*k"
        , "Zirconium, k = 22.7W/m*k"
        ]

        knum = [0 
        , 237
        , 200
        , 7.86
        , 27.0
        , 96.8
        , 93.7
        , 99.2
        , 401
        , 59.9
        , 317
        , 147
        , 80.2
        , 60.5
        , 51.9
        , 41.0
        , 15.1
        , 14.9
        , 13.4
        , 14.2
        , 35.3
        , 156
        , 138
        , 90.7
        , 53.7
        , 71.8
        , 71.6
        , 47.9
        , 150
        , 148
        , 429
        , 57.5
        , 54.0
        , 66.6
        , 21.9
        , 174
        , 27.6
        , 30.7
        , 116
        , 22.7
        ]
        for a in k:
            self.comboBox.addItem("{0}".format(a))

        #연립방정식 풀기
        def Symbolcal():

            F  = Function('F')
            q,k,x,C1,C2,T  = symbols('q k x C1 C2 T')
            F = -q/(2*k)*x**2 + C1*x + C2 - T
            kvalue = knum[self.comboBox.currentIndex()]
            F = F.subs(k,kvalue)

            try:
                q1 = float(self.qgen.text())
                F  = F.subs(q,q1)

            except ValueError:
                F  = F.subs(q,0)

            def Bc1():

                if  Radiosel[0] == 0:                           #일정표면온도

                    x1 = float(self.lineEdit_1.text())          #x1값 Ui로부터 받아오기
                    self.eq4else[1] = x1                        #그래프 생성를 위해서 x1위치 저장하기

                    t1 = float(self.lineEdit_2.text())
                    f1 = F.subs([(x,x1),(T,t1)])

                    return f1

                elif  Radiosel[0] == 1:                         #일정 열유속

                    x2 = float(self.lineEdit_3.text())
                    self.eq4else[1] = x2
                    q1 = float(self.lineEdit_4.text())

                    f1 = -kvalue*F.diff(x).subs(x,x2) - q1

                    return f1

                elif Radiosel[0] == 2:                           #단열조건

                    x3 = float(self.lineEdit_5.text())
                    self.eq4else[1] = x3

                    f1 = F.diff(x).subs(x,x3)


                    return f1

                elif Radiosel[0] == 3:                          #표면대류조건

                    x4   = float(self.lineEdit_6.text())
                    self.eq4else[1] = x4

                    h1   = float(self.lineEdit_7.text())
                    Tair = float(self.lineEdit_8.text())

                    q4 = float(self.lineEdit_9.text())
                    Ts = float(self.lineEdit_10.text())

                    if Ts == 0:
                        
                        Tsur = symbols('Tsur')
                        q4 = float(self.lineEdit_9.text())

                        f2 = h1*(Tair - Tsur) + q4
                        Ts = solve(f2)

                        return Ts

                    elif q4 == 0:

                        Ts = float(self.lineEdit_10.text())
                        
                        return Ts
                
                else:
                    pass

            def Bc2():

                if Radiosel[1] == 0:

                    x1 = float(self.lineEdit_11.text())
                    self.eq4else[2] = x1

                    t1 = float(self.lineEdit_12.text())

                    f1 = F.subs(x,x1)
                    f1 = f1.subs(T,t1)

                    return f1

                elif  Radiosel[1] == 1:

                    x2 = float(self.lineEdit_13.text())
                    self.eq4else[2] = x2
                    q1 = float(self.lineEdit_14.text())

                    f1 = -kvalue*F.diff(x).subs(x,x2) - q1

                    return f1

                elif Radiosel[1] == 2:

                    x3 = float(self.lineEdit_15.text())
                    self.eq4else[2] = x3          

                    f1 = F.diff(x).subs(x,x3)

                    return f1

                elif Radiosel[1] == 3:

                    x4   = float(self.lineEdit_16.text())
                    self.eq4else[2] = x4

                    h1   = float(self.lineEdit_17.text())
                    Tair = float(self.lineEdit_18.text())


                    q4 = float(self.lineEdit_19.text())
                    Ts = float(self.lineEdit_20.text())

                    if Ts == 0:
                        
                        Tsur = symbols('Tsur')
                        q4 = float(self.lineEdit_19.text())

                        f2 = h1*(Tair - Tsur) + q4
                        Ts = solve(f2)

                        return Ts

                    elif q4 == 0:

                        Ts = float(self.lineEdit_20.text())

                        return Ts

                else:
                    pass

            return [Bc1(),Bc2()]

        #식 출력하기
        def Showeq():            

            q,k,x,C1,C2,T  = symbols('q k x C1 C2 T')

            F = -q/(2*k)*x**2 + C1*x + C2 - T

            kvalue = knum[self.comboBox.currentIndex()]
            ans = Symbolcal()
            print(ans)


            if Radiosel[0] == 0 and Radiosel[1] == 0:                                                           #경우1 : 양쪽 표면온도를 아는상태

                ans = solve((ans[0],ans[1]))
                c1,c2 = ans[C1],ans[C2]
                q1 = float(self.qgen.text())
                
                F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T

                self.textBrowser.clear()
                self.textBrowser.append('T(x) = {0}'.format(str(F)))
                self.eq4else[0] = F


            elif (Radiosel[0] == 0 and Radiosel[1] == 2) or (Radiosel[0] == 2 and Radiosel[1] == 0):            #경우2 : 한쪽 표면온도 , 한쪽 단열


                ans = solve((ans[0],ans[1]))
                c1,c2 = ans[C1],ans[C2]
                q1 = float(self.qgen.text())

                F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T
                self.textBrowser.clear()
                self.textBrowser.append('T(x) = {0}'.format(str(F)))
                self.eq4else[0] = F


            elif (Radiosel[0] == 1 and Radiosel[1] == 0) or (Radiosel[0] == 0 and Radiosel[1] == 1):             #경우3 : 한쪽 표면온도 , 열유속

                ans = solve([ans[0],ans[1]],[C1,C2])
                c1,c2 = ans[C1],ans[C2]
                q1 = float(self.qgen.text())

                F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T

                self.textBrowser.clear()
                self.textBrowser.append('T(x) = {0}'.format(str(F)))
                self.eq4else[0] = F


            elif (Radiosel[0] == 3 and Radiosel[1] == 0) or (Radiosel[0] == 0 and Radiosel[1] == 3):             #경우4 : 한쪽 일정표면, 대류 

                if Radiosel[0] == 3 and Radiosel[1] == 0:

                    q1 = float(self.qgen.text())

                    Ts = ans[0][0]

                    x1 = float(self.lineEdit_6.text())
                    t1 = Ts

                    x2 = float(self.lineEdit_11.text())
                    t2 = float(self.lineEdit_12.text())

                    f1 = F.subs([(x,x1),(q,q1),(T,t1),(k,kvalue)])
                    f2 = F.subs([(x,x2),(q,q1),(T,t2),(k,kvalue)])

                    ans = solve((f1,f2))

                    c1,c2 = ans[C1],ans[C2]

                    F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0}'.format(str(F)))
                    self.eq4else[0] = F


                elif Radiosel[0] == 0 and Radiosel[1] == 3:

                    q1 = float(self.qgen.text())

                    Ts = ans[1]

                    x1 = float(self.lineEdit_1.text())
                    t1 = float(self.lineEdit_2.text())

                    x2 = float(self.lineEdit_16.text())
                    t2 = ans[1][0]


                    f1 = F.subs([(x,x1),(q,q1),(T,t1),(k,kvalue)])

                    f2 = F.subs([(x,x2),(q,q1),(T,t2),(k,kvalue)])

                    ans = solve((f1,f2))

                    c1,c2 = ans[C1],ans[C2]

                    F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0}'.format(str(F)))
                    self.eq4else[0] = F
            
            elif Radiosel[0] == 1 and Radiosel[1] == 1 :                                                        #경우5 : 열유속 , 열유속


                pass


            elif (Radiosel[0] == 2 and Radiosel[1] == 1) or (Radiosel[0] == 1 and Radiosel[1] == 2):            #경우6:  열유속 , 단열

                if ans[0]   == C1:

                    ans = solve(ans[1],C1)
                    c1 = ans[0]                    

                    q1 = float(self.qgen.text())

                    F = F.subs([(C1,c1),(C2,0),(q,q1),(k,kvalue)]) + T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0} + C2'.format(str(F)))
                    self.eq4else[0] = F

                elif ans[1] == C1:

                    ans = solve(ans[0],C1)
                    c1 = ans[0]

                    q1 = float(self.qgen.text())

                    F = F.subs([(C1,c1),(C2,0),(q,q1),(k,kvalue)]) + T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0} + C2'.format(str(F)))
                    self.eq4else[0] = F

                else:

                    ans = solve([ans[0],ans[1]],[C1])
                    c1 = ans[0]
                    q1 = float(self.qgen.text())

                    F = F.subs([(C1,c1),(C2,0),(q,q1),(k,kvalue)]) + T


                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0} +C2'.format(str(F)))
                    self.eq4else[0] = F



            elif (Radiosel[0] == 3 and Radiosel[1] == 2) or (Radiosel[0] == 2 and Radiosel[1] == 3):             #경우7 : 열유속 , 대류

                pass





            elif (Radiosel[0] == 3 and Radiosel[1] == 1) or (Radiosel[0] == 1 and Radiosel[1] == 3):             #경우8 : 단열 , 단열

                pass




            elif (Radiosel[0] == 3 and Radiosel[1] == 2) or (Radiosel[0] == 2 and Radiosel[1] == 3):             #경우9 : 단열 ,대류

                
                ans = solve((ans[0],ans[1]))
                Tsur = ans[T]

                try:

                    x1 = float(self.lineEdit_5.text())
                    q1 = float(self.qgen.text())

                    x2 = float(self.lineEdit_16.text())
                    t2 = Tsur

                    f1 = F.diff(x).subs([(x,x1),(q,q1),(k,kvalue)])
                    f2 = F.subs([(x,x2),(q,q1),(T,t2),(k,kvalue)])

                    ans = solve((f1,f2))
                    c1,c2 = ans[C1],ans[C2]

                    F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)])+  T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0}'.format(str(F)))
                    self.eq4else[0] = F


                except ValueError:

                    x1 = float(self.lineEdit_5.text())
                    t1 = Tsur                

                    q1 = float(self.qgen.text())

                    x2 = float(self.lineEdit_16.text())
                    t2 = ans[T]

                    f1 = F.subs([(x,x1),(q,q1),(T,t1),(k,kvalue)])
                    f2 = F.diff(x).subs([(x,x2),(q,q1),(k,kvalue)])

                    ans = solve((f1,f2))
                    c1,c2 = ans[C1],ans[C2]

                    F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T

                    self.textBrowser.clear()
                    self.textBrowser.append('T(x) = {0}'.format(str(F)))
                    self.eq4else[0] = F


            elif Radiosel[0] == 3 and Radiosel[1] == 3:                                                       #경우10 : 대류, 대류

                print(ans)

                
                x1 = float(self.lineEdit_6.text())
                t1 = np.array(ans[0])[0]

                x2 = float(self.lineEdit_16.text())
                t2 = np.array(ans[1])[0]

                q1 = float(self.qgen.text())


                f1 = F.subs([(x,x1),(q,q1),(k,kvalue),(T,t1)])
                f2 = F.subs([(x,x2),(q,q1),(k,kvalue),(T,t2)])

                ans = solve((f1,f2))

                c1,c2 = ans[C1],ans[C2]

                F = F.subs([(C1,c1),(C2,c2),(q,q1),(k,kvalue)]) + T


                self.textBrowser.clear()
                self.textBrowser.append('T(x) = {0}'.format(str(F)))

                self.eq4else[0] = F


        self.pushButton_1.clicked.connect(Showeq)
        self.pushButton_2.clicked.connect(self.show_graph)
        self.pushButton_3.clicked.connect(self.show_opengl)

    def show_graph(self):
        self.graphwindow.show()

    def show_opengl(self):
        self.opengl.show()

class Graphwindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()                            #Qwiget 을 만듬
        self.setCentralWidget(self.main_widget)                 #QMainWindow에 이걸해야지 뭐든지 추가할 수있는거임..

        button = QPushButton("Show Graph")                      #버튼을 생성함
        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))      #canvas도 생성함
        vbox = QVBoxLayout(self.main_widget)                    #layout도 생성함
        self.ax = self.canvas.figure.subplots()

        vbox.addWidget(self.canvas)                             #layout에 canvas를 추가
        vbox.addWidget(button)                                  #이렇게 추가해야지 실제로 적용되는것.
        self.addToolBar(NavigationToolbar(self.canvas, self))   #toolbor 추가

        self.setWindowTitle('Graph')                            #이름,크기지정
        self.setGeometry(300, 100, 600, 400)
        button.clicked.connect(self.update_chart)               #버튼 기능

    def update_chart(self):                                     #그래프 추가하기
        x = symbols("x")
        f = lambdify(x,Solved.eq4else[0],"numpy")

        x1 = Solved.eq4else[1]
        x2 = Solved.eq4else[2]
        ex = (x2-x1)/20

        
        x = np.linspace(x1,x2,100)
                                                                #grid 추가하는 방법 찾아보기.....
                                                                
        self.ax.grid()
        self.ax.set_xlim([x1-ex, x2+ex])    
        self.plot = self.ax.plot(x,f(x),'r')                    #이렇게 새로운 값을 대입할 수 있는것
        self.canvas.draw()                                      #show 말고 draw 그림

class Opengl(QOpenGLWidget):                                    #그림그리기.....

    x = symbols('x')

    def  __init__(self):
        super().__init__()
 
    def initializeGL(self):
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
 
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
 
        glClearDepth(1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
 
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
 
    def resizeGL(self, width, height):
        glGetError()
 
        aspect = width if (height == 0) else width / height
 
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
 
    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()


        glClearColor(0.2, 0.2, 0 , 0)                           #바탕화면 색깔
        glPushMatrix()
        glTranslatef(0.0, 0.0, -3.0)                            #시점조정하기...
        self.Draw()
        glPopMatrix()
        glFlush()
 
    def Draw(self):

        def Vertices():                                             #좌표......

            x = np.linspace(-1,1,200)
            ver= []

            for a in x:
                ver1 = [a,-0.5]
                ver2 = [a, 0.5]
                ver.append(ver1)
                ver.append(ver2)

            return ver

        def Color():                                                #색배합 조정하기

            expr = lambdify(self.x,Solved.eq4else[0],'numpy')
            x = np.linspace(Solved.eq4else[1],Solved.eq4else[2],200)
            T = np.array(expr(x))
            T_avg = np.average(T)                   #평균값
            
            dT = T-T_avg                            # dT= 온도 - 평균 

            print(dT)
            dT_max = np.max(dT)
            dT_min = np.min(dT)

            color= []
        
            for T in dT:
                if T > 0:
                    if    dT_max >= T >=  0.93*dT_max:
                        color1 = [253/253,0,0]
                        color2 = [253/253,0,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.93*dT_max> T >= 0.86*dT_max:
                        color1 = [253/253,34/253,0]
                        color2 = [253/253,34/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.86*dT_max> T >= 0.79*dT_max:
                        color1 = [253/253,68/253,0]
                        color2 = [253/253,68/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.79*dT_max> T >= 0.72*dT_max:
                        color1 = [253/253,102/253,0]
                        color2 = [253/253,102/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.72*dT_max> T >= 0.65*dT_max:
                        color1 = [253/253,136/253,0]
                        color2 = [253/253,136/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.65*dT_max> T >= 0.58*dT_max:
                        color1 = [253/253,170/253,0]
                        color2 = [253/253,170/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.58*dT_max> T >= 0.51*dT_max:
                        color1 = [253/253,204/253,0]
                        color2 = [253/253,204/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.51*dT_max> T >= 0.44*dT_max:
                        color1 = [253/253,238/253,0]
                        color2 = [253/253,238/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.44*dT_max> T >= 0.37*dT_max:
                        color1 = [233/253,253/253,0]
                        color2 = [233/253,253/253,0]
                        color.append(color1)
                        color.append(color2)
                        
                    elif 0.37*dT_max> T >= 0.30*dT_max:
                        color1 = [199/253,253/253,0]
                        color2 = [199/253,253/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.30*dT_max> T >= 0.23*dT_max:
                        color1 = [165/253,253/253,0]
                        color2 = [165/253,253/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.23*dT_max> T >= 0.16*dT_max:
                        color1 = [131/253,253/253,0]
                        color2 = [131/253,253/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.16*dT_max> T >= 0.09*dT_max:
                        color1 = [97/253,253/253,0]
                        color2 = [97/253,253/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.09*dT_max> T >= 0.02*dT_max:
                        color1 = [63/253,253/253,0]
                        color2 = [63/253,253/253,0]
                        color.append(color1)
                        color.append(color2)

                    elif 0.02*dT_max> T >= 0.00*dT_max:
                        color1 = [29/253,253/253,0]
                        color2 = [29/253,253/253,0]
                        color.append(color1)
                        color.append(color2) 

                else:
                    if dT_min <= T < 0.93*dT_min:               #가장 차가운
                        color1 = [0,25/253,253/253]
                        color2 = [0,25/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.93*dT_min <= T < 0.86*dT_min:
                        color1 = [0,59/253,253/253]
                        color2 = [0,59/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.86*dT_min <= T < 0.79*dT_min:
                        color1 = [0,93/253,253/253]
                        color2 = [0,93/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.79*dT_min <= T < 0.72*dT_min:
                        color1 = [0,127/253,253/253]
                        color2 = [0,127/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.72*dT_min <= T < 0.65*dT_min:
                        color1 = [0,161/253,253/253]
                        color2 = [0,161/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.65*dT_min <= T < 0.58*dT_min:
                        color1 = [0,195/253,253/253] 
                        color2 = [0,195/253,253/253] 
                        color.append(color1)
                        color.append(color2)

                    elif 0.58*dT_min <= T < 0.51*dT_min:
                        color1 = [0,229/253,253/253]
                        color2 = [0,229/253,253/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.51*dT_min <= T < 0.44*dT_min:
                        color1 = [0,253/253,243/253]
                        color2 = [0,253/253,243/253]
                        color.append(color1)
                        color.append(color2) 

                    elif 0.44*dT_min <= T < 0.37*dT_min:
                        color1 = [0,253/253,209/253]
                        color2 = [0,253/253,209/253]
                        color.append(color1)
                        color.append(color2)  

                    elif 0.37*dT_min <= T < 0.30*dT_min:
                        color1 = [0,253/253,175/253]
                        color2 = [0,253/253,175/253]
                        color.append(color1)
                        color.append(color2) 

                    elif 0.30*dT_min <= T < 0.23*dT_min:
                        color1 = [0,253/253,141/253]
                        color2 = [0,253/253,141/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.23*dT_min <= T < 0.16*dT_min:
                        color1 = [0,253/253,107/253]
                        color2 = [0,253/253,107/253]
                        color.append(color1)
                        color.append(color2) 

                    elif 0.16*dT_min <= T < 0.09*dT_min:
                        color1 = [0,253/253,73/253]
                        color2 = [0,253/253,73/253]
                        color.append(color1)
                        color.append(color2) 

                    elif 0.09*dT_min <= T < 0.02*dT_min:
                        color1 = [0,253/253,39/253]
                        color2 = [0,253/253,39/253]
                        color.append(color1)
                        color.append(color2)

                    elif 0.02*dT_min <= T < 0.00*dT_min:
                        color1 = [0,253/253,5/253]
                        color2 = [0,253/253,5/253]
                        color.append(color1)
                        color.append(color2)   
                
            return color

        glBegin(GL_TRIANGLE_STRIP)                              #(GL_TRIANGLE_STRIP으로 그릴것

        for a,b in zip(Vertices(),Color()):

            glColor3fv(b)                                       #색깔이 먼저 언급되어야한다.
            glVertex2fv(a)                                      #그다음이 좌표임

        glEnd()

def solve_show():
    app = QApplication(sys.argv)
    myWindow = Solved()
    myWindow.show()
    sys.exit(app.exec_())
