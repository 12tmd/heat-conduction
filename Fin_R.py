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
import matplotlib.pyplot as plt
from sympy.core.numbers import Infinity


form_class6 = uic.loadUiType("FinR.ui")[0]

class FinR(QMainWindow, form_class6):

    val4else = ['T(x)','q','q4C','x','L','m','M','t']

    def __init__(self):


        self.graphwindow = Graphwindow()
        self.opengl = Opengl()

        super().__init__()
        self.setupUi(self)

        self.Radiobutton = [self.radioButton_1,self.radioButton_2,self.radioButton_3,
            self.radioButton_4]


        def BC():
            for a,b in zip(self.Radiobutton,range(4)):
                if a.isChecked():
                    self.Radiosel[0] = b
                    print(b)

        self.Radiosel = np.ones(1,dtype= np.int0)*5

        for a in self.Radiobutton:
            a.toggled.connect(BC)

        self.pushButton_1.clicked.connect(self.Calfin)
        self.pushButton_2.clicked.connect(self.show_graph)
        self.pushButton_3.clicked.connect(self.show_opengl)


    def Calfin(self):

        Bc = self.Radiosel

        #공통 변수 설정..
        try:
            w = float(self.lineEdit_w.text())

        except ValueError:
            w = 1

        x = symbols('x')
        L = symbols('L')
        
        k = float(self.lineEdit_k.text())
        h = float(self.lineEdit_h.text())
        t = float(self.lineEdit_t.text())
        self.val4else[7] = t

        T_b = float(self.lineEdit_tb.text())
        T_a =float(self.lineEdit_ta.text())

        theta_b = T_b - T_a
        P = 2*(w+t)
        A = w*t


    #입력받은 값을 이용해서 m,M,theha_b 를 얻음

        M = self.fun_M(h,P,k,A,theta_b)
        m = self.fun_m(h,P,k,A)
        theta  = self.Case_A_temperature(x,m,L,k,h)

        if Bc == 0:             #BC1

            L = float(self.lineEdit_1_L.text())
            theta  = self.Case_A_temperature(x,m,L,k,h)


            T = theta*(theta_b) + T_a
            q = self.Case_A_heatrate(M,m,L,k,h)


        #따로 저장해 놓을것 --> 다른곳에서 쓸 수 있음
            self.val4else[0] = T
            self.val4else[1] = q
            self.val4else[4] = L

            try:
                x1 = float(self.lineEdit_1_x.text())

                self.textBrowser_1.append(" T({0}) = {1} ".format(str(x1),str(T.subs(x,x1))))
                self.textBrowser_1.append(" T(x) = {0} ".format(str(N(T,3))))
                self.textBrowser_2.append(" q = {0}".format(str(q)))

            except ValueError:

                self.textBrowser_1.append(" T({0}) ={1} ".format((str(x),str(T))))
                self.textBrowser_1.append(" T(x) ={0} ".format(str(N(T,3))))
                self.textBrowser_2.append(" q = {0} ".format(str(q)))

        elif Bc == 1:               #BC2

            L = float(self.lineEdit_2_L.text())
            theta  = self.Case_B_temperature(x,m,L)

            T = theta*(theta_b) + T_a
            q = self.Case_B_heatrate(M,m,L)

        #따로 저장해 놓을것 --> 다른곳에서 쓸 수 있음
            self.val4else[0] = T
            self.val4else[1] = q
            self.val4else[4] = L

            print(self.val4else[0])

            try:
                x1 = float(self.lineEdit_2_x.text())

                self.textBrowser_1.append(" T({0}) = {1} ".format(str(x1), str(T.subs(x,x1))))
                self.textBrowser_1.append(" T(x) = {0} ".format(str(T)))
                self.textBrowser_2.append(" q = {0}".format(str(q)))

            except ValueError:

                self.textBrowser_1.append(" T({0}) ={1} ".format(str(x),str(T.subs(x,x))))
                self.textBrowser_2.append(" q = {0} ".format(str(q)))


        elif Bc == 2:               #BC3

            L   = float(self.lineEdit_3_L.text())
            T_L = float(self.lineEdit_3_T.text())

            theta_L = T_L - T_a
            theta_b = T_b - T_a

            theta  = self.Case_C_temperature(x,m,L,theta_L,theta_b)

            T = theta*(theta_b) + T_a

            q = self.Case_C_heatrate(M,m,L,theta_L,theta_b)


        #따로 저장해 놓을것 --> 다른곳에서 쓸 수 있음

            self.val4else[0] = T
            self.val4else[1] = q[0]
            self.val4else[2] = q[1]
            self.val4else[4] = L

            try:
                x1 = float(self.lineEdit_3_x.text())

                self.textBrowser_1.append(" T({0}) ={1} ".format(str(x1),str(T.subs(x,x1))))
                self.textBrowser_1.append(" T(x) ={0} ".format(str(T)))

                self.textBrowser_2.append(" q0 = {0}".format(str(q[0])))
                self.textBrowser_2.append(" qL = {0}".format(str(q[1])))

            except ValueError:

                self.textBrowser_1.append(" T({0}) ={1} ".format(str(x),str(T.subs(x,x))))
                self.textBrowser_1.append(" T(x) ={0} ".format(str(T)))


                self.textBrowser_2.append(" q0 = {0}".format(str(q[0])))
                self.textBrowser_2.append(" qL = {0}".format(str(q[1])))

        elif Bc == 3:               #BC3

            theta  = self.Case_D_temperature(x,m)

            T = theta*(theta_b) + T_a
            q = self.Case_D_heatrate(M)

            L = 10

        #따로 저장해 놓을것 --> 다른곳에서 쓸 수 있음
            self.val4else[0] = T
            self.val4else[1] = q
            self.val4else[4] = L

            try:
                x1 = float(self.lineEdit_4_x.text())

                self.textBrowser_1.append(" T({0}) ={1} ".format(str(x1),str(T.subs(x,x1))))
                self.textBrowser_1.append(" T(x) ={0} ".format(str(T)))

                self.textBrowser_2.append(" q = {0}".format(str(q)))

            except ValueError:

                self.textBrowser_1.append(" T({0}) ={1} ".format(str(x),str(T.subs(x,x))))
                self.textBrowser_1.append(" T(x) ={0} ".format(str(T)))

                self.textBrowser_2.append(" q = {0} ".format(str(q)))

        else:
            pass


    def fun_m(self,h,P,k,A):
        return sqrt((h*P)/(k*A))

    def fun_M(self,h,P,k,A,theta_b):

        return sqrt(h*P*k*A)*theta_b

    def Case_A_temperature(self,x, m, L, k, h):    
        # convection
        d1 = N(cosh(m*(L-x)) + (h/(m*k))*sinh(m*(L-x)),2)
        d2 = N(cosh(m*L) + (h/(m*k))*sinh(m*L),2)

        return N(d1/d2,2)

    def Case_A_heatrate(self,M, m, L, k, h):    
        # convection
        d1 = sinh(m*L) + (h/(m*k))*cosh(m*L)
        d2 = cosh(m*L) + (h/(m*k))*sinh(m*L)
        return M*d1/d2

    def Case_B_temperature(self,x, m, L):    
        # adiabatic
        return cosh(m*(L-x))/cosh(m*L)

    def Case_B_heatrate(self,M, m, L):    
        # adiabatic
        return M*tanh(m*L)

    def Case_C_temperature(self,x, m, L, theta_L, theta_b):    
        # prescribed temperature
        d1 = (theta_L/theta_b)*sinh(m*x) + sinh(m*(L-x))    
        return d1/sinh(m*L)

    def Case_C_heatrate(self,M, m, L, theta_L, theta_b):    
        # prescribed temperature
        q0 = M/sinh(m*L) * (cosh(m*L) - (theta_L/theta_b))
        qL = M/sinh(m*L) * (1 - cosh(m*L)*(theta_L/theta_b))
        return [q0, qL]

    def Case_D_temperature(self,x,m):
        # infinite fin
        return exp(-m*x)

    def Case_D_heatrate(self,M):
        # infinite fin
        return M

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
        f = lambdify(x,FinR.val4else[0],"numpy")

        x1 = 0
        x2 = FinR.val4else[4]
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


        glClearColor(0.2, 0.2, 0 , 0)                                #바탕화면 색깔
        glPushMatrix()
        glTranslatef(0.0, 0.0, -3.0)                                 #시점조정하기...
        self.Draw()
        glPopMatrix()
        glFlush()
 
    def Draw(self):

        def Vertices():                                              #좌표......

            x = np.linspace(-1.5,1.5,200)
            ver= []

            t = FinR.val4else[7]
            L = FinR.val4else[4]

            for a in x:
                ver1 = [a,-0.2]
                ver2 = [a, 0.2]
                ver.append(ver1)
                ver.append(ver2)

            return ver

        def Color():                                                   #색배합 조정하기

            expr = lambdify(self.x,FinR.val4else[0],'numpy')
            x = np.linspace(0,FinR.val4else[4],200)
            T = np.array(expr(x))
            T_avg = np.average(T)                   #평균값
            
            dT = T-T_avg                            # dT= 온도 - 평균 
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

        glBegin(GL_TRIANGLE_STRIP)                              #핀그림

        glColor3fv((253/253,0,0))
        glVertex2fv((-2 ,- 2))
        glColor3fv((253/253,0,0))
        glVertex2fv((-1.5,-2))
        glColor3fv((253/253,0,0))
        glVertex2fv((-2 ,  2))
        glColor3fv((253/253,0,0))
        glVertex2fv((-1.5, 2))

        glEnd()

def Fin_show():
    app = QApplication(sys.argv)
    myWindow = FinR()
    myWindow.show()
    sys.exit(app.exec_())
