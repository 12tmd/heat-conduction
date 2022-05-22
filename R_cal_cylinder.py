import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np

form_class4 = uic.loadUiType("R4.ui")[0]

class R4(QMainWindow, form_class4):

    def __init__(self):

        super().__init__()
        self.setupUi(self)
        

#%%
#Combobox setting....

        Combolist = [self.comboBox_1,self.comboBox_2,self.comboBox_3,self.comboBox_4,self.comboBox_5]

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

        for a in Combolist:
            for c in k:
                a.addItem("{0}".format(c))
        
        def kvalue():
                
            k = [0,0,0,0,0]

            k[0] = self.comboBox_1.currentIndex()
            k[1] = self.comboBox_2.currentIndex()
            k[2] = self.comboBox_3.currentIndex()
            k[3] = self.comboBox_4.currentIndex()
            k[4] = self.comboBox_5.currentIndex()       #결과가 index로 나옴....

            k1 = [0,0,0,0,0]
            for a in range(5):
                k1[a] = knum[k[a]]

            return np.array(k1)


#%% for문을 위해서 list로 정리한것

        r1 = [self.r1input1,self.r1input2,self.r1input3,
                self.r1input4,self.r1input5]
                
        r2 = [self.r2input1,self.r2input2,self.r2input3,
                self.r2input4,self.r2input5]

        L = [self.Linput1,self.Linput2,self.Linput3,
                self.Linput4,self.Linput5]

        R = [self.Rsol1,self.Rsol2,self.Rsol3,self.Rsol4,self.Rsol5]

        for a,b,c in zip(r1,r2,L):
           a.setText("0")
           b.setText("0")
           c.setText("0")

#%% Calbutton
        def Calcylinder():
            
            ri = np.zeros(5)                                        #계산을 위한 array생성
            ro = np.zeros(5)
            L1 = np.zeros(5)

            for a,b,c,d in zip(r1,r2,L,range(5)):                   #array에 값 대입
                ri[d] = float(a.text())
                ro[d] = float(b.text())
                L1[d] = float(c.text())

            try:                                                    
                reslut = np.log(ro/ri)/(2*np.pi*L1*kvalue())        #계산식

            except ZeroDivisionError:
                pass

            reslut[np.isnan(reslut)] = 0                            #nan결과를 0으로
            reslut[np.isinf(reslut)] = 0                            #inf결과를 0으로

            
            for a,b in zip(R,reslut):
                a.setText('{0:10.2e}'.format(b))
            
            rtotal = np.sum(reslut)
            self.Rtotal.setText('{0:10.2e}'.format(rtotal))

#%%대류도 일어날때 계산하기....

            try:

                hi = float(self.Innerh.text())
                ho = float(self.Outerh.text())
            
                ri = float(self.Innerr.text())/1000
                ro = float(self.Outerr.text())/1000

                Li = float(self.InnerL.text())
                Lo = float(self.OuterL.text())

            except ValueError:
                hi,ho,ri,ro,Li,Lo = 0,0,0,0,0,0
                pass

            try:
                finalr = rtotal + 1/(2*np.pi*hi*ri*Li) + 1/(2*np.pi*ho*ro*Lo)

            except ZeroDivisionError:

                finalr = rtotal
                pass

            self.Rtotalair.setText('{0:10.2e}'.format(finalr))

        self.Closebutton.clicked.connect(Calcylinder)

#%%
def Rcalc_show():
    app = QApplication(sys.argv)
    myWindow = R4()
    myWindow.show()
    sys.exit(app.exec_())
