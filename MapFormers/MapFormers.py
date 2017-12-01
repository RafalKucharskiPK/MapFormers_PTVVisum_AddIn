"""
 _   _____  
| | /___  \     Intelligent Infrastructure
| |  ___| |     script created by: Rafal Kucharski, and Sebastian Niemczyk
| | /  ___/     16/08/2011
| | | |___      info: info@intelligent-infrastructure.eu
|_| |_____|     Copyright (c) Intelligent Infrastructure 2011 

references: ExNumerus.blogspot.com + QHull www.qhull.org
=====================
Dependencies:
 
1. OpenLayers (www.openlayers.com)
2. PyQt4 by riverside

=====================
 
==========================
End-User License Agreement:
===========================
This software is created by Intelligent-Infrastructure - Rafal Kucharski (i2) Krakow Polska, who also owns the copyrights. 

By using this software you agree with terms stated below:

1.You can use the software only if You bought it from intelligent-infrastructure, or got an written permission of i2 to do so.
2.You can use and modify the software code, as long as you don't sell it's parts commercially.
3.You cannot publish and/or show any parts of the code to third-party users without written permission of i2 
4.If You want to sell the software created by modifying this software, you need to contact with i2 and agree conditions
5.This is one user copy, you cannot use it on multiple computers without written permission to do so
6.You cannot modify this statement
7.You can freely analyze the code, and propose any changes
8. After period defined by special i2 statement this software becomes freeware, so that it can be freely downloaded and/or modified.

sept 2011, Krakow Poland
"""

try:    
    import sys,os    
except:
    import win32api,os        
    win32api.MessageBox(0, "Welcome! \n\nThere seems to be a problem with your python package. \n \n To use MapFormers you need to reinstall your python package \n(best way is via Visum install package)" , 'Map Formers by intelligent infrastructure')


def Get_Paths():
    
    '''
    Create paths to working folder, html and png file
    in standalone version script opens visum file with selected path via COM
    '''
    Paths={}
    Paths["MainVisum"] = Visum.GetWorkingFolder()
    Paths["ScriptFolder"] = Paths["MainVisum"] + "\\AddIns\\intelligent-infrastructure\\MapFormers"
    Visum.SetPath(48, Paths["ScriptFolder"])
    Paths["Html"] =Paths["ScriptFolder"] + "\\template.html"
    #Paths["Screenshot"] = Paths["ScriptFolder"] + "\\Screenshot.png"
    Paths["Screenshot"] = "E:" + "\\Screenshot.png"
    Paths["Logo"]=Paths["ScriptFolder"] + "\\help\\i2_logo.png"
    Paths["Icon"]=Paths["ScriptFolder"] + "\\help\\i2_icon.png"
    Paths["Help"]=Paths["ScriptFolder"] + "\\Help\\help.html"
    Paths["PyQtinstall"]=Paths["ScriptFolder"]+"\\PyQt-Py2.5-x86-gpl-4.8.5-1.exe"
    
    return Paths

try:
    Visum    
except:
    import win32com.client
    Visum=win32com.client.Dispatch("Visum.Visum.13")
    Visum.LoadVersion("E:/Krakow.ver")
    #Visum.LoadVersion("D:/B.ver")


Paths=Get_Paths()
 



        
try:    
    import PyQt4.QtCore
    from PyQt4 import QtCore
    from PyQt4 import QtGui    
    from PyQt4.QtCore import SIGNAL, QUrl, Qt, QEventLoop, QCoreApplication,QString
    from PyQt4.QtGui import  QMainWindow,QSizePolicy, QFrame, QGroupBox, QGridLayout, QStackedWidget, QRadioButton, QVBoxLayout, QImage, QPainter, QApplication, QWidget, QPushButton, QCheckBox, qApp, QComboBox, QLabel, QDoubleSpinBox, QProgressBar, QSlider, QDesktopWidget, QMessageBox
    from PyQt4.QtWebKit import QWebPage, QWebSettings, QWebView  
    
except:    
    import win32api,os        
    win32api.MessageBox(0, "Welcome! \n To use MapFormers you need to install PyQt4 \n please press OK to install external packages. \n Target folder should be your python path" , 'Map Formers by intelligent infrastructure')
    os.startfile(Paths["PyQtinstall"])
        
#import PyQt4.QtCore
#from PyQt4 import QtCore
#from PyQt4 import QtGui    
#from PyQt4.QtCore import SIGNAL, QUrl, Qt, QEventLoop, QCoreApplication,QString
#from PyQt4.QtGui import  QMainWindow,QSizePolicy, QFrame, QGroupBox, QGridLayout, QStackedWidget, QRadioButton, QVBoxLayout, QImage, QPainter, QApplication, QWidget, QPushButton, QCheckBox, qApp, QComboBox, QLabel, QDoubleSpinBox, QProgressBar, QSlider, QDesktopWidget, QMessageBox
#from PyQt4.QtWebKit import QWebPage, QWebSettings, QWebView
    

def Init(path=None):
        import win32com.client        
        Visum=win32com.client.Dispatch('Visum.Visum')
        if path!=None: Visum.LoadVersion(path)
        return Visum

try: 
    Visum
except: 
    Visum=Init()

def CheckAttr(o,attr):
       return attr in [e.Code for e in o.Attributes.GetAll]

class GUI(QtGui.QMainWindow):
    
    
    def __init__(self,win_parent = None):               
       
        '''
        Initialize main window
        '''
        QtGui.QMainWindow.__init__(self, win_parent)
        self.setWindowTitle('MapFormers: Get nodes geolocations')
        self.setGeometry(250, 200, 714, 491)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.WindowSystemMenuHint)
        self.setWindowIcon(QtGui.QIcon(Paths["Icon"]))        
        self.Elem_init()
        self.InitialValues()
        self.setGeometry_()
        self.InitialValues()
        self.setLabels()
        self.SetLayouts()
        
        
        if not CheckAttr(Visum.Net.Nodes,'Google_X'):
            Visum.Net.Nodes.AddUserDefinedAttribute('Google_X', 'Google_X', 'Google_X', 2,10) #else create UDAs
        if not CheckAttr(Visum.Net.Nodes,'Google_Y'):
            Visum.Net.Nodes.AddUserDefinedAttribute('Google_Y', 'Google_Y', 'Google_Y', 2,10) #else create UDAs

            
        self.connect(self.SB_NodeNumber,QtCore.SIGNAL('editingFinished()'),self.MakeVisScreenshot)
        self.connect(self.DSB_Zoom,QtCore.SIGNAL('editingFinished()'),self.MakeVisScreenshot)
        

        self.connect(self.SB_NodeNumber,QtCore.SIGNAL('editingFinished()'),self.UpdateGeoPos)
        self.connect(self.SB_NodeNumber,QtCore.SIGNAL('valueChanged()'),self.UpdateGeoPos)  
        
        self.connect(self.B_ImportPos,QtCore.SIGNAL('clicked()'),self.ImportGeoPosition)
        
        self.connect(self.B_Next,QtCore.SIGNAL('clicked()'),self.NextWindow)
        self.connect(self.B_Back,QtCore.SIGNAL('clicked()'),self.BackWindow)
        
        self.connect(self.B_Calculate,QtCore.SIGNAL('clicked()'),self.Transform)
        self.connect(self.RB_prj,QtCore.SIGNAL('clicked()'),self.RBPrjClick)
        self.connect(self.RB_regression,QtCore.SIGNAL('clicked()'),self.RBRegClick)
        self.connect(self.RB_partiall,QtCore.SIGNAL('clicked()'),self.RBParClick)
        
        self.connect(self.B_Cancel, QtCore.SIGNAL('clicked()'),self.closeEvent)
        self.connect(self.B_Cancel_T2, QtCore.SIGNAL('clicked()'),self.closeEvent)
        
        self.connect(self.B_Help, QtCore.SIGNAL('clicked()'),self.openHelp)
        self.connect(self.B_Help_T2, QtCore.SIGNAL('clicked()'),self.openHelp)
          
    def Elem_init(self):
        
        self.SW_Main=QStackedWidget(self)
        
        self.SW_Tab1=QWidget(self.SW_Main)
        self.SW_Tab2=QWidget(self.SW_Main)
        
        self.GB_LeftSide=QGroupBox(self.SW_Tab1)
        self.GB_RightSide=QGroupBox(self.SW_Tab1)
        self.BottomWidget=QtGui.QWidget(self.SW_Tab1)
        
        self.Wid_LayVer_LeftSide = QtGui.QWidget(self.GB_LeftSide)
        self.L_ImageLeft = QtGui.QLabel(self.Wid_LayVer_LeftSide)
        
        self.GB_Options_LB=QtGui.QGroupBox(self.GB_LeftSide)
        
        self.L_NodeNumber=QtGui.QLabel(self.GB_Options_LB)
        self.L_zoom=QtGui.QLabel(self.GB_Options_LB)
        self.SB_NodeNumber=QtGui.QSpinBox(self.GB_Options_LB)
        self.DSB_Zoom=QtGui.QDoubleSpinBox(self.GB_Options_LB)
        self.L_GeoT=QtGui.QLabel(self.GB_Options_LB)
        self.L_GeoPos=QtGui.QLabel(self.GB_Options_LB)
        
        self.ImageLeft = QtGui.QPixmap(Paths["Screenshot"])

        self.Wid_LayVer_RightSide = QtGui.QWidget(self.GB_RightSide)
        
        self.B_ImportPos=QtGui.QPushButton(self.Wid_LayVer_RightSide)
        self.Web = QWebView(self.Wid_LayVer_RightSide) 
        
        self.B_Help=QtGui.QPushButton(self.BottomWidget)
        self.B_Next=QtGui.QPushButton(self.BottomWidget)
        self.B_Cancel=QtGui.QPushButton(self.BottomWidget)
        self.L_ImageLogo = QtGui.QLabel(self.BottomWidget)
        
        self.ImageLogo = QtGui.QPixmap(Paths["Logo"])
        
        self.BG_Transform=QtGui.QGroupBox(self.SW_Tab2)
        self.BottomWidget_T2=QtGui.QWidget(self.SW_Tab2)
        
        

        self.GB_Opt_T2=QtGui.QGroupBox(self.SW_Tab2)
        
        self.SB_NodeNumber_T2=QtGui.QSpinBox(self.GB_Opt_T2)
        self.DSB_Factor_T2=QtGui.QDoubleSpinBox(self.GB_Opt_T2)
        self.L_Factor_T2=QtGui.QLabel(self.GB_Opt_T2)
        self.L_NodeNumber_T2=QtGui.QLabel(self.GB_Opt_T2)
    
              
        self.RB_prj=QRadioButton(self.BG_Transform)
        self.RB_regression=QRadioButton(self.BG_Transform)
        self.RB_partiall=QRadioButton(self.BG_Transform)     
        
        self.B_Help_T2=QtGui.QPushButton(self.BottomWidget_T2)
        self.B_Back=QtGui.QPushButton(self.BottomWidget_T2)
        self.B_Calculate=QtGui.QPushButton(self.BottomWidget_T2)
        self.B_Cancel_T2=QtGui.QPushButton(self.BottomWidget_T2)
        self.L_ImageLogo_T2 = QtGui.QLabel(self.BottomWidget_T2)
        
        self.LayGrid_Main=QtGui.QGridLayout() 
        self.LayVer_LeftSide=QtGui.QVBoxLayout()
        self.LayVer_RightSide=QtGui.QVBoxLayout()
        self.LayGrid_Bottom = QtGui.QGridLayout()
        self.LayGrid_Opt = QtGui.QGridLayout() 
        self.LayVer_Main_T2=QtGui.QVBoxLayout()
        self.Lay_Transform=QVBoxLayout()
        self.LayGrid_Bottom_T2 = QtGui.QGridLayout()
        self.BL_Lay_Transform=QtGui.QVBoxLayout()
        
        self.LayHor_Opt_T2=QtGui.QHBoxLayout()
        
        self.V_NodeFilter=Visum.Filters.NodeFilter()
        self.V_LinkFilter=Visum.Filters.LinkFilter()
    
    def setLabels(self):
        
        self.GB_LeftSide.setTitle("Visum Node")
        self.GB_RightSide.setTitle("Map reference")
        self.L_NodeNumber.setText("Node number:")
        self.L_zoom.setText("Zoom:")
        self.L_GeoT.setText("Current node's geoposition:")
        self.L_GeoPos.setText("no reference")
        self.B_ImportPos.setText("Save reference")
        self.B_Help.setText("Help")
        self.B_Next.setText("Next ->")
        self.B_Cancel.setText("Cancel")
        self.RB_prj.setText("Option 1: Transform network by means of .prj file.\n (This option will worn only if network scale is linear (scale for X axis = scale for Y axis) - \n in most cases it will not work for Your network.")
        self.RB_regression.setText("Option 2: Transform network by means of linear regression calibrated with input reference data. \n Specify confidence factor [0-1] for input data in the box below - default value is 0.8")
        self.RB_partiall.setText("Option 3: Adjust only active part of the network (nodes, and links) based on reference node from box below")
        self.BG_Transform.setTitle("Transform network")
        self.B_Help_T2.setText("Help")
        self.B_Back.setText("<- Back")
        self.B_Calculate.setText("Calculate")
        self.B_Cancel_T2.setText("Cancel")
        self.L_Factor_T2.setText("Confidence factor:")
        self.L_NodeNumber_T2.setText("Node number:")
        
    def setGeometry_(self):
        
        self.B_Help.setFixedSize(85,23)     
        self.B_Next.setFixedSize(85,23)
        self.B_Cancel.setFixedSize(85,23)
        self.L_ImageLogo.setFixedSize(200,32)
        self.B_Help_T2.setFixedSize(85,23)
        self.B_Back.setFixedSize(85,23)     
        self.B_Calculate.setFixedSize(85,23)   
        self.B_Cancel_T2.setFixedSize(85,23)
        self.L_ImageLogo_T2.setFixedSize(200,32)
        
        self.L_ImageLeft.setMinimumSize(300, 300)
        self.L_ImageLeft.setBaseSize(350, 350)
        self.Web.setContentsMargins(0, 0, 0, 0)
        self.Web.setMinimumSize(350, 350)
        self.Web.setBaseSize(375, 375)
        
    def InitialValues(self):
        
        self.setCentralWidget(self.SW_Main)

        self.Web.page().mainFrame().load(QUrl(Paths["Html"])) 
        self.Web.page().setViewportSize(self.Web.page().mainFrame().contentsSize())  
        
        NodeIter=Visum.Net.Nodes.Iterator
        try:
            FirstActiveNode=NodeIter.Item.AttValue("No")
        except: 
            Visum.Net.AddNode(1,1,1)
            NodeIter=Visum.Net.Nodes.Iterator
            FirstActiveNode=NodeIter.Item.AttValue("No")
        
        Visum.Graphic.Autozoom(Visum.Net.Nodes.ItemByKey(FirstActiveNode))
        self.V_NodeFilter.Init()
        self.V_NodeFilter.AddCondition("OP_NONE", False, "NO","EqualVal",FirstActiveNode)
        self.V_NodeFilter.UseFilter=True

        self.V_LinkFilter.Init()
        self.V_LinkFilter.AddCondition("OP_NONE",False,"ToNodeNo","EqualVal",FirstActiveNode)
        self.V_LinkFilter.UseFilter=True

        Visum.Graphic.Screenshot(Paths["Screenshot"])
        Screenshot=QtGui.QPixmap(Paths["Screenshot"])
        
        self.SB_NodeNumber.setValue(FirstActiveNode)
        self.SB_NodeNumber.setMaximum(1000000000)
        
        self.SB_NodeNumber_T2.setValue(FirstActiveNode)
        self.SB_NodeNumber_T2.setMaximum(1000000000)
        
        self.DSB_Factor_T2.setValue(0.8)
        self.DSB_Factor_T2.setMaximum(1)
        
        
        self.DSB_Zoom.setValue(1)
        self.DSB_Zoom.setSingleStep(0.5)
        self.DSB_Zoom.setMaximum(1000000)   
        
        self.L_ImageLeft.setPixmap(Screenshot)
        self.L_ImageLeft.setScaledContents(True)
        
        self.ImageLogo.scaled(200, 23, Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        #self.L_ImageLogo.setScaledContents(True)
        self.L_ImageLogo.setPixmap(self.ImageLogo)
        
        self.L_ImageLogo_T2.setScaledContents(True)
        self.L_ImageLogo_T2.setPixmap(self.ImageLogo)
        
        self.L_ImageLeft.show()
        self.RBRegClick()
        
        self.RB_regression.setChecked(True)
            
                
    def SetLayouts(self):
        
        self.L_NodeNumber.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.L_zoom.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.SB_NodeNumber.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.DSB_Zoom.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.L_GeoT.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.L_GeoPos.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.L_ImageLogo_T2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.L_ImageLogo.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        
        self.L_NodeNumber_T2.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.SB_NodeNumber_T2.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.L_Factor_T2.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.DSB_Factor_T2.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        
        self.GB_Options_LB.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.BottomWidget_T2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.GB_Opt_T2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        
        self.LayGrid_Opt.addWidget(self.L_NodeNumber, 1, 0, 1, 1)
        self.LayGrid_Opt.addWidget(self.L_zoom, 1, 2, 1, 1)
        self.LayGrid_Opt.addWidget(self.SB_NodeNumber,1,1,1,1)
        self.LayGrid_Opt.addWidget(self.DSB_Zoom,1,3,1,1)
        self.LayGrid_Opt.addWidget(self.L_GeoT,0,0,1,2)
        self.LayGrid_Opt.addWidget(self.L_GeoPos,0,2,1,2)
        self.LayGrid_Opt.setVerticalSpacing(20)
        
        self.LayVer_LeftSide.addWidget(self.L_ImageLeft)
        self.LayVer_LeftSide.addWidget(self.GB_Options_LB)
        self.LayVer_LeftSide.setSpacing(20)
        
        self.LayVer_RightSide.addWidget(self.Web)
        self.LayVer_RightSide.addWidget(self.B_ImportPos)
        self.LayVer_RightSide.setSpacing(20)
        
        self.LayGrid_Bottom.addWidget(self.B_Help,0,0,1,1)
        self.LayGrid_Bottom.addWidget(QWidget(),0,1,1,1)
        self.LayGrid_Bottom.addWidget(self.L_ImageLogo,0,2,1,1)
        self.LayGrid_Bottom.addWidget(QWidget(),0,3,1,1)
        self.LayGrid_Bottom.addWidget(self.B_Next,0,4,1,1)
        self.LayGrid_Bottom.addWidget(self.B_Cancel,0,5,1,1)
        
        self.LayGrid_Main.addWidget(self.GB_LeftSide,0,0,1,2)
        self.LayGrid_Main.addWidget(self.GB_RightSide,0,2,1,4)
        self.LayGrid_Main.addWidget(self.BottomWidget,1,0,1,6)
        
        self.BL_Lay_Transform.addWidget(self.RB_prj)
        self.BL_Lay_Transform.addWidget(self.RB_regression)
        self.BL_Lay_Transform.addWidget(self.RB_partiall)
        
        self.LayGrid_Bottom_T2.addWidget(self.B_Help_T2,0,0,1,1)
        self.LayGrid_Bottom_T2.addWidget(QWidget(),0,1,1,1)
        self.LayGrid_Bottom_T2.addWidget(self.L_ImageLogo_T2,0,2,1,1)
        self.LayGrid_Bottom_T2.addWidget(QWidget(),0,3,1,1)
        self.LayGrid_Bottom_T2.addWidget(self.B_Back,0,4,1,1)
        self.LayGrid_Bottom_T2.addWidget(self.B_Calculate,0,5,1,1)
        self.LayGrid_Bottom_T2.addWidget(self.B_Cancel_T2,0,6,1,1)
        
        
        self.LayHor_Opt_T2.addWidget(self.L_NodeNumber_T2)
        self.LayHor_Opt_T2.addWidget(self.SB_NodeNumber_T2)
        self.LayHor_Opt_T2.addWidget(self.L_Factor_T2)
        self.LayHor_Opt_T2.addWidget(self.DSB_Factor_T2)
        self.LayHor_Opt_T2.addWidget(QWidget())
        
        self.LayVer_Main_T2.addWidget(self.BG_Transform)
        self.LayVer_Main_T2.addWidget(self.GB_Opt_T2)
        self.LayVer_Main_T2.addWidget(QWidget())
        self.LayVer_Main_T2.addWidget(self.BottomWidget_T2)
        
        self.GB_Opt_T2.setLayout(self.LayHor_Opt_T2)
        
        self.SW_Main.addWidget(self.SW_Tab1)
        self.SW_Main.addWidget(self.SW_Tab2)
        
        self.GB_LeftSide.setLayout(self.LayVer_LeftSide)
        self.GB_RightSide.setLayout(self.LayVer_RightSide)   
        self.GB_Options_LB.setLayout(self.LayGrid_Opt)         
        self.BottomWidget.setLayout(self.LayGrid_Bottom)  
        self.SW_Tab1.setLayout(self.LayGrid_Main)     
        self.BG_Transform.setLayout(self.BL_Lay_Transform)       
        self.BottomWidget_T2.setLayout(self.LayGrid_Bottom_T2)    
        self.SW_Tab2.setLayout(self.LayVer_Main_T2)
    
 
        
    def RBPrjClick(self):
        self.DSB_Factor_T2.setDisabled(True)
        self.SB_NodeNumber_T2.setDisabled(True)
        
    def RBRegClick(self):
        self.DSB_Factor_T2.setEnabled(True)
        self.SB_NodeNumber_T2.setDisabled(True)

    def RBParClick(self):
        self.DSB_Factor_T2.setDisabled(True)
        self.SB_NodeNumber_T2.setEnabled(True)
    
 
    
    def NextWindow(self):
        self.SW_Main.setCurrentIndex(1)
        self.setWindowTitle('MapFormers: Transform network') #dodanie filtra na nodes - Google_X>0
        self.V_NodeFilter.Init()
        self.V_NodeFilter.AddCondition("OP_NONE", False, "Google_X",3,0)
        self.V_NodeFilter.UseFilter=True
    
    def BackWindow(self):
        self.SW_Main.setCurrentIndex(0)
        self.setWindowTitle('MapFormers: Get nodes geolocations')


    def UpdateGeoPos(self):
        '''
        Script updates label displaying node's geolocation
        '''
        
        NodeNumber=self.SB_NodeNumber.value()
        try:

            xf=Visum.Net.Nodes.ItemByKey(NodeNumber).AttValue("Google_X")
            x=QString()
            x.setNum(xf,'g',5)
            yf=Visum.Net.Nodes.ItemByKey(NodeNumber).AttValue("Google_Y")
            y=QString()
            y.setNum(yf,'g',5)
            if (xf==0 and yf==0):
                self.Web.page().mainFrame().evaluateJavaScript("removemarkers();")
                self.L_GeoPos.setText("no reference")
            else:
                self.L_GeoPos.setText("x: "+x+" N"+" y: "+y+" E")
                self.Web.page().mainFrame().evaluateJavaScript("Gx = %f; Gy = %f;" % (xf, yf))
                self.Web.page().mainFrame().evaluateJavaScript("markerf();")
        
        except:
            self.L_GeoPos.setText("node does not exist")



            
    def ImportGeoPosition(self):
        '''        
        evaluate JavaScript to return previously selected geographical position in OpenLayers WebWidget
        '''
        NodeNumber=self.SB_NodeNumber.value()
        try: 
            Visum.Net.Nodes.GetMultiAttValues('Google_X')  #check if UDAs exists
        except:    
            Visum.Net.Nodes.AddUserDefinedAttribute('Google_X', 'Google_X', 'Google_X', 2,10) #else create UDAs
            Visum.Net.Nodes.AddUserDefinedAttribute('Google_Y', 'Google_Y', 'Google_Y', 2,10)

        Visum.Net.Nodes.ItemByKey(NodeNumber).SetAttValue("Google_X",self.Web.page().mainFrame().evaluateJavaScript("returnposx();").toReal()[0]) # w pliku html trzeba sie upewnic, ze to zawsze bedzie wspolrzedna lon/lat ! ! ! czasami osm samo zmienia na Projected Coordinate System (czyli wartosci okolo miliona, tak nie moze byc, bo nigdy nie dojdziemy do ladu!zawsze musza byc lon/lat
        Visum.Net.Nodes.ItemByKey(NodeNumber).SetAttValue("Google_Y",self.Web.page().mainFrame().evaluateJavaScript("returnposy();").toReal()[0])
        self.UpdateGeoPos()

   
    def Transform(self):
        
        type=[self.RB_prj.isChecked(),False,self.RB_regression.isChecked(),self.RB_partiall.isChecked()]        
        
        nodeno=self.SB_NodeNumber_T2.value()
        factor=self.DSB_Factor_T2.value()
        
        
        def rescale(scaleX,scaleY,deltaX,deltaY,activeOnly):    
            
            def link_iter():
                
                    def New_WKT(WKT,scaleX,scaleY,deltaX,deltaY):
                            
                            WKT=str(WKT[11:-1])
                            WKT=WKT.split(',')
                            for i in range(len(WKT)):
                                WKT[i]=WKT[i].split(' ')
                            WKT=[[i for i in el] for el in WKT]
                            del WKT[0]
                            del WKT[-1]
                            Mtx=[[ scaleX*float(el[0])+deltaX, scaleY*float(el[1])+deltaY ] for el in WKT]            
                            
                            Nowy=[[ float(el[0]), float(el[1]) ] for el in Mtx]
                            Nowy=', '.join([str(x) for x in Nowy])
                            Nowy=Nowy.replace('],','www')
                            Nowy=Nowy.replace(',','')
                            Nowy=Nowy.replace('www',',')
                            Nowy=Nowy.replace('[','')
                            Nowy=Nowy.replace(']','')
                            Nowy='LINESTRING('+Nowy+')'                    
                            return Nowy                
                
                    Container=Visum.Net.Links
                    WKTs=Container.GetMultiAttValues('WKTPOLY',activeOnly)           
                    New_WKTs=[]            
                    for i in range(len(WKTs)):                                  
                            New_WKTs.append((WKTs[i][0],New_WKT(WKTs[i][1],scaleX,scaleY,deltaX,deltaY)))                
                    return tuple(New_WKTs)    
                
            def iter(Container):
                Xy=Container.GetMultiAttValues('XCoord',activeOnly)
                Yy=Container.GetMultiAttValues('YCoord',activeOnly)
                New_Xy=[]
                New_Yy=[]
                for i in range(len(Xy)):
                    New_Xy.append((Xy[i][0],scaleX*Xy[i][1]+deltaX))
                    New_Yy.append((Yy[i][0],scaleY*Yy[i][1]+deltaY))
                return tuple(New_Xy),tuple(New_Yy)     
                Container.SetMultiAttValues('XCoord',tuple(New_Xy))        
                Container.SetMultiAttValues('YCoord',tuple(New_Yy))
                
                
                
            Node_X,Node_Y=iter(Visum.Net.Nodes)
            New_WKTs=link_iter()
            Zone_X,Zone_Y=iter(Visum.Net.Zones) 
            #Visum.Graphic.ShowMinimized()
            Visum.Net.Nodes.SetMultiAttValues('XCoord',Node_X)        
            Visum.Net.Nodes.SetMultiAttValues('YCoord',Node_Y)    
            try: Visum.Net.Links.SetMultiAttValues('WKTPOLY',New_WKTs)
            except: pass
            try:
                Visum.Net.Zones.SetMultiAttValues('XCoord',Zone_X)        
                Visum.Net.Zones.SetMultiAttValues('YCoord',Zone_Y)
            except: pass
         
        def get_wgs(X): #transform google lon lat to X,Y
        
            from pyproj import Proj
            
            pr_tm = Proj('+proj=merc +lat_0=0 +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs') 
            
            x_latlong = X[0]
            y_latlong = X[1]
        
            x_tm, y_tm = pr_tm(X[0], X[1]) 
        
            return x_tm,y_tm
        
        def set_Visum_projection(false_easting,false_northing,scale):      
          scale=1/float(scale) #""" reciprocal of scale  correct effect """
          Visum_Projection=u'PROJCS["Mapformers",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["GRS_1980",6378137.0,298.257223562]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Mercator"],PARAMETER["False_Easting",'+str(false_easting)+' ],PARAMETER["False_Northing",'+str(false_northing)+' ],PARAMETER["Central_Meridian",0],PARAMETER["Standard_Parallel_1",0],UNIT["Meter",'+str(scale)+']]'
          Visum.Net.NetParameters.SetProjection(Visum_Projection, True)
        
        def get_coords():    
            Visum_X=Visum.Net.Nodes.GetMultiAttValues('XCoord',True)
            Visum_X=[el[1] for el in Visum_X]        
            Visum_Y=Visum.Net.Nodes.GetMultiAttValues('YCoord',True)
            Visum_Y=[el[1] for el in Visum_Y]
            Google_X=Visum.Net.Nodes.GetMultiAttValues('Google_X',True)
            Google_X=[el[1] for el in Google_X]
            Google_Y=Visum.Net.Nodes.GetMultiAttValues('Google_Y',True)
            Google_Y=[el[1] for el in Google_Y] 
            
            #if Google_X[0]<200:
            #    for i in range(len(Google_X)):
            #        point=[Google_X[i],Google_Y[i]]
            #        [Google_X[i],Google_Y[i]]=get_wgs(point)
                
                
                
        
            return Visum_X,Visum_Y,Google_X,Google_Y   
        
        def linreg(Visum_,Google_):
            try:
                numpy        
            except:
                import numpy as np
                
            (scale,delta) = np.polyfit(Visum_,Google_,1)
            nGoogle_=np.polyval([scale,delta],Visum_)
            err=(sum((nGoogle_-Google_)**2)/len(Visum_))**.5        
            return scale,delta,err
        
        def cleaned_linreg(Visum_,Google_,cut_factor):            
            try:
                numpy        
            except:
                import numpy as np
                
            errs=[]            
            cut_factor=min((max(cut_factor,.1)),1)        
            range_=range(max(1,int(len(Google_)*cut_factor)))
            for j in range_:
                (scale,delta) = np.polyfit(Visum_,Google_,1)
                nGoogle_=np.polyval([scale,delta],Visum_)
                err=[(nGoogle_[i]-Google_[i])**2 for i in range(len(nGoogle_))]
                errs.append((sum((nGoogle_-Google_)**2)/len(Visum_))**.5)        
                max_err=err.index(max(err))    
                Visum_.remove(Visum_[max_err])
                Google_.remove(Google_[max_err])
                
            return scale,delta,errs
        
        def dist(X,Y):        
            return ((X[0]-X[1])**2+(Y[0]-Y[1])**2)**.5
            
        def do_projection(Visum_X,Visum_Y,Google_X,Google_Y):
                dist_Visum=dist(Visum_X,Visum_Y) #"""calculate distance in Visum, and real distance in Google"""
                dist_Google=dist(Google_X,Google_Y)
                scale=dist_Google/dist_Visum       
                set_Visum_projection(0,0,1) #"""first set base projection with scale =1"""
                set_Visum_projection(0,0,scale) #"""now adjust the scale"""        
                Visum_X=Visum.Net.Nodes.GetMultiAttValues('XCoord',True)
                Visum_X=[el[1] for el in Visum_X]
                Visum_Y=Visum.Net.Nodes.GetMultiAttValues('YCoord',True)
                Visum_Y=[el[1] for el in Visum_Y] #"""get new rescaled coords"""   
                delta_X= Google_X[0]-Visum_X[0]
                delta_Y= Google_Y[0]-Visum_Y[0]
                set_Visum_projection(0,0,1) #"""first set base projection with scale = 1"""
                set_Visum_projection(0,0,scale) #"""now adjust the scale"""    
                set_Visum_projection(0,0,1) #"""now set bas projection one more time"""
                set_Visum_projection(delta_X,delta_Y,scale) #"""and go to proper projection"""
        
        def analyse_Coords(Visum_X,Visum_Y,Google_X,Google_Y):        
            def dst_mtx(A,*B):
                try: 
                    B
                    mtx=[[abs(a-b) for a in A] for b in B]            
                except: 
                    mtx=[[abs(a-b) for a in A] for b in A]
                return mtx 
    
            def get_scale(Visum_d,Google_d):
                        range_=range(len(Visum_d))
                        Visum_deltas=dst_mtx(Visum_d)
                        for i in range_:
                                for j in range_:
                                    if i==j:
                                        Visum_deltas[i][i]=1000000000000000000000
                        
                        Google_deltas=dst_mtx(Google_d)
                        scales=[[Google_deltas[i][j]/Visum_deltas[i][j] for i in range_] for j in range_]
                        return sum([sum(row) for row in scales])/(len(Visum_d)**2-len(Visum_d))     
                
            def get_delta(Visum_d,Google_d,scale):
                size=len(Visum_d)
                
                
                return -sum([Visum_d[i]*scale-Google_d[i] for i in range(size)])/float(size)
                    
            def get_tg_Mtx(Visum_X,Visum_Y,Google_X,Google_Y):
                # to do ! dla macierzy obliczyc tg nachylenia par punktow dla Googla i dla Visuma 
                # policzyc roznice miedzy katami i statycznie opisac (mean, std, dev, etc.)
                pass   
            
            scale_X=get_scale(Visum_X,Google_X)        
            scale_Y=get_scale(Visum_Y,Google_Y)        
            delta_X=get_delta(Visum_X,Google_X,scale_X)        
            delta_Y=get_delta(Visum_Y,Google_Y,scale_Y)        
            return scale_X,scale_Y,delta_X,delta_Y
        
        
        
        #tg_V=abs(Visum_X[0]-Visum_X[1])/abs(Visum_Y[0]-Visum_Y[1])
        #tg_G=abs(Google_X[0]-Google_X[1])/abs(Google_Y[0]-Google_Y[1])
        #dev=1-tg_V/tg_G
        
        Visum_X,Visum_Y,Google_X,Google_Y = get_coords()
        Visum.Graphic.ShowMinimized()
        
        if type==[1,0,0,0]:
            
            """ poprzez projekcje Visum set projection """
            do_projection(Visum_X,Visum_Y,Google_X,Google_Y)
            
            
        elif type==[0,1,0,0]:
            """ przypadek rescale dla dwu punktow """
            
            scale_X,scale_Y,delta_X,delta_Y=analyse_Coords(Visum_X,Visum_Y,Google_X,Google_Y)
            rescale(scale_X,scale_Y,delta_X,delta_Y,False)         
            
        elif type==[0,0,1,0]:
            """ przypadek rescale dla wielu punktow """                                
            scale_X,delta_X,_=cleaned_linreg(Visum_X,Google_X,factor)    #zmiana 0,8 -> factor.   
            scale_Y,delta_Y,_=cleaned_linreg(Visum_Y,Google_Y,factor)
            rescale(scale_X,scale_Y,delta_X,delta_Y,False)           
             
        else: 
            """ przesuniecie czesci sieci (dodatkowy tuning) """    
            Node=Visum.Net.Nodes.ItemByKey(nodeno)            
            delta_X= Node.AttValue('Google_X')-Node.AttValue('XCoord')
            delta_Y= Node.AttValue('Google_Y')-Node.AttValue('YCoord')
            rescale(1,1,delta_X,delta_Y,True)
            
            
            
        Visum.Graphic.ShowMaximized()
            #"""finito"""
    

    
    def MakeVisScreenshot(self):
        '''
        make the screenshot of visum network with selected options
        '''
        NodeNumber=self.SB_NodeNumber.value()
        zoom=self.DSB_Zoom.value()
        try: 
            zoom=1/zoom
        except:
            pass
        
        try: 
            Visum.Graphic.Autozoom(Visum.Net.Nodes.ItemByKey(NodeNumber))
            self.V_NodeFilter.Init()
            self.V_NodeFilter.AddCondition("OP_NONE", False, "NO","EqualVal",NodeNumber)
            self.V_NodeFilter.UseFilter=True
    
            self.V_LinkFilter.Init()
            self.V_LinkFilter.AddCondition("OP_NONE",False,"ToNodeNo","EqualVal",NodeNumber)
            self.V_LinkFilter.UseFilter=True
            
            Window=Visum.Graphic.GetWindow()
            WWidth=Window[2]-Window[0]
            WHeight=Window[3]-Window[1]
            WXCenter=Window[0]+WWidth/2
            WYCenter=Window[1]+WHeight/2
            WXmin=WXCenter-(WWidth*zoom)
            WYmin=WYCenter-(WHeight*zoom)
            WXmax=WXCenter+(WWidth*zoom)
            WYmax=WYCenter+(WHeight*zoom)
            Visum.Graphic.SetWindow(WXmin,WYmin,WXmax,WYmax)
            Visum.Graphic.Screenshot(Paths["Screenshot"])
            
            Screenshot=QtGui.QPixmap(Paths["Screenshot"])
            Screenshot.scaled(350, 350, 0,1)
            self.L_ImageLeft.setPixmap(Screenshot)
            
        except:
            self.L_GeoPos.setText("node does not exist")
            
            
    def closeEvent(self):
        os.remove(Paths["Screenshot"])
        QtGui.qApp.quit()
        
    def openHelp(self):
        os.startfile(Paths["Help"])

            
if __name__ == '__main__':       
    try:
        ex
        import win32api,os        
        win32api.MessageBox(0, "Sorry! \n\nYou cannot run MapFormers twice with single Visum session. To run it again restart Visum and run MapFormers again.\n\n            intelligent-infrastructure")
    except:
        app2 = QtGui.QApplication(sys.argv)
        ex = GUI()    
        ex.show()    
        app2.exec_()
    