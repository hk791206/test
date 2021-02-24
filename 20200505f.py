# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '20200425f.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
import sys
import imutils
import math
from PyQt5.QtCore import QRect, Qt

class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        
        self.timer_camera = QtCore.QTimer()
        
        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)
                
        self.cap = cv2.VideoCapture(0)
       # cv2.imwrite(r'C:\Users\a0913\Desktop\82.jpg',self.image)
        self.CAM_NUM = 0
        self.CAM_SET_COUNT = 0

        self.slot_init()

        self.timer = QtCore.QTimer() 
        self.timer.timeout.connect(self.update_label) 
        self.timer.start(3000) # every 1,000 milliseconds

        print ("__start__")

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1214, 881)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setBold(True)
        font.setWeight(75)
        mainWindow.setFont(font)
        mainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 5)
        self.gridLayout_5.setHorizontalSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 2, 1)
        self.label_27 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout_5.addWidget(self.label_27, 0, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("background-color: rgb(255, 71, 105);\n"
"color: rgb(255, 255, 255);")
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.gridLayout_5.addWidget(self.label_26, 1, 1, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(1, 10)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_11 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(255, 43, 46);\n"
"color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 5, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 5, 1)
        self.label_14 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 4, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 5, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 4)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.gridLayout.setRowMinimumHeight(0, 1)
        self.gridLayout.setRowMinimumHeight(1, 1)
        self.gridLayout.setRowMinimumHeight(2, 1)
        self.gridLayout.setRowMinimumHeight(3, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(1, 6)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.widget = QtWidgets.QWidget(self.tab_2)
        self.widget.setGeometry(QtCore.QRect(10, 30, 596, 121))
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_16 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 0, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_4.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 1, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_4.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(16)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 2, 0, 1, 1)
        # self.pushButton = QtWidgets.QPushButton(self.widget)
        # font = QtGui.QFont()
        # font.setFamily("微軟正黑體")
        # font.setPointSize(13)
        # self.pushButton.setFont(font)
        # self.pushButton.setObjectName("pushButton")
        # self.gridLayout_4.addWidget(self.pushButton, 2, 3, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 0, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_4.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1214, 25))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)


        self.lineEdit_3.setValidator(QtGui.QIntValidator())
        self.lineEdit.setValidator(QtGui.QIntValidator())
        self.lineEdit_2.setValidator(QtGui.QIntValidator())
        self.lineEdit_4.setValidator(QtGui.QIntValidator())
        self.lineEdit_3.setText('5')
        self.lineEdit.setText('5')
        self.lineEdit_2.setText('10')
        self.lineEdit_4.setText('10')
        #print (type(self.lineEdit.text()))


        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.label_27.setText(_translate("mainWindow", "行政院農業委員會"))
        self.label_26.setText(_translate("mainWindow", "火鶴花辨識系統"))
        self.label_11.setText(_translate("mainWindow", "0"))
        self.label_8.setText(_translate("mainWindow", "破損數"))
        self.label_10.setText(_translate("mainWindow", "面積"))
        self.label_4.setText(_translate("mainWindow", "等級："))
        self.label_3.setText(_translate("mainWindow", "葉幅"))
        self.label_12.setText(_translate("mainWindow", "小邊緣瑕疵"))
        self.label_5.setText(_translate("mainWindow", "0"))
        self.label_9.setText(_translate("mainWindow", "0"))
        self.label_7.setText(_translate("mainWindow", "0"))
        self.label_6.setText(_translate("mainWindow", "葉寬"))
        self.label_13.setText(_translate("mainWindow", "大邊緣瑕疵"))
        self.label_14.setText(_translate("mainWindow", "0"))
        self.label_15.setText(_translate("mainWindow", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "檢測"))
        self.label_16.setText(_translate("mainWindow", "等級A 葉寬大於"))
        self.label_17.setText(_translate("mainWindow", "等級B 葉寬介於"))
        self.label_20.setText(_translate("mainWindow", "-"))
        self.label_18.setText(_translate("mainWindow", "等級C 葉寬小於"))
        #self.pushButton.setText(_translate("mainWindow", "確定"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("mainWindow", "參數設定"))

    def slot_init(self):
        self.button_open_camera_click()
        self.timer_camera.timeout.connect(self.show_camera)
        
        #self.pushButton.clicked.conncet(self.set_range)
        # self.pushButton_2.clicked.connect(self.savePhoto)
        # self.pushButton.clicked.connect(self.load_data)
        # self.pushButton_4.clicked.connect(self.openlight)
        # self.pushButton_5.clicked.connect(self.select)
        # self.pushButton_6.clicked.connect(self.save)
        # self.horizontalSlider.valueChanged.connect(self.label_color_change)
        # self.horizontalSlider_4.valueChanged.connect(self.label_color_change)
       # self.horizontalSlider_3.valueChanged.connect(self.label_color_change)

    def button_open_camera_click(self):        
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                self, u"Warning", u"Do you conncet the camera with Raspi?",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)

    def show_camera(self):

        if self.CAM_SET_COUNT == 0:
           # self.cap.set(3,2048)
           # self.cap.set(4,1536)
           # self.cap.set(10,100) #BRIGHTNESS ok
            #self.cap.set(11,50) #CONTRAST ok
           # self.cap.set(12,100) #SATURATION ok
            #self.cap.set(13,0) #HUE圖像的色相 ok
            #self.cap.set(15,-1) #EXPOSURE
            self.cap.set(16,1) #指示是否應將圖像轉換為RGB
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) 
            self.CAM_SET_COUNT = self.CAM_SET_COUNT + 1

        self.rect_count = 0
        self.little_defect = 0
        self.big_defect = 0

        flag, self.im = self.cap.read()
       # cv2.imwrite(r'C:\Users\a0913\Desktop\flower_pic\binbinbin.jpg',self.im)
        
        self.im = cv2.GaussianBlur(self.im,(5,5),1.5)  #############
        #self.im = cv2.bilateralFilter(self.im,40,75,75)

        self.im=cv2.flip(self.im,1)
        self.im2 = self.im.copy()
        self.im1 = self.im.copy()
        self.im2 = cv2.resize(self.im2,(640, 480)) 
        self.im1 = cv2.resize(self.im1,(640, 480)) 

        #self.image=cv2.flip(self.image,1) 

        HSV = cv2.cvtColor(self.im2, cv2.COLOR_BGR2HSV) 
        H, S, V = cv2.split(HSV)    
        Lowerred0 = np.array([156,43,46])
        Upperred0 = np.array([180,255,255])
        mask1 = cv2.inRange(HSV, Lowerred0, Upperred0) 
        Lowerred1 = np.array([0,43,46])
        Upperred1 = np.array([10,255,255])
        mask2 = cv2.inRange(HSV, Lowerred1, Upperred1)   
        pic_bin = mask1 +mask2
        print (np.sum(pic_bin))
        if np.sum(pic_bin) == 0 :
                #print ('blackblackblackblackblackblackblackblackblackblackblackblack')
                self.real_rect_count = 0
                self.little_defect = 0
                self.real_big_defect = 0
                self.max_area = 0
                self.Height = 0
                self.Width = 0
                self.label_5.setText('%s'%self.Width) #葉幅
                self.label_7.setText('%s'%self.Height)  #葉寬
                self.label_11.setText('%s'%self.max_area)  #面積
                self.label_9.setText('%s'%self.real_rect_count) #破損數
                self.label_14.setText('%s'%self.little_defect) #小瑕疵
                self.label_15.setText('%s'%self.real_big_defect) #大瑕疵

                cv2.putText(self.im1, "Height:%d"%self.Width, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(self.im1, "Width:%d"%self.Height, (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(self.im1, "Area:%d"%self.max_area, (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                self.im1 = cv2.cvtColor(self.im1, cv2.COLOR_BGR2RGB)
                _translate = QtCore.QCoreApplication.translate
                showImage = QtGui.QImage(self.im1.data, self.im1.shape[1], self.im1.shape[0], QtGui.QImage.Format_RGB888)
                self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
                self.label_2.setScaledContents(True)
                self.label_2.setCursor(Qt.CrossCursor)

                self.label_4.setText('等級：')

        else :
                #pic_bin = cv2.bilateralFilter(pic_bin,40,75,75)
                kernel = np.ones((5,5),np.uint8)              #########################
                #pic_bin = cv2.dilate(pic_bin,kernel,iterations = 1)
                #pic_bin = cv2.erode(pic_bin,kernel,iterations = 1)
                #pic_bin = cv2.morphologyEx(pic_bin, cv2.MORPH_CLOSE, kernel)

                ##pic_bin = cv2.bilateralFilter(pic_bin,40,75,75)
                pic_bin = cv2.dilate(pic_bin,kernel,iterations = 1)

               # pic_bin = cv2.bilateralFilter(pic_bin,40,75,75)
                pic_bin = cv2.erode(pic_bin,kernel,iterations = 1)
                #pic_bin = cv2.dilate(pic_bin,kernel,iterations = 1)
                cv2.imwrite(r'C:\Users\a0913\Desktop\flower_pic\binbin1.jpg',pic_bin)
        
        ######## detect area
                contours_2, hierarchy = cv2.findContours(pic_bin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                if len(contours_2) > 0 :
                        cnt_max = contours_2[0] #获取最大的一个轮廓
                        self.max_area = cv2.contourArea(cnt_max)
                        for cont_2 in contours_2:
                                if cv2.contourArea(cont_2) > self.max_area:
                                        cnt_max = cont_2
                                        self.max_area = cv2.contourArea(cont_2)
                        print('max_area:',self.max_area)
                ######## detect defect
                        #contours, hierarchy = cv2.findContours(pic_bin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                        #print ("there are " + str(len(contours)) + " contours")
                        
                        #cnt = contours[0]
                        #print ("there are " + str(len(cnt)) + " points in contours[0]")
                        hull = cv2.convexHull(cnt_max,returnPoints = False)
                        #print ("after convexHull, there are " + str(len(hull)) + " points")
                        defects = cv2.convexityDefects(cnt_max,hull)
                        #print ("there are " + str(len(defects)) + " defects in contours[0]")
                        
                        if not defects is None :
                                for i in range(defects.shape[0]):
                                        s,e,f,d = defects[i,0]
                                        start = tuple(cnt_max[s][0])
                                        end = tuple(cnt_max[e][0])
                                        far = tuple(cnt_max[f][0])
                                        print (d)
                                        if d >= 1000 and d <= 5000:
                                                self.little_defect = self.little_defect + 1
                                        elif d > 5000 :
                                                self.big_defect = self.big_defect + 1
                                        cv2.line(self.im2,start,end,[0,255,0],2)
                                        cv2.circle(self.im2,far,2,[255,0,0],-1)

                                self.real_big_defect = self.big_defect - 1
                                if self.real_big_defect < 0 :
                                        self.real_big_defect = 0

                                print ('little_defect:',self.little_defect)
                                print ('real_big_defect:',self.real_big_defect)
                        else :
                                self.real_big_defect = 0
                                self.little_defect = 0
                                # cv2.imshow('im', im)
                                # cv2.waitKey(0)
                                # cv2.destroyAllWindows()
                else:
                        self.Height = 0
                        self.Width = 0
                        self.max_area = 0
                        self.real_big_defect = 0
                        self.little_defect = 0
                        self.real_rect_count = 0
                        self.little_defect = 0
                        self.real_big_defect = 0


                ######## detect height,width and broke
                global rect
                
                contours = cv2.findContours(pic_bin,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)  #cv2.RETR_EXTERNAL 定义只检测外围轮廓
                #print (contours[0])
                if len(contours) > 0 :
                        cnts = contours[1] if imutils.is_cv3() else contours[0]  #用imutils来判断是opencv是2还是2+

                        rect_height = np.zeros(shape=(1,len(cnts)))
                        rect_width = np.zeros(shape=(1,len(cnts)))
                        rect_area = np.zeros(shape=(1,len(cnts)))

                        for cnt in cnts: 
                                # rows,cols = self.im1.shape[:2]
                                # [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
                                # if vx < 0.001 :
                                #         vx = 0.001
                                # lefty = int((-x*vy/vx) + y)
                                # righty = int(((cols-x)*vy/vx)+y)
                                # #print ('斜率:',vy/vx)
                                # theta = math.acos(vx)*180/math.pi
                                # #print ('theta',theta)
                                # print ('sssssssssssssssssss',(cols-1,righty-1),(0,lefty-1))
                                # cv2.line(self.im1,(cols-1,righty),(0,lefty),(255,0,0),2)

                                # 最小外接矩形框，有方向角
                                rect = cv2.minAreaRect(cnt)
                                #print (rect[1][0],rect[1][1])
                                rect_height[0][self.rect_count] = rect[1][0]
                                rect_width[0][self.rect_count] = rect[1][1]
                                rect_area[0][self.rect_count] = rect[1][0]*rect[1][1]
                                #print (abs(rect[2]))
                                #minirec_theta = rect[2]
                                #print (type(rect[2]),(type(theta)),type(rect))
                                #rect[2] = -(90.0-theta)
                                

                                box = cv2.cv.Boxpoints() if imutils.is_cv2()else cv2.boxPoints(rect)
                                box = np.int0(box)
                                # if theta-5 < 90- abs(rect[2]) < theta+5 :  


                                cv2.drawContours(self.im1, [box], 0, (255, 0, 0), 2)
                                self.rect_count = self.rect_count + 1
                                # else :
                                #         self.Height = 0
                                #         self.Width = 0
                                #         self.max_area = 0

                        if self.rect_count != 0 :
                                
                                max_index = np.argmax(rect_area)
                                max_height = rect_height[0][max_index]
                                max_width = rect_width[0][max_index]

                                self.real_rect_count = self.rect_count-2
                                if self.real_rect_count < 0 :
                                        self.real_rect_count = 0

                                print ('broke:',self.real_rect_count)
                                #im = cv2.resize(im,(640, 480)) 
                                #print (rect)
                                if max_height >= max_width :
                                        self.Height = max_height
                                        self.Width = max_width
                                else :
                                        self.Width = max_height
                                        self.Height = max_width                                       
                                # cv2.imshow('a',im)
                                # cv2.imwrite(r'C:\Users\a0913\Desktop\flower_pic\result.jpg',im)
                                # cv2.waitKey(0)
                                # cv2.destroyAllWindows()

                cv2.putText(self.im1, "Height:%d"%self.Height, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(self.im1, "Width:%d"%self.Width, (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(self.im1, "Area:%d"%self.max_area, (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                self.im1 = cv2.cvtColor(self.im1, cv2.COLOR_BGR2RGB)

                _translate = QtCore.QCoreApplication.translate
                showImage = QtGui.QImage(self.im1.data, self.im1.shape[1], self.im1.shape[0], QtGui.QImage.Format_RGB888)
                self.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage))
                self.label_2.setScaledContents(True)
                self.label_2.setCursor(Qt.CrossCursor)

                self.Height = round(self.Height*0.05784,2)
                #self.Height = "%.2f"%self.Height
                self.Width = round(self.Width*0.05784,2)
                self.max_area = round(self.max_area*0.05784*0.05784,2)
                self.real_rect_count = int(self.real_rect_count)
                self.little_defect = int(self.little_defect)
                self.real_big_defect = int(self.real_big_defect)

                self.label_5.setText('%s'%self.Height) #葉幅
                self.label_7.setText('%s'%self.Width)  #葉寬
                self.label_11.setText('%s'%self.max_area)  #面積
                self.label_9.setText('%s'%self.real_rect_count) #破損數
                self.label_14.setText('%s'%self.little_defect) #小瑕疵
                self.label_15.setText('%s'%self.real_big_defect) #大瑕疵
                self.range()
                self.timer_camera.start(2000)
    def update_label(self): 
            print ('3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s3s')
            
        #  current_time = time.strftime("%Y-%m-%d %H:%M:%S") 
        #  ui.label_4.setText(current_time)

    def range(self) :
        if (self.lineEdit_3.text() == '') or (self.lineEdit.text() == '') or (self.lineEdit_2.text() == '') or (self.lineEdit_4.text() == '') :
                self.label_4.setText('等級：')

        else :
            self.lineEdit_3_value = self.lineEdit_3.text()
            self.lineEdit_3_value = int(self.lineEdit_3_value)
            self.lineEdit_value = self.lineEdit.text()
            self.lineEdit_value = int(self.lineEdit_value)
            self.lineEdit_2_value = self.lineEdit_2.text()
            self.lineEdit_2_value = int(self.lineEdit_2_value)         
            self.lineEdit_4_value = self.lineEdit_4.text()
            self.lineEdit_4_value = int(self.lineEdit_4_value)

            if  self.Width < self.lineEdit_3_value and self.Width > 0:
                    self.label_4.setText('等級：C')
            elif self.Width >= self.lineEdit_value and self.Width < self.lineEdit_2_value :
                    self.label_4.setText('等級：B')
            elif self.Width >= self.lineEdit_4_value :
                    self.label_4.setText('等級：A')

if __name__ == '__main__': 

#     app_progress = QApplication(sys.argv)
#     window = Actions()
#     QApplication.closeAllWindows()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #ui.setupUi(MainWindow)
    MainWindow.setWindowTitle('Flower system')
    MainWindow.show()

#     def update_label(): 
#          current_time = time.strftime("%Y-%m-%d %H:%M:%S") 
#          ui.label_4.setText(current_time)

#     timer = QtCore.QTimer() 
#     timer.timeout.connect(update_label) 
#     timer.start(1000) # every 1,000 milliseconds

    sys.exit(app.exec_()) 