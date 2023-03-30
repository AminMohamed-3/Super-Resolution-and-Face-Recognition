import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)

from PyQt5.QtWidgets import *
from PySide2.QtWidgets import *

# GUI FILE
from ui_main import Ui_MainWindow

# IMPORT FUNCTIONS
from ui_functions import *
from Esrgan import super_res
from person_detection import detect_person
from age_gender_race import person_characterstics
from face_allignment_recognition import verifyFace
import numpy as np
import cv2
import gc
path = []
res = []
class MainWindow(QMainWindow):

    def __init__(self):
        self.path = path
        self.res = res
        QMainWindow.__init__(self)
        self.path = path
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # define widgets
        QMainWindow.setWindowTitle(self, "Face Super Resolution")
        self.button = self.findChild(QPushButton, "openimage")
        self.button_2 = self.findChild(QPushButton, "result")
        self.label_image = self.findChild(QLabel, "label")
        self.label_image_3 = self.findChild(QLabel, "label_3")
        self.label_txt = self.findChild(QLabel,"label_2")
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.button.clicked.connect(self.upload_image)
        ## PAGES
        self.button_2.clicked.connect(self.pipeline)
        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))


        ## SHOW ==> MAIN WINDOW

        self.show()
        ## ==> END ##

    def upload_image(self):
        File_name = QFileDialog.getOpenFileName(self, "Open file", "D:\\College\\College_Projects\\Gp", "All Files "
                                                                                                            "(*);;PNG "
                                                                                                            "Files ("
                                                                                                            "*.png);; "
                                                                                                            "JPG Files "
                                                                                                            "(*.jpg)")
        # open the image
        self.pixmap = QPixmap(File_name[0])
        # add pic to label
        self.label_image.setPixmap(self.pixmap)

        self.path = File_name[0]
    def show_image(self,path):
        # open the image
        self.pixmap = QPixmap(path)
        # add pic to label
        self.label_image_3.setPixmap(self.pixmap)

    def pipeline(self):
        img_path = self.path
        img_path_2 = 'lr_face_1.png'
        img_2 = cv2.imread(img_path_2)
        sr,path = super_res(img_path)
        self.show_image(path)
        numpy_image = np.array(sr)
        sr_img = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        detected_person, detect_face, flag = detect_person(sr_img)
        if flag:
            predicted_age, predicted_gender, predicted_race = person_characterstics(detect_face)
            print(predicted_age)
            print(predicted_gender)
            print(predicted_race)
            verification = verifyFace(detected_person, img_2)
            print(verification)
            self.res = f"Gender: {predicted_gender}\nAge: {predicted_age}\nRace: {predicted_race}"
            self.label_txt.setText(self.res)
        else:
            print("No detected persons in this image")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())