import sys
import FDM

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):   

     #레이아웃 정의
        
        layout1 = QVBoxLayout()

        layout2 = QHBoxLayout()

        layout7 = QFormLayout()

        pixmap = QPixmap("최종그림파일.png")
        image1 = QLabel(self)
        image1.setPixmap(pixmap)
       
        self.edit_i = QLineEdit()
        self.edit_i.setText("5")
        self.edit_j = QLineEdit()
        self.edit_j.setText("5")

        layout6 = QVBoxLayout()
        self.text1 = QTextBrowser(self)
        self.text2 = QTextBrowser(self)
        self.text3 = QTextBrowser(self)

        label_corner = QLabel("Coner")
        label_surface = QLabel("Surface")
        label_center = QLabel("Center")
       
        layout3 = QHBoxLayout()


        layout4 = QGridLayout()
        label1 = QLabel() 
        label2 = QLabel("표면 1")
        label3 = QLabel("표면 2")
        label4 = QLabel("표면 3")
        label5 = QLabel("표면 4")

        label6 = QLabel("Ts")

        self.label7 = QLineEdit()
        self.label8 = QLineEdit()
        self.label9 = QLineEdit()
        self.label10 = QLineEdit()



        label11 = QLabel("Tair")
        self.label12 = QLineEdit()
        self.label13 = QLineEdit()
        self.label14 = QLineEdit() 
        self.label15 = QLineEdit()


        label16 = QLabel("h")
        self.label17 = QLineEdit()
        self.label18 = QLineEdit()
        self.label19 = QLineEdit() 
        self.label20 = QLineEdit()      



        label21 = QLabel("q") 
        self.label22 = QLineEdit()
        self.label23 = QLineEdit()
        self.label24 = QLineEdit() 
        self.label25 = QLineEdit()   

        layout5 = QFormLayout()
        self.label_k = QLineEdit()
        self.label_k.setText("100")

        self.label_dx = QLineEdit()
        self.label_dx.setText("2")

        self.label_dy = QLineEdit()
        self.label_dy.setText("1")

        Line_edit_all = [self.label7,self.label8,self.label9,self.label10,
        self.label12,self.label13,self.label14,self.label15,
        self.label17,self.label18,self.label19,self.label20,
        self.label22,self.label23,self.label24,self.label25]
  
        for a in Line_edit_all:
            a.setText("0")

        button1 = QPushButton("계산")
        button1.clicked.connect(self.btn_cal)

      #add

        layout7.addRow(image1)
        layout7.addRow( " i:", self.edit_i)
        layout7.addRow( " j:", self.edit_j)

        layout6.addWidget(label_corner)
        layout6.addWidget(self.text1)
        layout6.addWidget(label_surface)
        layout6.addWidget(self.text2)
        layout6.addWidget(label_center)
        layout6.addWidget(self.text3)

        layout5.addRow( " k   :" , self.label_k)
        layout5.addRow( " dx  :" , self.label_dx)
        layout5.addRow( " dy  :" , self.label_dy)
        layout5.addRow(button1)


        layout4.addWidget(label1, 0,0)
        layout4.addWidget(label2, 0,1)
        layout4.addWidget(label3, 0,2)

        layout4.addWidget(label4, 0,3)
        layout4.addWidget(label5, 0,4)
        layout4.addWidget(label6, 1,0)
        layout4.addWidget(self.label7, 1,1)
        layout4.addWidget(self.label8, 1,2)
        layout4.addWidget(self.label9, 1,3)
        layout4.addWidget(self.label10, 1,4)
        layout4.addWidget(label11, 2,0)
        layout4.addWidget(self.label12, 2,1)
        layout4.addWidget(self.label13, 2,2)
        layout4.addWidget(self.label14, 2,3)
        layout4.addWidget(self.label15, 2,4)
        layout4.addWidget(label16, 3,0)
        layout4.addWidget(self.label17, 3,1)
        layout4.addWidget(self.label18, 3,2)
        layout4.addWidget(self.label19, 3,3)
        layout4.addWidget(self.label20, 3,4)
        layout4.addWidget(label21, 4,0)
        layout4.addWidget(self.label22, 4,1)
        layout4.addWidget(self.label23, 4,2)
        layout4.addWidget(self.label24, 4,3)
        layout4.addWidget(self.label25, 4,4)
             
        layout3.addLayout(layout4)
        layout3.addLayout(layout5)

        layout2.addLayout(layout7)
        layout2.addLayout(layout6)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        
        self.setLayout(layout1)
        self.resize(700, 300)
        self.show()

    def btn_cal(self):

        Tem_S = ["Tem_S1","Tem_S2","Tem_S3","Tem_S3"]
        Tem_A = ["Tem_A1","Tem_A2","Tem_A3","Tem_A4"]
        h =     ["h1","h2","h3","h4"]
        q =     ["q1","q2","q3","q4"]

        value = ["dx","dy","k"]
        size = ["i","j"]

        value[0] = self.label_dx.text()
        value[1] = self.label_dy.text()
        value[2] = self.label_k.text()

        size[0] =  int(self.edit_i.text())
        size[1] =  int(self.edit_j.text())

        Tem_S[0] = self.label7.text()
        Tem_A[0] = self.label12.text()
        h[0]= self.label17.text()
        q[0]= self.label22.text()

        Tem_S[1] = self.label8.text()
        Tem_A[1] = self.label13.text()
        h[1]= self.label18.text()
        q[1]= self.label23.text()

        Tem_S[2] = self.label9.text()
        Tem_A[2] = self.label14.text()
        h[2]= self.label19.text()
        q[2]= self.label24.text()

        Tem_S[3] = self.label10.text()
        Tem_A[3] = self.label15.text()

        h[3]= self.label20.text()
        q[3]= self.label25.text()


        for a,b in zip(Tem_S,range(4)):

            if a == '0':
                FDM.Tem_S[b] = "x"

            else:
                FDM.Tem_S[b] = float(a)

        for a,b in zip(Tem_A,range(4)):

            if a == '0':
                FDM.Tem_A[b] = "x"

            else:
                FDM.Tem_A[b] = float(a)

        for a,b in zip(h,range(4)):

            if a == '0':
                FDM.h[b] = "x"

            else:
                FDM.h[b] = float(a)

        for a,b in zip(q,range(4)):
            if a == '0':

                FDM.q[b] = "x"

            else:
                FDM.q[b] = float(a)


        for a,b in zip(value,range(3)):
            FDM.value[b] = float(a)

        FDM.Ploting(size[0],size[1])
        EQ4view = FDM.EQ4view[0]

        EQ4coner = [EQ4view[0,0],EQ4view[0,size[1]-1],EQ4view[size[0]-1,size[1]-1],EQ4view[size[0]-1,0]]

        self.text1.clear()
        self.text2.clear()
        for a in EQ4coner:
            self.text1.append("{0} \n".format(a))

        EQ4surface = [EQ4view[0,round(size[1]/2)],EQ4view[round(size[0]/2),round(size[1]-1)],EQ4view[round(size[0]-1),round(size[1]/2)],EQ4view[round(size[0]/2),0]] 
        for a in EQ4surface:
            self.text2.append("{0} \n".format(a))       

        self.text3.append(" T = (Tn + Tw + Ts + Te)/4 " )


def Win_show():

    app = QApplication(sys.argv)
    w = Main()
    w.show()
    app.exec()

Win_show()