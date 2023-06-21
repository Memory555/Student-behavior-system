from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1060, 560)

        self.pb_other = QtWidgets.QPushButton(Form) # 查询详情
        self.pb_other.setGeometry(QtCore.QRect(240, 500, 101, 41))
        self.pb_other.setObjectName("pb_other")
        self.pb_exit = QtWidgets.QPushButton(Form)  # 退出
        self.pb_exit.setGeometry(QtCore.QRect(640, 500, 101, 41))
        self.pb_exit.setObjectName("pb_exit")
        self.tableView = QtWidgets.QTableView(Form) # 查询数据库所有结果框
        self.tableView.setGeometry(QtCore.QRect(100, 30, 841, 441))
        self.tableView.setObjectName("tableView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_other.setText(_translate("Form", "刷新"))
        self.pb_exit.setText(_translate("Form", "退出"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
