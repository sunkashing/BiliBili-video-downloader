import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDesktopWidget, QFrame

import bilibili
from video_downloader_GUI import MyWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())

    # context = bilibili.download("https://www.bilibili.com/video/BV1qz4y1R7Qc",
    #                             output_dir='.', merge=True, caption=True, keep_obj=False)
    #
    # if type(context) is int:
    #     print('BV number not found')
    #
    # print(context)
