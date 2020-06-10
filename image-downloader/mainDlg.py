import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os.path
import image_downloader

class Ui_ImageDownloader(object):
    def setupUi(self, ImageDownloader):
        ImageDownloader.setObjectName("ImageDownloader")
        ImageDownloader.resize(297, 140)
        self.Start = QtWidgets.QPushButton(ImageDownloader)
        self.Start.setGeometry(QtCore.QRect(50, 60, 75, 23))
        self.Start.setObjectName("Start")
        self.Start.clicked.connect(self.start_clicked)

        self.Finish = QtWidgets.QPushButton(ImageDownloader)
        self.Finish.setGeometry(QtCore.QRect(160, 60, 75, 23))
        self.Finish.setObjectName("Finish")
        self.Finish.clicked.connect(self.finish_clicked)

        self.retranslateUi(ImageDownloader)
        QtCore.QMetaObject.connectSlotsByName(ImageDownloader)

    def retranslateUi(self, ImageDownloader):
        _translate = QtCore.QCoreApplication.translate
        ImageDownloader.setWindowTitle(_translate("ImageDownloader", "ImageDownloader"))
        self.Start.setText(_translate("ImageDownloader", "Start"))
        self.Finish.setText(_translate("ImageDownloader", "Finish"))

    def start_clicked(self):
        if not os.path.exists('image_scrap.csv'):
#            self.showDialog()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Image_scrap.csv File ndoes't exist!")
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
        else:
            image_downloader.main('image_scrap.csv')
        return
        
    def finish_clicked(self):
        app.exit()

    def showDialog(self):
        d = QtWidgets.QDialog()
        s = QtWidgets.QLabel("Image_scrap.csv File\ndoes't exist!")
        s.move(20, 20)
        b1 = QtWidgets.QPushButton("ok",d)
        b1.move(50,50)
#        b1.clicked.connect(d.exit())
        d.setWindowTitle("Warning")
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        d.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImageDownloader = QtWidgets.QDialog()
    ui = Ui_ImageDownloader()
    ui.setupUi(ImageDownloader)
    ImageDownloader.show()
    sys.exit(app.exec_())
