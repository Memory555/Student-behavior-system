from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 232)
        self.pb_success = QtWidgets.QPushButton(Form)
        self.pb_success.setGeometry(QtCore.QRect(30, 160, 101, 41))
        self.pb_success.setObjectName("pb_success") # 成功回答
        self.label = QtWidgets.QLabel(Form) # 姓名
        self.label.setGeometry(QtCore.QRect(220, 90, 51, 41))
        self.label.setObjectName("label")
        self.pb_fail = QtWidgets.QPushButton(Form)
        self.pb_fail.setGeometry(QtCore.QRect(200, 160, 101, 41))
        self.pb_fail.setObjectName("pb_fail") # 回答失败
        self.label_id = QtWidgets.QLabel(Form) # 学号
        self.label_id.setGeometry(QtCore.QRect(30, 90, 51, 41))
        self.label_id.setObjectName("label_id")
        self.pb_other = QtWidgets.QPushButton(Form) # 退出
        self.pb_other.setGeometry(QtCore.QRect(370, 160, 81, 41))
        self.pb_other.setObjectName("pb_other")
        self.lcdNumber_id = QtWidgets.QLCDNumber(Form)
        self.lcdNumber_id.setGeometry(QtCore.QRect(100, 90, 101, 41))  # 学号输出框
        self.lcdNumber_id.setObjectName("lcdNumber_id")
        self.pb_start = QtWidgets.QPushButton(Form) # 开始筛选幸运观众
        self.pb_start.setGeometry(QtCore.QRect(180, 20, 271, 41))
        self.pb_start.setObjectName("pb_start")
        self.pb_connect_db = QtWidgets.QPushButton(Form) # 连接数据库
        self.pb_connect_db.setGeometry(QtCore.QRect(30, 20, 131, 41))
        self.pb_connect_db.setObjectName("pb_connect_db")
        self.textBrowser_name = QtWidgets.QTextBrowser(Form)
        self.textBrowser_name.setGeometry(QtCore.QRect(280, 90, 181, 41))  # 姓名输出框
        self.textBrowser_name.setObjectName("textBrowser_name")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_success.setText(_translate("Form", "成功回答"))
        self.label.setText(_translate("Form", "姓名"))
        self.pb_fail.setText(_translate("Form", "答题失败"))
        self.label_id.setText(_translate("Form", "学号"))
        self.pb_other.setText(_translate("Form", "退出"))
        self.pb_start.setText(_translate("Form", "开始筛选幸运观众"))
        self.pb_connect_db.setText(_translate("Form", "连接数据库"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
