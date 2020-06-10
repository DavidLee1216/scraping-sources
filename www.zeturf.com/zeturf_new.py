# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import scraping
import datetime
from selenium import webdriver

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(410, 248)
        self.RacingTypeCombo = QtWidgets.QComboBox(Dialog)
        self.RacingTypeCombo.setGeometry(QtCore.QRect(120, 33, 191, 25))
        self.RacingTypeCombo.setObjectName("RacingTypeCombo")
        self.DateFrom = QtWidgets.QDateEdit(Dialog)
        self.DateFrom.setGeometry(QtCore.QRect(80, 80, 110, 25))
        self.DateFrom.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        self.DateFrom.setObjectName("DateFrom")
        self.DateTo = QtWidgets.QDateEdit(Dialog)
        self.DateTo.setGeometry(QtCore.QRect(250, 80, 110, 25))
        self.DateTo.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.DateTo.setObjectName("DateTo")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 36, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 82, 45, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(200, 85, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 130, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.FilenameEdit = QtWidgets.QLineEdit(Dialog)
        self.FilenameEdit.setGeometry(QtCore.QRect(80, 125, 251, 25))
        self.FilenameEdit.setObjectName("FilenameEdit")
        self.ButtonSelFile = QtWidgets.QPushButton(Dialog)
        self.ButtonSelFile.setGeometry(QtCore.QRect(340, 125, 41, 25))
        self.ButtonSelFile.setObjectName("ButtonSelFile")
        self.ButtonSelFile.clicked.connect(self.select_file_clicked)
        self.ButtonStart = QtWidgets.QPushButton(Dialog)
        self.ButtonStart.setGeometry(QtCore.QRect(100, 180, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonStart.setFont(font)
        self.ButtonStart.setObjectName("ButtonStart")
        self.ButtonStart.clicked.connect(self.start_clicked)
        self.ButtonClose = QtWidgets.QPushButton(Dialog)
        self.ButtonClose.setGeometry(QtCore.QRect(220, 180, 75, 25))
        self.ButtonClose.clicked.connect(self.close_clicked)

        font = QtGui.QFont()
        font.setPointSize(10)
        self.ButtonClose.setFont(font)
        self.ButtonClose.setObjectName("ButtonClose")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.add_racing_types()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Racing Type"))
        self.label_2.setText(_translate("Dialog", "From"))
        self.label_3.setText(_translate("Dialog", "To"))
        self.label_4.setText(_translate("Dialog", "File"))
        self.ButtonSelFile.setText(_translate("Dialog", "..."))
        self.ButtonStart.setText(_translate("Dialog", "Start"))
        self.ButtonClose.setText(_translate("Dialog", "Close"))

    def select_file_clicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"Choose File", "","excel Files (*.xlsx *.xls)", options=options)
        ext = fileName.rsplit(".", 1)
        if len(ext)==2 and (ext[1]!='xlsx' and ext[1]!='xls'):
            fileName += ".xlsx"
        elif len(ext)==1:
            fileName += ".xlsx"
        self.FilenameEdit.setText(fileName)

    def close_clicked(self):
        app.exit()

    def start_clicked(self):
        driver = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
        driver.set_page_load_timeout(50)
        url = "https://www.zeturf.com/en/resultats-et-rapports/archives"
        filename = self.FilenameEdit.text()
        if filename=="":
            self.show_message("Warning", "Please select excel file")
            return
        ext = filename.rsplit(".", 1)
        if len(ext)==1 or (len(ext)==2 and (ext[1]!='xlsx' and ext[1]!='xls')):
            self.show_message("Warning", "Please select right excel file")
            return
        racing_type = self.RacingTypeCombo.currentText()
        date_from = datetime.date(self.DateFrom.date().year(), self.DateFrom.date().month(), self.DateFrom.date().day())
        date_to = datetime.date(self.DateTo.date().year(), self.DateTo.date().month(), self.DateTo.date().day())
        curr_date = datetime.date.today()
        if date_from>=curr_date or date_to>=curr_date:
            self.show_message("Warning", "Date must be before today")
            return
        elif date_to < date_from:
            self.show_message("Warning", "Date 'From' must be before or equal to Date 'To'")
            return
        scraping.start(driver, url, filename, date_from, date_to, racing_type)
        driver.close()
        self.show_message('Success', 'Scraping successfully completed')

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def add_racing_types(self):
        self.RacingTypeCombo.addItem("All")
        self.RacingTypeCombo.addItem("Harness")
        self.RacingTypeCombo.addItem("Flat")
        self.RacingTypeCombo.addItem("Monte")
        self.RacingTypeCombo.addItem("Hurdle")
        self.RacingTypeCombo.addItem("Steeplechase")
        self.RacingTypeCombo.addItem("Jump")
        self.RacingTypeCombo.setCurrentIndex(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()
