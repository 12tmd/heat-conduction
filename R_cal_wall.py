import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np

form_class1 = uic.loadUiType("Rcal4planewall.ui")[0]
form_class2 = uic.loadUiType("Rcal4planewallseries.ui")[0]
form_class3 = uic.loadUiType("Rcal4planewallparallel.ui")[0]


class Rcal4planewall(QMainWindow, form_class1):

    i = 0                                                #button Enable 시키기....
    z = 0

    Rs = np.zeros(5)
    Rp = np.zeros(5)    

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        Seriestextviewer = [self.Series1textviewer,self.Series2textviewer,self.Series3textviewer,
                self.Series4textviewer,self.Series5textviewer]

        Paralleltextviewer = [self.parallel1textviewer,self.parallel2textviewer,
                self.parallel3textviewer,self.parallel4textviewer]      

        Seriesbutton = [self.Series1button, self.Series2button,self.Series3button,
                self.Series4button,self.Series5button]

        parallelbutton =[self.parallelbutton1,self.parallelbutton2,
                self.parallelbutton3,self.parallelbutton4]

        def OpenRcal4planewallseries():                                             #직렬연결 계산UI 열기
            myWindow = Rcal4planewallseries()
            myWindow.show()

        def OpenRcal4planewallparallel():                                           #병렬연결 계산창 열기
            myWindow = Rcal4planewallparallel()
            myWindow.show()
        
        def CallS():
            for a,b in zip(Seriestextviewer,range(5)):
                a.append(str(Rcal4planewall.Rs[b]))

        def CallP():
            for a,b in zip(Paralleltextviewer,range(4)):
                a.append('{0:10.2e}'.format(Rcal4planewall.Rp[b]))

        def Heatcal():

            Q = float(self.Heat.text())

            R = np.sum(Rcal4planewall.Rs) + np.sum(Rcal4planewall.Rp)
            T = Q*R

            self.Totalrviwer.append('{0:10.2e}'.format(R))
            self.Deltat.setText('{0:10.2e}'.format(T))

        for a in Seriesbutton:
            a.clicked.connect(OpenRcal4planewallseries)

        for a in parallelbutton:
            a.clicked.connect(OpenRcal4planewallparallel)

        self.Callseriesbutton.clicked.connect(CallS)
        self.Callparallelbutton.clicked.connect(CallP)

        self.Heatbutton.clicked.connect(Heatcal)

class Rcal4planewallseries(QMainWindow, form_class2):

    i = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ######################################################################################### 값 정리 필요....

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
            self.Combobox1.addItem("{0}".format(a))

        def kvalue():

            index = int(self.Combobox1.currentIndex())
            k = knum[index]   

            return k

        
        ##########################################################################################
        
        self.Combobox1.currentIndexChanged.connect(kvalue)
        
        def Calculate():

            L = float(self.Linput.text())
            A = float(self.Ainput.text())

            k = kvalue()
            ans = "{0:10.2e}".format(L/(k*A))

            self.Browser.append(str(ans))
            Rcal4planewall.Rs[Rcal4planewallseries.i] = ans
            Rcal4planewallseries.i +=1
            
            return ans

        self.Calbutton.clicked.connect(Calculate)

        def apply():
            self.close()

        self.Push1.clicked.connect(apply)


class Rcal4planewallparallel(QMainWindow, form_class3):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #########################################################################

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
    
        #########################################################################

        
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

            return k1

        A = [self.Ainput1,self.Ainput2,self.Ainput3,self.Ainput4,self.Ainput5]
        for a in A:
            a.setText("0")

        View = [self.Routput1,self.Routput2,self.Routput3,self.Routput4,self.Routput5]

        def Calculate():

            L = float(self.Linput.text())
            A = [float(self.Ainput1.text()),float(self.Ainput2.text()),float(self.Ainput3.text()),float(self.Ainput4.text()),float(self.Ainput5.text())]
            k = kvalue()
            ans = []
            Rt = 0

            try :
                for a,b in zip(A,k):
                    ans.append(L/(b*a))
                    Rt += 1/(L/(b*a))
            
            except ZeroDivisionError :
                pass

            for a,b in zip(View,ans):
                a.setText("{0:10.2e}".format(b))

            Rt = 1/Rt
            self.Rtotal.append(str('{0:10.2e}'.format(Rt)))

            Rcal4planewall.Rp[Rcal4planewall.z] = Rt
            Rcal4planewall.z +=1
    
        self.Calbutton.clicked.connect(Calculate)

        def apply():
            self.close()

        self.Closebutton.clicked.connect(apply)


def Rcalw_show():
    app = QApplication(sys.argv)
    myWindow = Rcal4planewall()
    myWindow.show()
    sys.exit(app.exec_())
