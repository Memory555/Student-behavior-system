from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1086, 907)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_camera = QtWidgets.QLabel(self.centralwidget) # 未打开相机的黑色界面
        self.label_camera.setGeometry(QtCore.QRect(30, 80, 800, 600))
        self.label_camera.setText("")
        self.label_camera.setObjectName("label_camera")
        self.label_time = QtWidgets.QLabel(self.centralwidget) # 显示时间
        self.label_time.setGeometry(QtCore.QRect(850, 20, 231, 30))
        self.label_time.setText("")
        self.label_time.setObjectName("label_time")
        self.bt_random_check = QtWidgets.QPushButton(self.centralwidget) # 随机抽签
        self.bt_random_check.setGeometry(QtCore.QRect(860, 740, 211, 41))
        self.bt_random_check.setObjectName("bt_random_check")
        self.bt_supplement = QtWidgets.QPushButton(self.centralwidget) # 漏签补签
        self.bt_supplement.setGeometry(QtCore.QRect(970, 700, 101, 31))
        self.bt_supplement.setObjectName("bt_supplement")
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(150, 690, 31, 131))
        self.line_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.lineEdit_supplement = QtWidgets.QLineEdit(self.centralwidget) # 漏签补签输入框
        self.lineEdit_supplement.setGeometry(QtCore.QRect(860, 700, 101, 31))
        self.lineEdit_supplement.setObjectName("lineEdit_supplement")
        self.textBrowser_log = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_log.setGeometry(QtCore.QRect(350, 690, 301, 161))
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 833, 301, 16))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.bt_start_check = QtWidgets.QPushButton(self.centralwidget) # 开始分析
        self.bt_start_check.setGeometry(QtCore.QRect(180, 760, 151, 61))
        self.bt_start_check.setObjectName("bt_start_check")
        self.bt_generator = QtWidgets.QPushButton(self.centralwidget) # 训练模型
        self.bt_generator.setGeometry(QtCore.QRect(180, 690, 151, 61))
        self.bt_generator.setObjectName("bt_generator")
        self.bt_analyse = QtWidgets.QPushButton(self.centralwidget) # 分析详情
        self.bt_analyse.setGeometry(QtCore.QRect(660, 760, 181, 61))
        self.bt_analyse.setObjectName("bt_analyse")
        self.tableView_escape = QtWidgets.QTableView(self.centralwidget) # 未到记录表
        self.tableView_escape.setGeometry(QtCore.QRect(860, 450, 211,201))
        self.tableView_escape.setObjectName("tableView_escape")
        self.bt_check_variation = QtWidgets.QPushButton(self.centralwidget) # 核验数据库
        self.bt_check_variation.setGeometry(QtCore.QRect(20, 760, 131, 61))
        self.bt_check_variation.setObjectName("bt_check_variation")
        self.bt_open_camera = QtWidgets.QPushButton(self.centralwidget) # 打开相机
        self.bt_open_camera.setGeometry(QtCore.QRect(660, 690, 181, 61))
        self.bt_open_camera.setObjectName("bt_open_camera")
        self.label_title = QtWidgets.QLabel(self.centralwidget) # 标题
        self.label_title.setGeometry(QtCore.QRect(360, 20, 400, 40))
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(30, 70, 800, 600))
        # self.label_logo.setMinimumSize(QtCore.QSize(800, 600))
        # self.label_logo.setMaximumSize(QtCore.QSize(800, 600))
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.bt_leave = QtWidgets.QPushButton(self.centralwidget) # 请假登记
        self.bt_leave.setGeometry(QtCore.QRect(970, 660, 101, 31))
        self.bt_leave.setObjectName("bt_leave")
        self.bt_exit = QtWidgets.QPushButton(self.centralwidget) # 退出系统
        self.bt_exit.setGeometry(QtCore.QRect(860, 790, 211, 61))
        self.bt_exit.setObjectName("bt_exit")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(20, 60, 821, 21))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lineEdit_leave = QtWidgets.QLineEdit(self.centralwidget) # 请假登记输入
        self.lineEdit_leave.setGeometry(QtCore.QRect(860, 660, 101, 31))
        self.lineEdit_leave.setObjectName("lineEdit_leave")
        self.bt_listName1 = QtWidgets.QPushButton(self.centralwidget) # 未到
        self.bt_listName1.setGeometry(QtCore.QRect(880, 410, 50, 30))
        self.bt_listName1.setObjectName("bt_listName1")

        self.bt_output = QtWidgets.QPushButton(self.centralwidget)  # 未到导出
        self.bt_output.setGeometry(QtCore.QRect(980, 410, 50, 30))
        self.bt_output.setObjectName("bt_output")

        self.label_emo1 = QtWidgets.QLabel(self.centralwidget)  # 情绪1
        self.label_emo1.setGeometry(QtCore.QRect(880, 80, 50, 30))
        self.label_emo1.setObjectName("label_emo1")

        self.label_emo1_1 = QtWidgets.QLabel(self.centralwidget)  # 情绪1
        self.label_emo1_1.setGeometry(QtCore.QRect(980, 80, 70, 30))
        self.label_emo1_1.setObjectName("label_emo1_1")

        self.label_emo2 = QtWidgets.QLabel(self.centralwidget)  # 情绪2
        self.label_emo2.setGeometry(QtCore.QRect(880, 140, 50, 30))
        self.label_emo2.setObjectName("label_emo2")

        self.label_emo2_2 = QtWidgets.QLabel(self.centralwidget)  # 情绪2
        self.label_emo2_2.setGeometry(QtCore.QRect(980, 140, 70, 30))
        self.label_emo2_2.setObjectName("label_emo2_2")

        self.label_emo3 = QtWidgets.QLabel(self.centralwidget)  # 情绪3
        self.label_emo3.setGeometry(QtCore.QRect(880, 200, 50, 30))
        self.label_emo3.setObjectName("label_emo3")

        self.label_emo3_3 = QtWidgets.QLabel(self.centralwidget)  # 情绪3
        self.label_emo3_3.setGeometry(QtCore.QRect(980, 200, 70, 30))
        self.label_emo3_3.setObjectName("label_emo3_3")

        self.label_emo4 = QtWidgets.QLabel(self.centralwidget)  # 情绪4
        self.label_emo4.setGeometry(QtCore.QRect(880, 260, 50, 30))
        self.label_emo4.setObjectName("label_emo4")

        self.label_emo4_4 = QtWidgets.QLabel(self.centralwidget)  # 情绪4
        self.label_emo4_4.setGeometry(QtCore.QRect(980, 260, 70, 30))
        self.label_emo4_4.setObjectName("label_emo4")

        self.label_emo6 = QtWidgets.QLabel(self.centralwidget)  # 情绪5
        self.label_emo6.setGeometry(QtCore.QRect(880, 320, 50, 30))
        self.label_emo6.setObjectName("label_emo6")

        self.label_emo6_6 = QtWidgets.QLabel(self.centralwidget)  # 情绪5
        self.label_emo6_6.setGeometry(QtCore.QRect(980, 320, 70, 30))
        self.label_emo6_6.setObjectName("label_emo6")

        self.bt_gathering = QtWidgets.QPushButton(self.centralwidget) # 信息采集
        self.bt_gathering.setGeometry(QtCore.QRect(20, 690, 131, 61))
        self.bt_gathering.setObjectName("bt_gathering")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(840, 70, 20, 781))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1086, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSetting)
        self.menuFile.addAction(self.actionExport)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bt_random_check.setText(_translate("MainWindow", "随机抽签"))
        self.bt_supplement.setText(_translate("MainWindow", "漏签补签"))
        self.bt_start_check.setText(_translate("MainWindow", "开始分析"))
        self.bt_generator.setText(_translate("MainWindow", "训练模型"))
        self.bt_analyse.setText(_translate("MainWindow", "分析详情"))
        self.bt_check_variation.setText(_translate("MainWindow", "未采集人员"))
        self.bt_open_camera.setText(_translate("MainWindow", "打开相机"))
        self.bt_leave.setText(_translate("MainWindow", "请假登记"))
        self.bt_exit.setText(_translate("MainWindow", "退出系统"))
        self.label_emo1.setText(_translate("MainWindow", "高兴"))
        self.label_emo1_1.setText(_translate("MainWindow", "       "))
        self.label_emo2.setText(_translate("MainWindow", "伤心"))
        self.label_emo2_2.setText(_translate("MainWindow", "       "))
        self.label_emo3.setText(_translate("MainWindow", "惊讶"))
        self.label_emo3_3.setText(_translate("MainWindow", "       "))
        self.label_emo4.setText(_translate("MainWindow", "生气"))
        self.label_emo4_4.setText(_translate("MainWindow", "       "))
        self.label_emo6.setText(_translate("MainWindow", "中立"))
        self.label_emo6_6.setText(_translate("MainWindow", "       "))
        self.bt_listName1.setText(_translate("MainWindow", "未到"))
        self.bt_output.setText(_translate("MainWindow", "导出"))
        self.bt_gathering.setText(_translate("MainWindow", "信息采集"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setWhatsThis(_translate("MainWindow", "Author: datamonday"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionExport.setText(_translate("MainWindow", "Export"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
