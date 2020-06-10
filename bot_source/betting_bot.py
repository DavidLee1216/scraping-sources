# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import xlrd
import auto_betting
from selenium import webdriver

driver = webdriver.Chrome(executable_path='./chromedrive/chromedriver.exe')
driver.maximize_window()

class UsernamePassword:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(665, 270)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 40, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(180, 35, 191, 30))
        self.comboBox.setObjectName("comboBox")
        self.loginButton = QtWidgets.QPushButton(Dialog)
        self.loginButton.setGeometry(QtCore.QRect(180, 80, 100, 40))
        self.loginButton.setFont(font)
        self.loginButton.setObjectName("LoginButton")
        self.loginButton.clicked.connect(self.login)
        self.logoutButton = QtWidgets.QPushButton(Dialog)
        self.logoutButton.setGeometry(QtCore.QRect(300, 80, 100, 40))
        self.logoutButton.setFont(font)
        self.logoutButton.setObjectName("LogoutButton")
        self.logoutButton.clicked.connect(self.logout)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 210, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start_betting)
        self.closeButton = QtWidgets.QPushButton(Dialog)
        self.closeButton.setGeometry(QtCore.QRect(300, 210, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close)

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(180, 150, 341, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(530, 150, 75, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.setExcelFile)

        self.loadUsername()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username"))
        self.pushButton.setText(_translate("Dialog", "Start"))
        self.closeButton.setText(_translate("Dialog", "Close"))
        self.label_2.setText(_translate("Dialog", "Filename"))
        self.pushButton_2.setText(_translate("Dialog", "Select Excel"))
        self.loginButton.setText(_translate("Dialog", "Login"))
        self.logoutButton.setText(_translate("Dialog", "Logout"))

    def setExcelFile(self):
        filename = self.openFileNameDialog()
        self.lineEdit.setText(filename)

    def loadUsername(self):
        sheet = auto_betting.get_excel_sheet_object('login.xlsx')
        self.userdata = []
        for i in range(1, sheet.nrows):
            username = sheet.cell(i, 0).value
            password = sheet.cell(i, 1).value
            userdata = UsernamePassword(username, password)
            self.userdata.append(userdata)
            self.comboBox.addItem(username)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Choose File", "","excel Files (*.xlsx *.xls)", options=options)
        return fileName

    def getPassword(self, username):
        for user in self.userdata:
            if user.username==username:
                return user.password
        return None

    def login(self):
        username = self.comboBox.currentText()
        password = self.getPassword(username)
        bLogged = auto_betting.login(driver, "https://www.zeturf.com", username, password)
        if bLogged:
            pass
        else:
            self.show_message('Warning', 'Log in failed')

    def logout(self):
        auto_betting.logout(driver)

    def close(self):
        if driver:
            driver.close()
        app.exit()

    def start_betting(self):
        driver.maximize_window()
        driver.set_page_load_timeout(50)
        filename = self.lineEdit.text()
        auto_betting.bet(driver, filename)
        self.show_message("Message", "Betting Completed!")

    def show_message(self, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    driver.close()
