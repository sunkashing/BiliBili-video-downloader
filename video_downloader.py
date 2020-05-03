import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDesktopWidget, QFrame

import bilibili
from video_downloader_GUI import MyWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())
