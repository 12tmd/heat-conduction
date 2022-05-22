import sys

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

import Transient

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):   

     #레이아웃 정의
        
        layout1 = QHBoxLayout()

        layout2 = QVBoxLayout()
       
        pixmap = QPixmap("그림7.png")
        image1 = QLabel(self)
        image1.setPixmap(pixmap)
        
        form1 = QFormLayout()

        self.T1 = QLineEdit() 
        self.T2 = QLineEdit()
        self.T3 = QLineEdit()
        self.T4 = QLineEdit() 
        self.Ti = QLineEdit()      

        self.T1.setText('100')
        self.T2.setText('200')
        self.T3.setText('300')
        self.T4.setText('400')
        self.Ti.setText('0')

        layout3 = QFormLayout()

        label1 = QLabel( "_______________________ ")
        label2 = QLabel( "_______________________ ")

        self.nodesize = QLineEdit() 
        self.time = QLineEdit()
        self.k = QLineEdit()
        self.specificheat = QLineEdit() 
        self.density = QLineEdit()
        self.X = QLineEdit()
        self.Y = QLineEdit() 
        self.timeinterval = QLineEdit()        

        self.nodesize.setText('1')
        self.time.setText('0.3')
        self.k.setText('80.4')
        self.specificheat.setText('0.41')
        self.density.setText('7.86')
        self.X.setText('40')
        self.Y.setText('40')
        self.timeinterval.setText('1')


        button1 = QPushButton("계산")
        button1.clicked.connect(self.button1Function)
  
      #add
        
        form1.addRow( "T1 :" , self.T1)
        form1.addRow( "T2  :" ,  self.T2)
        form1.addRow( "T3  :" , self.T3)
        form1.addRow( "T4 :" , self.T4)
        form1.addRow( "Ti :" , self.Ti)
    
        layout3.addRow( label1 )
        layout3.addRow( " nodesize(mm) :" , self.nodesize )
        layout3.addRow( " time(s) :" , self.time)
        layout3.addRow( " k(W/m k) :" , self.k )
        layout3.addRow( " specific heat(J/g k) :" , self.specificheat)
        layout3.addRow( " density(g/cm^3) :" , self.density)
        layout3.addRow( " X(mm) :" , self.X)
        layout3.addRow( " Y(mm) :" , self.Y)

        layout3.addRow( " time interval:" , self.timeinterval)

        layout3.addRow( label2 )
        layout3.addRow(button1)

        layout2.addWidget(image1)
        layout2.addLayout(form1)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        

        self.setLayout(layout1)
        self.resize(200, 300)
        self.show()


     #함수정의
    def button1Function(self) :

        length_X = int(self.X.text())
        length_Y = int(self.Y.text())

        Transient.size[0] = length_X
        Transient.size[1] = length_Y

        u_top = float(self.T1.text())
        u_left = float(self.T2.text())
        u_bottom = float(self.T3.text())
        u_right = float(self.T4.text())
        u_inside = float(self.Ti.text())

        Transient.surface[0] = u_top
        Transient.surface[1] = u_right
        Transient.surface[2] = u_bottom
        Transient.surface[3] = u_left
        Transient.surface[4] = u_inside


        k = float(self.k.text())
        density = float(self.density.text())
        specific_heat =float(self.specificheat.text())
        node_size = int(self.nodesize.text())
        Time_input = float(self.time.text())               
        timeinterval = int(self.timeinterval.text())


        Transient.value[0] = k/1000
        Transient.value[1] = density/1000
        Transient.value[2] = specific_heat
        Transient.value[3] = node_size
        Transient.value[4] = Time_input

        alpha = k/density/specific_heat
        delta_t = (node_size ** 2)/(4 * timeinterval * alpha)   #1회 계산당 시간간격.....
        max_iter_time =  round(Time_input/delta_t)              #계산반복  횟수

        print(alpha)
        print(delta_t)
        print(max_iter_time)

        gamma = (alpha * delta_t) / (node_size ** 2)            #계산때 필요한 감마값...

        Transient.value2cal[0] = alpha
        Transient.value2cal[1] = delta_t
        Transient.value2cal[2] = max_iter_time
        Transient.value2cal[3] = gamma

        Transient.Animate_heatmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())


