import sys
from PyQt5 import QtWidgets, QtCore
from src.video_downloader_GUI import MyWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())
