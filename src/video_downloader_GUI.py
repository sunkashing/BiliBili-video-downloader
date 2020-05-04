import os
import urllib.request

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from PyQt5.QtWidgets import QDesktopWidget, QFrame, QFileDialog, QLabel

from src import bilibili
from src.merge_video_danmaku import Danmaku2ASS

quality_res = {'超清 4K': [3840, 2160], '高清 1080P60': [1920, 1080], '高清 1080P+': [1920, 1080],
               '高清 1080P': [1920, 1080], '高清 720P60': [1280, 720], '高清 720P': [1280, 720],
               '高清 720P (MP4)': [1280, 720], '清晰 480P': [720, 480], '流畅 360P': [480, 360]}


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
        self.cookie_input = QtWidgets.QLineEdit()
        self.init_cookie_box()
        self.output_directory = QtWidgets.QLineEdit()
        self.init_output_box()
        # self.container.addStretch()
        self.pic_label = QLabel()
        self.pixmap = QPixmap()
        self.process = QtWidgets.QPlainTextEdit()
        self.error = QtWidgets.QPlainTextEdit()

        self.video_bvid = QtWidgets.QLineEdit('')
        self.video_title = QtWidgets.QLineEdit('')
        self.video_format = QtWidgets.QLineEdit('')
        self.video_container = QtWidgets.QLineEdit('')
        self.video_quality = QtWidgets.QLineEdit('')
        self.video_size = QtWidgets.QLineEdit('')
        self.video_info = {'bvid': self.video_bvid, 'title': self.video_title, 'container': self.video_container,
                           'quality': self.video_quality, 'size': self.video_size}

        self.option_merge = QtWidgets.QCheckBox()
        self.option_danmaku = QtWidgets.QCheckBox()
        self.option_60fps = QtWidgets.QCheckBox()
        self.options = {'60fps boost': self.option_60fps}

        self.init_option_result_box()
        self.container.addStretch()
        self.setLayout(self.container)
        self.initUI()
        self.mythread = MyThread(self)
        self.download_button.clicked.connect(self.download_action)
        self.mythread.process_signal.connect(self.process_callback)
        self.mythread.error_signal.connect(self.error_callback)
        self.mythread.video_info_signal.connect(self.video_info_callback)
        self.mythread.download_button_enabled.connect(self.download_button_enabled_callback)

    def download_action(self):
        self.download_button.setEnabled(False)
        self.mythread.start()

    def process_callback(self, i):
        if i == '':
            self.process.setPlainText('')
        elif i.startswith('\r'):
            self.process.setFocus()
            cursorPos = self.process.textCursor()
            cursorPos.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
            cursorPos.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            cursorPos.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            cursorPos.removeSelectedText()
            cursorPos.deletePreviousChar()
            # self.process.setTextCursor(storeCursorPos)
            self.process.insertPlainText(i)
        else:
            self.process.appendPlainText(i)
        self.process.ensureCursorVisible()
        return

    def error_callback(self, i):
        self.error_print(i)
        return

    def video_info_callback(self, i):
        if 'initial_state' in i:
            url = str(i['initial_state']['videoData']['pic'])
            data = urllib.request.urlopen(url).read()
            self.pixmap.loadFromData(data)
            self.pixmap = self.pixmap.scaled(QSize(200, 400), QtCore.Qt.KeepAspectRatio)
            self.pic_label.setPixmap(self.pixmap)
            self.pic_label.setAlignment(QtCore.Qt.AlignCenter)

            self.video_bvid.setText(str(i['initial_state']['videoData']['bvid']))
            self.video_title.setText(str(i['initial_state']['videoData']['title']))
        elif 'stream' in i:
            self.video_container.setText(str(i['stream']['container']))
            self.video_quality.setText(str(i['stream']['quality']))
            self.video_size.setText(str(round(int(i['stream']['size']) / 1024 / 1024, 2)) + 'MB')

        return

    def download_button_enabled_callback(self, i):
        if i == 'true':
            self.download_button.setEnabled(True)

    def init_BV_box(self):
        BV_widget = QtWidgets.QWidget()
        BV_box = QtWidgets.QHBoxLayout(BV_widget)
        BV_box.addWidget(QtWidgets.QLabel('BV number: '))
        BV_box.addWidget(self.BV_input)
        BV_box.addWidget(self.download_button)
        BV_widget.setFixedHeight(60)
        self.container.addWidget(BV_widget)
        self.container.addWidget(QHLine())

    def init_cookie_box(self):
        cookie_widget = QtWidgets.QWidget()
        cookie_box = QtWidgets.QHBoxLayout(cookie_widget)
        cookie_box.addWidget(QtWidgets.QLabel('Cookie (optional): '))
        cookie_box.addWidget(self.cookie_input)
        cookie_widget.setFixedHeight(60)
        self.container.addWidget(cookie_widget)
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
        for k, v in self.options.items():
            self.init_option(options_box, k, v)
            options_box.addWidget(QHLine())
        options_box.addStretch()
        options_widget.setFixedWidth(150)
        option_result_box.addWidget(options_widget)

    def init_option(self, options_box, option_label, option):
        option_box = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(option_label)
        option_box.addWidget(label)
        if option_label == '60fps boost':
            label.setToolTip('Required for FFmpeg package, this will take a long time to run if checked!')
        option_box.addStretch()
        option_box.addWidget(option)
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
        url = 'https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg'
        data = urllib.request.urlopen(url).read()
        self.pixmap.loadFromData(data)
        self.pixmap = self.pixmap.scaled(QSize(200, 400), QtCore.Qt.KeepAspectRatio)
        self.pic_label.setPixmap(self.pixmap)
        self.pic_label.setAlignment(QtCore.Qt.AlignCenter)
        video_infos_box.addWidget(self.pic_label)
        video_infos_box.addWidget(QVLine())
        infos_box = QtWidgets.QVBoxLayout()
        for k, v in self.video_info.items():
            self.init_info(infos_box, k, v)
        video_infos_box.addLayout(infos_box)
        video_infos_widget.setFixedHeight(200)
        result_box.addWidget(video_infos_widget)

    def init_info(self, infos_box, info_name_label, info):
        info_box = QtWidgets.QHBoxLayout()
        info_box.addWidget(QtWidgets.QLabel(info_name_label))
        info.setReadOnly(True)
        info_box.addWidget(info)
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

    def error_print(self, error_object):
        if error_object == 'bv':
            self.error.setPlainText('Your BV number is not valid.')
        elif error_object == 'output':
            self.error.setPlainText('Your output directory is not valid.')
        else:
            self.error.setPlainText(error_object)

    def stop_thread(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()


class MyThread(QThread):
    process_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    video_info_signal = pyqtSignal(dict)
    download_button_enabled = pyqtSignal(str)

    def __init__(self, widget):
        super(MyThread, self).__init__()
        self.w = widget

    def run(self):
        is_valid = self.check_valid_input()
        if is_valid is not True:
            self.error_signal.emit(is_valid)
            self.download_button_enabled.emit('true')
            return

        self.error_signal.emit('')
        self.process_signal.emit('')
        self.video_info_signal.emit({})

        options = self.get_options()
        ck = str(self.w.cookie_input.text().strip('"').strip("'"))
        output_dir = self.w.output_directory.text()
        if ck == '':
            ck = 'CURRENT_FNVAL=16'
        # self.error_signal.emit(ck)
        context = bilibili.download(self.w.BV_input.text(), self,
                                    output_dir=output_dir, merge=True, caption=True,
                                    keep_obj=False, cookie=ck)
        # self.error_signal.emit(str(context))
        video_file = context['title'] + '.' + context['stream']['container']
        danmaku_file = '{}.cmt.xml'.format(context['title'])
        danmaku_output_file = '{}.ass'.format(context['title'])
        video_quality = context['stream']['quality']
        Danmaku2ASS(os.path.join(output_dir, danmaku_file), 'autodetect',
                    os.path.join(output_dir, danmaku_output_file),
                    quality_res[video_quality][0], quality_res[video_quality][1],
                    font_size=int(quality_res[video_quality][0] * quality_res[video_quality][1] / 30000),
                    duration_marquee=10)
        if options['60fps boost'] is True:
            try:
                os.system(
                    'ffmpeg -i ' + os.path.join(output_dir, video_file) + ' -filter:v "minterpolate=fps=60" -c:a copy ' +
                    os.path.join(output_dir, context['title'] + '.60fps.' + context['stream']['container']))
            except:
                self.error_signal.emit('No FFmpeg library found in this computer.')

        self.download_button_enabled.emit('true')

    def get_options(self):
        res = {}
        for k, v in self.w.options.items():
            res[k] = v.isChecked()
        return res

    def check_valid_input(self):
        if self.w.BV_input.text().strip() == '':
            return 'bv'
        if self.w.output_directory.text().strip() == '':
            return 'output'
        return True
