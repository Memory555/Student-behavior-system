import os
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
# 将根目录（execute所在目录）添加到环境变量
# from utils2.GlobalVar import add_path_to_sys, statical_facedata_nums
from utils2.GlobalVar import num_list

# 导入分析详情框界面
from ui import detail

# 将根目录（execute所在目录）添加到环境变量
from utils2.GlobalVar import add_path_to_sys, connect_to_sql
rootdir = add_path_to_sys()


class Detaillog(QWidget):
    def __init__(self):
        super().__init__()

        self.Dialog = detail.Ui_Form()
        self.Dialog.setupUi(self)

        # 实现路径错误提示，方便定位错误
        self.current_filename = os.path.basename(__file__)

        try:
            # 设置窗口名称和图标
            self.setWindowTitle("情绪分析详情界面")
            self.setWindowIcon(QIcon(f'{rootdir}/logo_imgs/fcb_logo.jpg'))
        except FileNotFoundError as e:
            print("[ERROR] UI背景图片路径不正确！(source file: {})".format(self.current_filename), e)
        # else:
        #     print("[INFO] 设置icon成功！")

        self.Dialog.pb_other.clicked.connect(self.answer_other)
        self.Dialog.pb_exit.clicked.connect(self.pd_exit)

    # 查询详情
    def answer_other(self):
        try:
            db, cursor = connect_to_sql()
        except ConnectionAbortedError as e:
            self.ui.textBrowser_log.append('[INFO] 连接数据库失败，请检查配置信息！')
        else:
            sql = "select * from detail"
            # 执行查询
            cursor.execute(sql)
            results = cursor.fetchall()
            self.student_ids = []
            self.student_names = []
            self.student_emo = []
            self.student_time = []
            for item in results:
                self.student_ids.append(item[0])
                self.student_names.append(item[1])
                self.student_emo.append(item[2])
                self.student_time.append(item[3])
        finally:
            db.commit()
            cursor.close()
            db.close()
        if len(self.student_ids) == 0:
            QMessageBox.warning(self, "Error", "暂无情绪分析结果！", QMessageBox.Ok)
        else:
            # 设置显示数据层次结构，4行4列(包含行表头)
            table_view_module = QtGui.QStandardItemModel(len(num_list), 1)
            table_view_module.setHorizontalHeaderLabels(['学号', '姓名', '当前表情', '情绪持续时间/s'])

            step = 0
            for i in num_list:
                id = int(i) # 要显示的学号
                k = self.student_ids.index(id)
                # id = self.student_ids[i]
                num = QtGui.QStandardItem(str(id))
                name = self.student_names[k]
                name = QtGui.QStandardItem(name)
                emo = self.student_emo[k]
                emo = QtGui.QStandardItem(emo)
                current_time = datetime.now()
                last_time = (current_time - self.student_time[k]).seconds
                last_time = QtGui.QStandardItem(str(last_time))


                # 设置每个位置的行名称和文本值
                table_view_module.setItem(step, 0, num)
                table_view_module.setItem(step, 1, name)
                table_view_module.setItem(step, 2, emo)
                table_view_module.setItem(step, 3, last_time)
                step = step + 1

            # 指定显示的tableView控件，实例化表格视图
            self.Dialog.tableView.setModel(table_view_module)

    def pd_exit(self):
        self.close()

    def handle_click(self):
        if not self.isVisible():
            self.show()

