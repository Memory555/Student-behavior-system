import os
import pickle
import sys
import threading
from datetime import datetime
from copy import deepcopy
import cv2
import imutils
import numpy as np
# 导入数据库操作包
import pymysql
# 导入界面处理包
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime, QCoreApplication, QThread
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
# 导入频帧画面大小调整包
from imutils import face_utils
from imutils.video import VideoStream
# 导入眨眼检测必要的包
from scipy.spatial import distance as dist

# 导入UI主界面
# from ui import MainUI
# 使用mainwindow类重构
from ui import mainwindow as MainWindowUI

# 导入打印中文脚本
from utils2 import PutChineseText
# 导入人脸识别检测包
from utils2 import GeneratorModel
# 导入眨眼检测类
from utils2.BlinksDetectionThread import BlinksDetectThread
# 导入信息采集槽函数类
from utils2.InfoDialog import InfoDialog
# 导入随机点名类
from utils2.RandomCheck import RCDialog
# 添加数据库连接操作
from utils2.GlobalVar import connect_to_sql

# 导入考勤状态判断相关函数
from utils2.AttendanceCheck import attendance_check
from utils2.GlobalVar import FR_LOOP_NUM, statical_facedata_nums

# # 为方便调试，修改后导入模块，重新导入全局变量模块
# import importlib
# importlib.reload(GeneratorModel)

import sys
import os
from collections import Counter

# 添加当前路径到环境变量
sys.path.append(os.getcwd())

# 导入全局变量，主要包含摄像头ID等
from utils2.GlobalVar import CAMERA_ID

import cv2 as cv
import numpy as np
from openvino.inference_engine import IECore

# 加载FaceNet人脸识别模型
model_xml = "E:/soft/smart/Face-Recognition-Class-Attendance-System-master/emo/intel/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.xml"
model_bin = "E:/soft/smart/Face-Recognition-Class-Attendance-System-master/emo/intel/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.bin"

labels = ['neutral', 'happy', 'sad', 'surprise', 'anger']

ie = IECore()
emotion_net = ie.read_network(model=model_xml, weights=model_bin)

input_blob = next(iter(emotion_net.input_info))

exec_net = ie.load_network(network=emotion_net, device_name="CPU", num_requests=2)

class MainWindow(QtWidgets.QMainWindow):
    # 类构造函数
    def __init__(self):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super().__init__()
        # self.ui = MainUI.Ui_Form()
        self.ui = MainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)

        # ####################### 相对路径 ######################
        # 初始化label显示的(黑色)背景
        self.bkg_pixmap = QPixmap('./logo_imgs/bkg1.png')
        # 设置主窗口的logo
        self.logo = QIcon('./logo_imgs/fcb_logo.jpg')
        # 设置提示框icon
        self.info_icon = QIcon('./logo_imgs/info_icon.jpg')
        # OpenCV深度学习人脸检测器的路径
        self.detector_path = "./model_face_detection"
        # OpenCV深度学习面部嵌入模型的路径
        self.embedding_model = "./model_facenet/openface_nn4.small2.v1.t7"
        # 训练模型以识别面部的路径
        self.recognizer_path = "./saved_weights/recognizer.pickle"
        # 标签编码器的路径
        self.le_path = "./saved_weights/le.pickle"

        # ###################### 窗口初始化 ######################
        # 设置窗口名称和图标
        self.setWindowTitle('学生行为分析系统 v1.0')
        self.setWindowIcon(self.logo)
        # 设置单张图片背景
        self.ui.label_camera.setPixmap(self.bkg_pixmap)
        # label_time显示系统时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time_text)
        # 启动时间任务
        self.timer.start()

        # ###################### 摄像头初始化 ######################
        # 初始化摄像头，默认调用第一个摄像头
        # self.url = 0
        # 如果要调用摄像头1，则设置为1，适用于：笔记本外接USB摄像头
        self.url = 0
        self.cap = cv2.VideoCapture()
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        # self.cap.set(cv2.CAP_PROP_FPS, 20)

        # ###################### 按键的槽函数 ######################
        # 设置摄像头按键连接函数
        self.ui.bt_open_camera.clicked.connect(self.open_camera)
        # 设置开始分析按键的回调函数
        self.ui.bt_start_check.clicked.connect(self.auto_control)
        # # 设置退出系统按键的回调函数
        # self.ui.bt_exit.clicked.connect(self.auto_control)
        # # 设置活体检测按键的回调函数
        # self.ui.bt_blinks.clicked.connect(self.blinks_thread)
        # 设置“退出系统”按键事件, 按下之后退出主界面
        self.ui.bt_exit.clicked.connect(self.quit_window)
        # 设置信息采集按键连接
        self.ui.bt_gathering.clicked.connect(self.open_info_dialog)
        # 设置区分打开摄像头还是人脸识别的标识符
        self.switch_bt = 0

        # ###################### 数据库相关操作 ######################
        # 初始化需要记录的人名
        self.record_name = []
        # 设置更新人脸数据库的按键连接函数
        self.ui.bt_generator.clicked.connect(self.train_model)
        # 设置查询班级人数按键的连接函数
        # self.ui.bt_check.clicked.connect(self.check_nums)
        # 设置请假按键的连接函数
        self.ui.bt_leave.clicked.connect(self.leave_button)
        # 设置漏签补签按键的连接函数
        self.ui.bt_supplement.clicked.connect(self.supplyment_button)
        # 设置对输入内容的删除提示
        self.ui.lineEdit_leave.setClearButtonEnabled(True)
        self.ui.lineEdit_supplement.setClearButtonEnabled(True)
        # # 设置查看结果（显示未到和迟到）按键的连接函数
        # self.ui.bt_view.clicked.connect(self.show_late_absence)
        # 核验本地人脸数据集与数据库中的ID是否一致，即验证是否有未录入数据库的情况，以及是否有未采集人脸的情况。
        self.ui.bt_check_variation.clicked.connect(self.check_variation_db)

        # self.check_time_set, ok = QInputDialog.getText(self, '考勤时间设定', '请输入考勤时间(格式为00:00:00):')
        self.check_time_set = '08:00:00'

        # # 设置输入考勤时间的限制
        # self.ui.spinBox_time_hour.setRange(0, 23)
        # self.ui.spinBox_time_minute.setRange(0, 59)

    # 显示系统时间以及相关文字提示函数
    def show_time_text(self):
        # 设置宽度
        self.ui.label_time.setFixedWidth(200)
        # 设置显示文本格式
        self.ui.label_time.setStyleSheet(
            # "QLabel{background:white;}" 此处设置背景色
            "QLabel{color:rgb(0, 0, 0); font-size:14px; font-weight:bold; font-family:宋体;}"
            "QLabel{font-size:14px; font-weight:bold; font-family:宋体;}")

        current_datetime = QDateTime.currentDateTime().toString()
        self.ui.label_time.setText("" + current_datetime)

        # 显示“人脸识别考勤系统”文字
        self.ui.label_title.setFixedWidth(400)
        self.ui.label_title.setStyleSheet("QLabel{font-size:26px; font-weight:bold; font-family:宋体;}")
        self.ui.label_title.setText("学生行为分析系统")

    def open_camera(self):
        # 判断摄像头是否打开，如果打开则为true，反之为false
        if not self.cap.isOpened():
            self.ui.label_logo.clear()
            # 默认打开Windows系统笔记本自带的摄像头，如果是外接USB，可将0改成1
            self.cap.open(self.url)
            self.show_camera()
        else:
            self.cap.release()
            self.ui.label_logo.clear()
            self.ui.label_camera.clear()
            self.ui.bt_open_camera.setText(u'打开相机')

    # def exit(self):
    #     # 退出系统

    # 进入考勤模式，通过switch_bt进行控制的函数
    def auto_control(self):
        # self.check_time_set = self.format_check_time_set()
        # if self.check_time_set == '':
        #     QMessageBox.warning(self, "Warning", "请先设定考勤时间(例 08:00)！", QMessageBox.Ok)
        # else:
        if self.cap.isOpened():
            if self.switch_bt == 0:
                self.switch_bt = 1
                # QMessageBox.information(self, "Tips", f"您设定的考勤时间为：{self.check_time_set}", QMessageBox.Ok)
                self.ui.bt_start_check.setText(u'退出分析')
                self.show_camera()
            elif self.switch_bt == 1:
                self.switch_bt = 0
                self.ui.bt_start_check.setText(u'开始分析')
                self.show_camera()
            else:
                print("[Error] The value of self.switch_bt must be zero or one!")
        else:
            QMessageBox.information(self, "Tips", "请先打开摄像头！", QMessageBox.Ok)

    # def blinks_thread(self):
    #     bt_text = self.ui.bt_blinks.text()
    #     if self.cap.isOpened():
    #         if bt_text == '活体检测':
    #             # 初始化眨眼检测线程
    #             self.startThread = BlinksDetectThread()
    #             self.startThread.start()  # 启动线程
    #             self.ui.bt_blinks.setText('停止检测')
    #         else:
    #             self.ui.bt_blinks.setText('活体检测')
    #             # self.startThread.terminate()  # 停止线程
    #     else:
    #         QMessageBox.information(self, "Tips", "请先打开摄像头！", QMessageBox.Ok)

    def show_camera(self):
        # 如果按键按下
        global embedded, le, recognizer
        if self.switch_bt == 0:
            self.ui.label_logo.clear()
            self.ui.bt_open_camera.setText(u'关闭相机')
            while self.cap.isOpened():
                # 以BGR格式读取图像
                ret, self.image = self.cap.read()
                # 告诉QT处理来处理任何没有被处理的事件，并且将控制权返回给调用者，让代码变的没有那么卡
                QApplication.processEvents()
                # 将图像转换为RGB格式
                show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                # opencv 读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage QImage(uchar * data, int width,
                self.showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                self.ui.label_camera.setPixmap(QPixmap.fromImage(self.showImage))
            # 因为最后会存留一张图像在lable上，需要对lable进行清理
            self.ui.label_camera.clear()
            self.ui.bt_open_camera.setText(u'打开相机')
            # 设置单张图片背景
            self.ui.label_camera.setPixmap(self.bkg_pixmap)

        elif self.switch_bt == 1:
            self.ui.label_logo.clear()
            self.ui.bt_start_check.setText(u'退出分析')

            # 人脸检测的置信度
            confidence_default = 0.5
            # 从磁盘加载序列化面部检测器
            proto_path = os.path.sep.join([self.detector_path, "deploy.prototxt"])
            model_path = os.path.sep.join([self.detector_path, "res10_300x300_ssd_iter_140000.caffemodel"])
            detector = cv2.dnn.readNetFromCaffe(proto_path, model_path)
            # 从磁盘加载序列化面嵌入模型
            try:
                self.ui.textBrowser_log.append("[INFO] 正在加载人脸识别模型")
                self.ui.textBrowser_log.append("[INFO] 正在加载情绪识别模型")
                # 加载FaceNet人脸识别模型
                embedded = cv2.dnn.readNetFromTorch(self.embedding_model)
            except FileNotFoundError as e:
                self.ui.textBrowser_log.append("面部嵌入模型的路径不正确！", e)

            # 加载实际的人脸识别模型和标签
            try:
                recognizer = pickle.loads(open(self.recognizer_path, "rb").read())
                le = pickle.loads(open(self.le_path, "rb").read())
            except FileNotFoundError as e:
                self.ui.textBrowser_log.append("人脸识别模型保存路径不正确！", e)

            # 构造人脸id的字典，以便存储检测到每个id的人脸次数，键为人名(ID)，值初始化为0，方便统计次数
            self.face_name_dict = dict(zip(le.classes_, len(le.classes_) * [0]))
            # 初始化循环次数，比如统计10帧中人脸的数量，取最大值进行考勤
            loop_num = 0
            # 循环来自视频文件流的帧
            while self.cap.isOpened():
                loop_num += 1
                # 从线程视频流中抓取帧
                ret, frame = self.cap.read()
                QApplication.processEvents()
                if ret:
                    # 调整框架的大小以使其宽度为900像素（同时保持纵横比），然后抓取图像尺寸
                    frame = imutils.resize(frame, width=900)
                    (h, w) = frame.shape[:2]
                    # 从图像构造一个blob, 缩放为 300 x 300 x 3 像素的图像，为了符合ResNet-SSD的输入尺寸
                    # OpenCV Blog的使用可参考：https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
                    image_blob = cv2.dnn.blobFromImage(
                        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                        (104.0, 177.0, 123.0), swapRB=False, crop=False)
                    # 应用OpenCV的基于深度学习的人脸检测器来定位输入图像中的人脸
                    detector.setInput(image_blob)
                    # 传入到ResNet-SSD以检测人脸
                    detections = detector.forward()

                    # 初始化一个列表，用于保存识别到的人脸
                    face_names = []
                    # 初始化一个列表，用于保存识别到的情绪
                    emo_txt = []

                    # 在检测结果中循环检测
                    # 注意：这里detection为ResNet-SSD网络的输出，与阈值的设置有关，具体可以参考prototxt文件的输出层，输出shape为[1, 1, 200, 7]
                    # 7 表示的含义分别为 [batch Id, class Id, confidence, left, top, right, bottom]
                    # 200 表示检测到的目标数量，具体可参考SSD的论文，针对每幅图像，SSD最终会预测8000多个边界框，通过NMS过滤掉IOU小于0.45的框，剩余200个。
                    for i in np.arange(0, detections.shape[2]):
                        # 提取与预测相关的置信度（即概率），detections的第3维
                        confidence = detections[0, 0, i, 2]

                        # 用于更新相机开关按键信息
                        if not self.cap.isOpened():
                            self.ui.bt_open_camera.setText(u'打开相机')
                        else:
                            self.ui.bt_open_camera.setText(u'关闭相机')


                        # 过滤弱检测
                        if confidence > confidence_default:
                            # 计算面部边界框的（x，y）坐标， 对应detections的4,5,6,7维（索引为3-7），含义分别代表：
                            # x_left_bottom, y_left_bottom, x_right_top, y_right_top
                            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            left = detections[0, 0, i, 3] * w
                            top = detections[0, 0, i, 4] * h
                            right = detections[0, 0, i, 5] * w
                            bottom = detections[0, 0, i, 6] * h


                            roi = frame[startY:endY, startX:endX, :]
                            image = cv2.resize(roi, (64, 64))
                            # image = cv2.resize(roi, (300, 300))
                            image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
                            res = exec_net.infer(inputs={input_blob: [image]})
                            prob_emotion = res['prob_emotion']
                            probs = np.reshape(prob_emotion, 5)
                            txt = labels[np.argmax(probs)]
                            # cv2.putText(frame, txt, (np.int32(left), np.int32(top)), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            #            (255, 0, 0), 2)
                            # cv2.rectangle(frame, (np.int32(left), np.int32(top)),
                            #              (np.int32(right), np.int32(bottom)), (0, 0, 255), 2, 8, 0)
                            # print(txt)

                            # 提取面部ROI
                            # 提取人脸的长和宽，本例中为 397 x 289
                            face = frame[startY:endY, startX:endX]
                            (fH, fW) = face.shape[:2]

                            # 确保面部宽度和高度足够大，以过滤掉小人脸(较远)，防止远处人员签到，以及过滤误检测
                            if fW < 100 or fH < 100:
                                continue

                            # 为面部ROI构造一个blob，然后通过面部嵌入模型传递blob以获得面部的128-d量化
                            # shape 为 (1, 3, 96, 96)
                            face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                              (96, 96),  # 调整到 96 x 96 像素
                                                              (0, 0, 0), swapRB=True, crop=False)
                            # 传入到 FaceNet人脸识别模型中，将 96 x 96 x 3 的人脸图像转换为128维度的向量
                            embedded.setInput(face_blob)
                            # 128 维的向量，shape=(1, 128)
                            vec = embedded.forward()
                            # 使用SVM对人脸向量进行分类
                            # prediction 为一向量，其shape的第一个维度为人脸库中ID的数量，返回分类概率的列表
                            prediction = recognizer.predict_proba(vec)[0]
                            # 取概率最大的索引
                            j = np.argmax(prediction)
                            # 得到预测概率
                            probability = prediction[j]
                            # 通过索引j找到人名(ID)转化为one-hot编码前的真实名称，也就是人脸数据集的文件夹名称，亦即数据库中ID字段的值
                            name = le.classes_[j]

                            # 统计各人脸被检测到的次数
                            self.face_name_dict[name] += 1

                            # 绘制面部的边界框以及相关的概率
                            text = "{}: {:.2f}%".format(name, probability * 100)
                            # 构造人脸边界框
                            y = startY - 10 if startY - 10 > 10 else startY + 10
                            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                            frame = cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255),
                                                2)
                            face_names.append(name)
                            emo_txt.append(txt)
                            # print(face_names)
                            # print(emo_txt)
                            # 统计各情绪数量
                            emo_count = Counter(emo_txt)
                            emo_len = len(emo_txt)
                            step1 = step2 = step3 =step4 = step5 = 0
                            for k, v in emo_count.items():
                                if k == 'happy':
                                    step1 = 1
                                    self.ui.label_emo1_1.setText(str(round((v/emo_len)*100,2))+'%')
                                if k == 'sad':
                                    step2 = 2
                                    self.ui.label_emo2_2.setText(str(round((v/emo_len)*100,2))+'%')
                                if k == 'surprise':
                                    step3 = 3
                                    self.ui.label_emo3_3.setText(str(round((v/emo_len)*100,2))+'%')
                                if k == 'neutral':
                                    step4 = 4
                                    self.ui.label_emo6_6.setText(str(round((v/emo_len)*100,2))+'%')
                                if k == 'anger':
                                    step5 = 5
                                    self.ui.label_emo4_4.setText(str(round((v/emo_len)*100,2))+'%')
                            # 刷新界面
                            if step1 == 0:
                                self.ui.label_emo1_1.setText('0.00%')
                            if step2 == 0:
                                self.ui.label_emo2_2.setText('0.00%')
                            if step3 == 0:
                                self.ui.label_emo3_3.setText('0.00%')
                            if step4 == 0:
                                self.ui.label_emo6_6.setText('0.00%')
                            if step5 == 0:
                                self.ui.label_emo4_4.setText('0.00%')

                    # bt_liveness = self.ui.bt_blinks.text()
                    # if bt_liveness == '停止检测':
                    #     ChineseText = PutChineseText.put_chinese_text('./utils2/microsoft.ttf')
                    #     frame = ChineseText.draw_text(frame, (330, 80), ' 请眨眨眼睛 ', 25, (55, 255, 55))

                    # 显示输出框架
                    show_video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                    # opencv读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage。
                    # QImage(uchar * data, int width, int height, int bytesPerLine, Format format)
                    self.showImage = QImage(show_video.data, show_video.shape[1], show_video.shape[0],
                                            QImage.Format_RGB888)
                    self.ui.label_camera.setPixmap(QPixmap.fromImage(self.showImage))

                    if loop_num == FR_LOOP_NUM:
                        # print(self.face_name_dict)
                        # print(face_names)
                        # 找到10帧中检测次数最多的人脸
                        # Python字典按照值的大小降序排列，并返回键值对元组
                        # 第一个索引[0]表示取排序后的第一个键值对，第二个索引[0]表示取键
                        most_id_in_dict = \
                            sorted(self.face_name_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][0]
                        # 将当前帧检测到次数最多的人脸保存到self.set_name集合中
                        self.set_name = set()
                        self.set_name.add(most_id_in_dict)
                        # self.set_name = set(face_names)
                        self.set_names = tuple(self.set_name)
                        # print(self.set_name, self.set_names)

                        self.record_names()
                        self.face_name_dict = dict(zip(le.classes_, len(le.classes_) * [0]))
                        loop_num = 0
                    else:
                        pass
                else:
                    self.cap.release()

            # 因为最后一张画面会显示在GUI中，此处实现清除。
            self.ui.label_camera.clear()

    def record_names(self):
        # 如果self.set_names是self.record_names 的子集返回ture
        if self.set_name.issubset(self.record_name):
            pass  # record_name1是要写进数据库中的名字信息 set_name是从摄像头中读出人脸的tuple形式
        else:
            # 获取到self.set_name有而self.record_name无的名字
            self.different_name = self.set_name.difference(self.record_name)
            # 把self.record_name变成两个集合的并集
            self.record_name = self.set_name.union(self.record_name)
            # different_name是为了获取到之前没有捕捉到的人脸，并再次将record_name1进行更新

            # 将集合变成tuple，并统计人数
            self.write_data = tuple(self.different_name)
            names_num = len(self.write_data)
            # # 显示签到人数
            # self.ui.lcd_2.display(len(self.record_name))

            if names_num > 0:
                # 将签到信息写入数据库
                self.line_text_info = []
                try:
                    # 打开数据库连接
                    db, cursor = connect_to_sql()
                except ConnectionError as e:
                    print("[Error] 数据库连接失败！")
                else:
                    # 获取系统时间，保存到秒
                    current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    results2 = self.use_id_get_info(self.write_data[0])

                    # 判断是否迟到，在这里只考虑正常情况，没有没有设置考勤时间的按钮
                    self.now = datetime.now()
                    # self.attendance_state = attendance_check(self.check_time_set)
                    self.attendance_state = '正常'
                    self.line_text_info.append((results2[0], results2[1], results2[2],
                                                current_time,
                                                self.attendance_state))
                    print(self.line_text_info)

                # 写入数据库
                try:
                    # 如果存在数据，先删除再写入。前提是设置唯一索引字段或者主键。
                    insert_sql2 = "replace into checkin(Name, ID, Class, Time, Description) values(%s, %s, %s, %s, %s)"
                    users2 = self.line_text_info
                    cursor.executemany(insert_sql2, users2)
                except ConnectionAbortedError as e:
                    self.ui.textBrowser_log.append("[INFO] 数据库写入失败!")
                else:
                    self.ui.textBrowser_log.append("[INFO] 数据库写入成功!")
                    # QMessageBox.information(self, "Tips", "签到成功，请勿重复操作！", QMessageBox.Ok)
                finally:
                    # 提交到数据库执行
                    db.commit()
                    cursor.close()
                    db.close()

    # # 查询班级人数
    # def check_nums(self):
    #     # 选择的班级
    #     global db
    #     input_class = self.ui.comboBox_class.currentText()
    #     # print("[INFO] 你当前选择的班级为:", input_class)
    #     if input_class != '':
    #         try:
    #             # 打开数据库连接, 使用cursor()方法获取操作游标
    #             db, cursor = connect_to_sql()
    #         except ValueError:
    #             self.ui.textBrowser_log.append("[ERROR] 连接数据库失败！")
    #         else:
    #             self.ui.textBrowser_log.append("[INFO] 连接数据库成功，正在执行查询...")
    #             # 查询语句，实现通过ID关键字检索个人信息的功能
    #             sql = "select * from studentnums where class = {}".format(input_class)
    #             cursor.execute(sql)
    #             # 获取所有记录列表
    #             results = cursor.fetchall()
    #             self.nums = []
    #             for i in results:
    #                 self.nums.append(i[1])
    #
    #             # 用于查询每班的实到人数
    #             sql2 = "select * from checkin where class = {}".format(input_class)
    #             cursor.execute(sql2)
    #
    #             # 获取所有记录列表
    #             results2 = cursor.fetchall()
    #             self.ui.textBrowser_log.append("[INFO] 查询成功！")
    #
    #             # 设定考勤时间
    #             self.check_time_set = self.format_check_time_set()
    #
    #             if self.check_time_set != '':
    #                 QMessageBox.information(self, "Tips", "您设定的考勤时间为{}".format(self.check_time_set), QMessageBox.Ok)
    #
    #                 have_checked_id = self.process_check_log(results2)
    #                 self.nums2 = len(np.unique(have_checked_id))
    #                 # print(self.nums2)
    #
    #             else:
    #                 QMessageBox.warning(self, "Warning", "请先设定考勤时间(例 08:00)！", QMessageBox.Ok)
    #
    #         finally:
    #             # lcd控件显示人数
    #             self.ui.lcd_1.display(self.nums[0])
    #             self.ui.lcd_2.display(self.nums2)
    #             # 关闭数据库连接
    #             db.close()

    # # 格式化设定的考勤时间
    # def format_check_time_set(self):
    #     """
    #     格式化考勤时间，方便比较
    #     :return: datetime.datetime格式，相见之后为timedelta格式，具有seconds，hours，minutes，days属性
    #     """
    #     # 获取完整的时间格式
    #     now = datetime.now()
    #     # 分别获取当前的年，月，日，时，分，秒，均为int类型
    #     judg_time = now
    #     now_y = judg_time.year
    #     now_m = judg_time.month
    #     now_d = judg_time.day
    #
    #     original_hour = str(self.ui.spinBox_time_hour.text())
    #     original_minute = str(self.ui.spinBox_time_minute.text())
    #     condition_hour = int(self.ui.spinBox_time_hour.text())
    #     condition_minute = int(self.ui.spinBox_time_minute.text())
    #
    #     if condition_hour < 10 and condition_minute < 10:
    #         check_time_set = "0" + original_hour + ":" + "0" + original_minute + ":" + "00"
    #     elif condition_hour < 10 and condition_minute >= 10:
    #         check_time_set = "0" + original_hour + ":" + original_minute + ":" + "00"
    #     elif condition_hour >= 10 and condition_minute < 10:
    #         check_time_set = original_hour + ":" + "0" + original_minute + ":" + "00"
    #     elif condition_hour >= 10 and condition_minute >= 10:
    #         check_time_set = original_hour + ":" + original_minute + ":" + "00"
    #     else:
    #         check_time_set = "08:00:00"
    #
    #     # 格式化考勤时间
    #     att_time = datetime.strptime(f'{now_y}-{now_m}-{now_d} {check_time_set}', '%Y-%m-%d %H:%M:%S')
    #
    #     return att_time

    # # 从结果中筛选已经签到的人数
    # def process_check_log(self, results):
    #     # 从所有考勤记录中筛选考勤时间之后的记录，并针对id取unique操作
    #     have_checked_id = []
    #     for item in results:
    #         # item[3]为每条考勤记录的考勤时间
    #         # 如果打卡时间 - 考勤时间设定 在考勤时间截止前1小时和一节大课之间内 则统计考勤记录
    #         if (abs((item[3] - self.check_time_set).seconds) < 60 * 60) or (item[3] - self.check_time_set).seconds > 0:
    #             have_checked_id.append(int(item[1]))
    #     return have_checked_id

    # 请假/补签登记
    def leave_button(self):
        self.leave_students(1)

    def supplyment_button(self):
        self.leave_students(2)

    def leave_students(self, button):
        global results
        self.lineTextInfo = []
        # 为防止输入为空卡死，先进行是否输入数据的判断
        if self.ui.lineEdit_leave.isModified() or self.ui.lineEdit_supplement.isModified():
            # 打开数据库连接
            db, cursor = connect_to_sql()
            # 获取系统时间，保存到秒
            currentTime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if button == 1:
                self.ui.textBrowser_log.append("[INFO] 正在执行请假登记...")
                self.description = "请假"
                self.lineText_leave_id = self.ui.lineEdit_leave.text()
                results = self.use_id_get_info(self.lineText_leave_id)
            elif button == 2:
                self.ui.textBrowser_log.append("[INFO] 正在执行漏签补签...")
                self.description = "漏签补签"
                self.lineText_leave_id = self.ui.lineEdit_supplement.text()
                results = self.use_id_get_info(self.lineText_leave_id)
            else:
                print("[Error] The value of button must be one or two!")

            if len(results) != 0:
                try:
                    self.ui.textBrowser_log.append("[INFO] 正在从数据库获取当前用户信息...")
                    print(results[0], results[1], results[2], currentTime, self.description)
                    self.lineTextInfo.append((results[0], results[1], results[2],
                                                currentTime,
                                                self.description))
                except ConnectionAbortedError as e:
                    self.ui.textBrowser_log.append("[INFO] 从数据库获取信息失败，请保证当前用户的信息和考勤记录已录入数据库！", e)
                # 写入数据库
                try:
                    # 如果存在数据，先删除再写入。前提是设置唯一索引字段或者主键。
                    insert_sql = "replace into checkin(Name, ID, Class, Time, Description) values(%s, %s, %s, %s, %s)"
                    users = self.lineTextInfo
                    cursor.executemany(insert_sql, users)
                except ValueError as e:
                    self.ui.textBrowser_log.append("[INFO] 写入数据库失败！", e)
                else:
                    self.ui.textBrowser_log.append("[INFO] 写入数据库成功！")
                    QMessageBox.warning(self, "Warning", "{} {}登记成功，请勿重复操作！".format(self.lineText_leave_id,
                                                                                    self.description), QMessageBox.Ok)
                finally:
                    # 提交到数据库执行
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                QMessageBox.critical(self, "Error", f"您输入的ID {self.lineText_leave_id} 不存在！请先录入数据库！")
        else:
            QMessageBox.critical(self, "Error", "学号不能为空，请输入后重试！", QMessageBox.Ok)  # (QMessageBox.Yes | QMessageBox.No)
        # 输入框清零
        self.ui.lineEdit_leave.clear()
        self.ui.lineEdit_supplement.clear()

    # # 考勤结束后，将班级内未签到的学生设为旷课
    # def set_rest_absenteeism(self):
    #     pass

    # 核验本地人脸与数据库信息是否一致
    def check_variation_db(self):
        try:
            db, cursor = connect_to_sql()
        except ConnectionAbortedError as e:
            self.ui.textBrowser_log.append('[INFO] 连接数据库失败，请检查配置信息！')
        else:
            sql = "select id, name from students"
            # 执行查询
            cursor.execute(sql)
            results = cursor.fetchall()
            self.student_ids = []
            self.student_names = []
            for item in results:
                self.student_ids.append(item[0])
                self.student_names.append(item[1])
            # 初始化点名列表
            # self.random_check_names = deepcopy(self.student_names)
            # self.random_check_ids = deepcopy(self.student_ids)
            print('[INFO] 当前班级内的成员包括：', self.student_ids, self.student_names)
            # 统计本地人脸数据信息
            num_dict = statical_facedata_nums()
            # ID
            self.keys = []
            for key in list(num_dict.keys()):
                self.keys.append(int(key))
            # print(set(self.student_ids))
            # print(set(self.keys))
            self.check_variation_set_operate()
        finally:
            db.commit()
            cursor.close()
            db.close()

    def check_variation_set_operate(self):
        # 并集
        union_set = set(self.student_ids).union(set(self.keys))
        # 交集
        inter_set = set(self.student_ids).intersection(set(self.keys))
        # 差集
        two_diff_set = set(self.student_ids).difference(set(self.keys))
        # 本地与数据库不同的ID
        local_diff_set = union_set - set(self.student_ids)
        # 数据库与本地不同的ID
        db_diff_set = union_set - set(self.keys)

        if len(union_set) == 0:
            # QMessageBox.critical(self, "Error", "本地人脸库名称与数据库均未录入信息，请先录入！", QMessageBox.Ok)
            self.ui.textBrowser_log.append('[Error] 本地人脸库名称与数据库均未录入信息，请先录入！')
            print('[Error] union_set:', union_set)
        elif len(inter_set) == 0 and len(union_set) != 0:
            # QMessageBox.critical(self, "Error", "本地人脸库名称与数据库完全不一致，请先修改！", QMessageBox.Ok)
            self.ui.textBrowser_log.append('[Error] 本地人脸库名称与数据库完全不一致，请先修改！')
            print('[Error] inter_set:', inter_set)
        elif len(two_diff_set) == 0 and len(union_set) != 0:
            # QMessageBox.information(self, "Success", "核验完成，未发现问题！", QMessageBox.Ok)
            self.ui.textBrowser_log.append('[Success] 核验完成，未发现问题！')
            print('[Success] two_diff_set:', two_diff_set)

        elif len(local_diff_set) != 0:
            # QMessageBox.warning(self, "Warning", "数据库中以下ID的人脸信息还未采集，请抓紧采集！", QMessageBox.Ok)
            self.ui.textBrowser_log.append('[Warning] 数据库中以下ID的人脸信息还未采集，请抓紧采集！')
            self.ui.textBrowser_log.append(str(local_diff_set))
            print('[Warning] local_diff_set:', local_diff_set)
        elif len(db_diff_set) != 0:
            # QMessageBox.warning(self, "Warning", "本地人脸以下ID的信息还未录入数据库，请抓紧录入！", QMessageBox.Ok)
            self.ui.textBrowser_log.append('[Warning] 本地人脸以下ID的信息还未录入数据库，请抓紧录入！')
            self.ui.textBrowser_log.append(str(db_diff_set))
            print('[Warning] db_diff_set:', db_diff_set)

    # 使用ID当索引找到其它信息
    def use_id_get_info(self, ID):
        global cursor, db
        if ID != '':
            try:
                # 打开数据库连接
                db, cursor = connect_to_sql()
                # 查询语句，实现通过ID关键字检索个人信息的功能
                sql = "select * from students where ID = {}".format(ID)
                # 执行查询
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
                self.check_info = []
                for i in results:
                    self.check_info.append(i[1])
                    self.check_info.append(i[0])
                    self.check_info.append(i[2])
                return self.check_info
            except ConnectionAbortedError as e:
                self.ui.textBrowser_log.append("[ERROR] 数据库连接失败！")
            finally:
                cursor.close()
                db.close()

    # # 显示迟到和未到
    # def show_late_absence(self):
    #     db, cursor = connect_to_sql()
    #     # 一定要注意字符串在检索时要加''！
    #     sql1 = "select name from checkin where Description = '{}'".format('迟到')
    #     sql2 = "select name from students"
    #     try:
    #         cursor.execute(sql1)
    #         results = cursor.fetchall()
    #         self.late_students = []
    #         for x in results:
    #             self.late_students.append(x[0])
    #         self.late_students.sort()
    #         # self.ui.textBrowser_log.append(self.late_students)
    #     except ConnectionAbortedError as e:
    #         self.ui.textBrowser_log.append('[INFO] 查询迟到数据失败', e)
    #
    #     try:
    #         cursor.execute(sql2)
    #         results2 = cursor.fetchall()
    #         self.students_id = []
    #         for i in results2:
    #             self.students_id.append(i[0])
    #         self.students_id.sort()
    #         print(self.students_id)
    #     except ConnectionAbortedError as e:
    #         self.ui.textBrowser_log.append('[INFO] 查询未到数据失败', e)
    #
    #     finally:
    #         db.commit()
    #         cursor.close()
    #         db.close()
    #
    #     # 集合运算，算出未到的和迟到的
    #     self.absence_nums = set(set(self.students_id) - set(self.late_students))
    #     self.absence_nums = list(self.absence_nums)
    #     self.absence_nums.sort()
    #
    #     # # 在控件中显示未到的同学
    #     # n_row_late = len(self.late_students)
    #     # n_row_absence= len(self.absence_nums)
    #     # model1 = QtGui.QStandardItemModel(n_row_late, 0)
    #     # # 设置数据行、列标题
    #     # model1.setHorizontalHeaderLabels(['姓名'])
    #     # # 设置填入数据内容
    #     # for row in range(n_row_late):
    #     #     item = QtGui.QStandardItem(self.late_students[row])
    #     #     # 设置每个位置的文本值
    #     #     model1.setItem(row, 0, item)
    #     # # 指定显示的tableView控件，实例化表格视图
    #     # table_view1 = self.ui.tableView_escape
    #     # table_view1.setModel(model1)
    #
    #     # # 迟到显示
    #     # module2 = QtGui.QStandardItemModel(rowAbsentee, 0)
    #     # # 设置数据行、列标题
    #     # module2.setHorizontalHeaderLabels(['姓名'])
    #     # # 设置填入数据内容
    #     # for row in range(rowAbsentee):
    #     #     item = QtGui.QStandardItem(self.absence_nums[row])
    #     #     # 设置每个位置的文本值
    #     #     module2.setItem(row, 0, item)
    #     # # 指定显示的tableView控件，实例化表格视图
    #     # table_view2 = self.ui.tableView_late
    #     # table_view2.setModel(module2)

    # 训练人脸识别模型，静态方法
    # @staticmethod
    def train_model(self):
        q_message = QMessageBox.information(self, "Tips", "你确定要重新训练模型吗？", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes == q_message:
            GeneratorModel.Generator()
            GeneratorModel.TrainModel()
            self.ui.textBrowser_log.append('[INFO] 模型训练完成!')
        else:
            self.ui.textBrowser_log.append('[INFO] 取消模型进程!')

    def open_info_dialog(self):
        if self.cap.isOpened():
            QMessageBox.warning(self, "Warning", "为防止摄像头冲突，已自动关闭摄像头！", QMessageBox.Ok)
            self.cap.release()

    def quit_window(self):
        if self.cap.isOpened():
            self.cap.release()
        QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建并显示窗口
    mainWindow = MainWindow()
    infoWindow = InfoDialog()
    rcWindow = RCDialog()
    mainWindow.ui.bt_gathering.clicked.connect(infoWindow.handle_click)
    mainWindow.ui.bt_random_check.clicked.connect(rcWindow.handle_click)
    mainWindow.show()
    sys.exit(app.exec_())
