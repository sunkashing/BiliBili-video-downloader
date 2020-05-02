import urllib.request

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget, QFrame, QFileDialog, QLabel

import bilibili


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.title = "Bilibili video downloader"
        self.container = QtWidgets.QVBoxLayout()
        self.BV_input = QtWidgets.QLineEdit()
        self.download_button = QtWidgets.QPushButton('Download')
        self.init_BV_box()
        self.output_directory = QtWidgets.QLineEdit()
        self.init_output_box()
        # self.container.addStretch()
        self.process = QtWidgets.QPlainTextEdit()
        self.error = QtWidgets.QPlainTextEdit()
        self.init_option_result_box()
        self.container.addStretch()
        self.setLayout(self.container)
        self.initUI()

    def init_BV_box(self):
        BV_widget = QtWidgets.QWidget()
        BV_box = QtWidgets.QHBoxLayout(BV_widget)
        BV_box.addWidget(QtWidgets.QLabel('BV number: '))
        BV_box.addWidget(self.BV_input)
        BV_box.addWidget(self.download_button)
        BV_widget.setFixedHeight(60)
        self.container.addWidget(BV_widget)
        self.download_button.clicked.connect(self.download_action)
        self.container.addWidget(QHLine())

    def init_output_box(self):
        output_widget = QtWidgets.QWidget()
        output_box = QtWidgets.QHBoxLayout(output_widget)
        # output_box.addWidget(QtWidgets.QLabel('Choose output folder: '))
        chooseButton = QtWidgets.QPushButton()
        chooseButton.setObjectName("chooseButton")

        output_box.addWidget(self.output_directory)

        chooseButton.setText("Choose Directory")
        output_box.addWidget(chooseButton)
        chooseButton.clicked.connect(self.openfile)
        self.output_directory.setReadOnly(True)

        output_widget.setFixedHeight(60)
        self.container.addWidget(output_widget)
        self.container.addWidget(QHLine())

    def openfile(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        self.output_directory.setText(directory)

    def init_option_result_box(self):
        option_result_widget = QtWidgets.QWidget()
        option_result_box = QtWidgets.QHBoxLayout(option_result_widget)
        self.init_options_box(option_result_box)
        option_result_box.addWidget(QVLine())
        self.init_result_box(option_result_box)
        option_result_widget.setFixedHeight(500)
        self.container.addWidget(option_result_widget)

    def init_options_box(self, option_result_box):
        options_widget = QtWidgets.QWidget()
        options_box = QtWidgets.QVBoxLayout(options_widget)
        self.init_option(options_box, QtWidgets.QLabel('Merge'))
        options_box.addWidget(QHLine())
        self.init_option(options_box, QtWidgets.QLabel('danmaku'))
        options_box.addStretch()
        options_widget.setFixedWidth(150)
        option_result_box.addWidget(options_widget)

    def init_option(self, options_box, option):
        option_box = QtWidgets.QHBoxLayout()
        option_box.addWidget(option)
        option_box.addStretch()
        option_box.addWidget(QtWidgets.QCheckBox())
        options_box.addLayout(option_box)

    def init_result_box(self, option_result_box):
        result_box = QtWidgets.QVBoxLayout()
        self.init_video_infos_box(result_box)
        result_box.addWidget(self.process)
        self.process.setReadOnly(True)
        self.process.setFixedHeight(150)
        result_box.addWidget(self.error)
        self.error.setReadOnly(True)
        self.error.setFixedHeight(100)
        option_result_box.addLayout(result_box)

    def init_video_infos_box(self, result_box):
        video_infos_widget = QtWidgets.QWidget()
        video_infos_box = QtWidgets.QHBoxLayout(video_infos_widget)
        url = 'http://i0.hdslb.com/bfs/archive/317697965235f5beb2cb06a85829389f4d16dab8.jpg'
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        picSize = QSize(200, 400)
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(picSize, QtCore.Qt.KeepAspectRatio)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(QtCore.Qt.AlignCenter)
        video_infos_box.addWidget(label)
        video_infos_box.addWidget(QVLine())
        infos_box = QtWidgets.QVBoxLayout()
        self.init_info(infos_box, 'name: ', 'xxx')
        self.init_info(infos_box, 'size: ', 'xxx')
        video_infos_box.addLayout(infos_box)
        video_infos_widget.setFixedHeight(200)
        result_box.addWidget(video_infos_widget)

    def init_info(self, infos_box, info_name, info):
        info_box = QtWidgets.QHBoxLayout()
        info_box.addWidget(QtWidgets.QLabel(info_name))
        info_box.addWidget(QtWidgets.QLabel(info))
        infos_box.addLayout(info_box)

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.center()
        self.resize(700, 700)
        self.show()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def download_action(self):
        is_valid = self.check_valid_input()
        if is_valid is not True:
            self.error_print(is_valid)
        else:
            self.error.setPlainText('')


    def check_valid_input(self):
        if self.BV_input.text().strip() == '':
            return self.BV_input
        if self.output_directory.text().strip() == '':
            return self.output_directory
        return True

    def error_print(self, error_object):
        if error_object is self.BV_input:
            self.error.setPlainText('Your BV number is not valid.')
        elif error_object is self.output_directory:
            self.error.setPlainText('Your output directory is not valid.')
