# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ice_hockey_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
#from PyQt5.QtGui import QIcon

import ice_hockey
import sport

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(617, 611)

        today = datetime.date.today()
#        print(today)

        self.groupBox_match = QtWidgets.QGroupBox(Dialog)
        self.groupBox_match.setGeometry(QtCore.QRect(40, 20, 541, 331))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_match.setFont(font)
        self.groupBox_match.setObjectName("groupBox_match")

        self.GetMatchResult = QtWidgets.QPushButton(self.groupBox_match)
        self.GetMatchResult.setGeometry(QtCore.QRect(330, 290, 141, 23))
        self.GetMatchResult.setObjectName("GetMatchResult")
        self.GetMatchResult.clicked.connect(self.get_match_result_click)

        # self.comboBox_tournament = QtWidgets.QComboBox(self.groupBox_match)
        # self.comboBox_tournament.setGeometry(QtCore.QRect(140, 90, 151, 22))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.comboBox_tournament.setFont(font)
        # self.comboBox_tournament.setObjectName("comboBox_tournament")
#        self.comboBox_tournament.addItem("Runkosarja")
#        self.comboBox_tournament.addItem("Playoffs")
#        self.comboBox_tournament.addItem("valmistavat_ottelut")

        self.label = QtWidgets.QLabel(self.groupBox_match)
        self.label.setGeometry(QtCore.QRect(30, 90, 87, 19))
        self.label.setMaximumSize(QtCore.QSize(111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.groupBox_date = QtWidgets.QGroupBox(self.groupBox_match)
        self.groupBox_date.setGeometry(QtCore.QRect(30, 170, 451, 101))
        self.groupBox_date.setObjectName("groupBox_date")

        self.checkBox_all_date = QtWidgets.QCheckBox(self.groupBox_date)
        self.checkBox_all_date.setGeometry(QtCore.QRect(50, 30, 121, 17))
        self.checkBox_all_date.setObjectName("checkBox_all_date")
        self.checkBox_all_date.setCheckState(True)
        self.checkBox_all_date.checkState = True
        self.checkBox_all_date.clicked.connect(self.check_box_all_date_click)

        self.label_2 = QtWidgets.QLabel(self.groupBox_date)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.dateEdit_from = QtWidgets.QDateEdit(self.groupBox_date)
        self.dateEdit_from.setGeometry(QtCore.QRect(100, 60, 110, 22))
        self.dateEdit_from.setObjectName("dateEdit_from")
        self.dateEdit_from.setDate(today)
        self.dateEdit_from.setDisabled(True)

        self.label_4 = QtWidgets.QLabel(self.groupBox_date)
        self.label_4.setGeometry(QtCore.QRect(230, 60, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.dateEdit_to = QtWidgets.QDateEdit(self.groupBox_date)
        self.dateEdit_to.setGeometry(QtCore.QRect(280, 60, 110, 22))
        self.dateEdit_to.setObjectName("dateEdit_to")
        self.dateEdit_to.setDate(today)
        self.dateEdit_to.setDisabled(True)


        self.label_3 = QtWidgets.QLabel(self.groupBox_match)
        self.label_3.setGeometry(QtCore.QRect(70, 100, 50, 19))
        self.label_3.setMaximumSize(QtCore.QSize(91, 20))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.comboBox_season = QtWidgets.QComboBox(self.groupBox_match)
        self.comboBox_season.setGeometry(QtCore.QRect(140, 100, 151, 22))
        self.comboBox_season.setObjectName("comboBox_season")

        self.label_5 = QtWidgets.QLabel(self.groupBox_match)
        self.label_5.setGeometry(QtCore.QRect(50, 50, 65, 16))
        self.label_5.setMaximumSize(QtCore.QSize(81, 16))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.textBrowser_excel1 = QtWidgets.QTextEdit(self.groupBox_match)
        self.textBrowser_excel1.setGeometry(QtCore.QRect(140, 40, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser_excel1.setFont(font)
        self.textBrowser_excel1.setObjectName("textBrowser_excel1")
        self.textBrowser_excel1.setReadOnly(True)

        self.pushButton_open1 = QtWidgets.QPushButton(self.groupBox_match)
        self.pushButton_open1.setGeometry(QtCore.QRect(460, 40, 51, 31))
        self.pushButton_open1.setObjectName("pushButton_open1")
        self.pushButton_open1.clicked.connect(self.open_excel1_click)

        self.pushButton_Finish = QtWidgets.QPushButton(Dialog)
        self.pushButton_Finish.setGeometry(QtCore.QRect(260, 570, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_Finish.setFont(font)
        self.pushButton_Finish.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_Finish.setObjectName("pushButton_Finish")
        self.pushButton_Finish.clicked.connect(self.finish_clicked)

        self.groupBox_player = QtWidgets.QGroupBox(Dialog)
        self.groupBox_player.setGeometry(QtCore.QRect(40, 360, 541, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_player.setFont(font)
        self.groupBox_player.setObjectName("groupBox_player")

        self.GetPlayerResult = QtWidgets.QPushButton(self.groupBox_player)
        self.GetPlayerResult.setGeometry(QtCore.QRect(330, 140, 141, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.GetPlayerResult.setFont(font)
        self.GetPlayerResult.setObjectName("GetPlayerResult")
        self.GetPlayerResult.clicked.connect(self.get_player_result_click)

        self.pushButton_open2 = QtWidgets.QPushButton(self.groupBox_player)
        self.pushButton_open2.setGeometry(QtCore.QRect(460, 30, 51, 31))
        self.pushButton_open2.setObjectName("pushButton_open2")
        self.pushButton_open2.clicked.connect(self.open_excel2_click)

        self.textBrowser_excel2 = QtWidgets.QTextEdit(self.groupBox_player)
        self.textBrowser_excel2.setGeometry(QtCore.QRect(140, 30, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textBrowser_excel2.setFont(font)
        self.textBrowser_excel2.setObjectName("textBrowser_excel2")
        self.textBrowser_excel2.setReadOnly(True)

        self.label_6 = QtWidgets.QLabel(self.groupBox_player)
        self.label_6.setGeometry(QtCore.QRect(50, 40, 65, 16))
        self.label_6.setMaximumSize(QtCore.QSize(81, 16))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_player)
        self.label_7.setGeometry(QtCore.QRect(60, 90, 47, 13))
        self.label_7.setObjectName("label_7")

        self.comboBox_inout = QtWidgets.QComboBox(self.groupBox_player)
        self.comboBox_inout.setGeometry(QtCore.QRect(140, 80, 161, 31))
        self.comboBox_inout.setObjectName("comboBox_inout")
        self.comboBox_inout.addItem("all new in/old out")
        self.comboBox_inout.addItem("new in")
        self.comboBox_inout.addItem("old out")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pushButton_Finish, self.GetMatchResult)
        Dialog.setTabOrder(self.GetMatchResult, self.GetPlayerResult)
        Dialog.setTabOrder(self.GetPlayerResult, self.textBrowser_excel1)
        Dialog.setTabOrder(self.textBrowser_excel1, self.pushButton_open1)
        Dialog.setTabOrder(self.pushButton_open1, self.comboBox_season)
        # Dialog.setTabOrder(self.pushButton_open1, self.comboBox_tournament)
        # Dialog.setTabOrder(self.comboBox_tournament, self.comboBox_season)
        Dialog.setTabOrder(self.comboBox_season, self.checkBox_all_date)
        Dialog.setTabOrder(self.checkBox_all_date, self.dateEdit_from)
        Dialog.setTabOrder(self.dateEdit_from, self.dateEdit_to)
        Dialog.setTabOrder(self.dateEdit_to, self.textBrowser_excel2)
        Dialog.setTabOrder(self.textBrowser_excel2, self.pushButton_open2)
        Dialog.setTabOrder(self.pushButton_open2, self.comboBox_inout)

        try:
            tours, seasons = ice_hockey.load_select_items()
            # for tr in tours:
            #     self.comboBox_tournament.addItem(tr)
            for season in seasons:
                self.comboBox_season.addItem(season)
            self.comboBox_season.setCurrentIndex(len(seasons)-1)
        except:
            self.show_message("Error occured during loading web site")

    def comboBox_season_click(self):
        return

    def comboBox_tournament_click(self):
        return

    def comboBox_inout_click(self):
        return

    def show_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def get_match_result_click(self):
        filename = self.textBrowser_excel1.toPlainText()
        if filename == '':
            self.show_message("Please select the excel file for match result")
            return
        # tournament = self.comboBox_tournament.currentText()
        season = self.comboBox_season.currentText()
        all_date_flg = self.checkBox_all_date.checkState
        date_from = datetime.date(self.dateEdit_from.date().year(), self.dateEdit_from.date().month(), self.dateEdit_from.date().day())
        date_to = datetime.date(self.dateEdit_to.date().year(), self.dateEdit_to.date().month(), self.dateEdit_to.date().day())
        res = ice_hockey.get_match_result(filename, season, all_date_flg, date_from, date_to)
        if res == -1:
            self.show_message("Excel file data format is not valid")
        elif res == -2:
            self.show_message("Network connection failed")
        else:
            self.show_message("Successful extracting")
        return
    
    def check_box_all_date_click(self):
        self.checkBox_all_date.checkState = not(self.checkBox_all_date.checkState)
        self.checkBox_all_date.setCheckState(self.checkBox_all_date.checkState)
        if self.checkBox_all_date.checkState==True:
            self.dateEdit_from.setDisabled(True)
            self.dateEdit_to.setDisabled(True)
        else:
            self.dateEdit_from.setEnabled(True)
            self.dateEdit_to.setEnabled(True)
        return

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Choose File", "","All Files (*);;excel Files (*.xlsx|*.xls)", options=options)
#        if fileName:
#            print(fileName)
        return fileName

    def get_player_result_click(self):
        today = datetime.date.today()
        filename = self.textBrowser_excel2.toPlainText()
        if filename == '':
            self.show_message("Please select the excel file for player out/new result")
            return
        this_year = today.year
        past_year = this_year-1
        year_string = str(past_year)+'-'+str(this_year)
        new_out_flg = self.comboBox_inout.currentIndex()
        sport.get_player_out_new_result(year_string, today, filename, new_out_flg)
        self.show_message("Successful extracting")
        return

    def finish_clicked(self):
        ice_hockey.close_driver()
        app.exit()
    
    def open_excel1_click(self):
        filename = self.openFileNameDialog()
        self.textBrowser_excel1.setText(filename)
        return
    
    def open_excel2_click(self):
        filename = self.openFileNameDialog()
        self.textBrowser_excel2.setText(filename)
        return

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_match.setTitle(_translate("Dialog", "Match Result"))
        self.GetMatchResult.setText(_translate("Dialog", "GetMatchResult"))
        # self.label.setText(_translate("Dialog", "Tournament"))
        self.groupBox_date.setTitle(_translate("Dialog", "Date"))
        self.checkBox_all_date.setText(_translate("Dialog", "All Date"))
        self.label_2.setText(_translate("Dialog", "From"))
        self.label_4.setText(_translate("Dialog", "To"))
        self.label_3.setText(_translate("Dialog", "Season"))
        self.label_5.setText(_translate("Dialog", "Excel File"))
        self.pushButton_open1.setText(_translate("Dialog", "Open"))
        self.pushButton_Finish.setText(_translate("Dialog", "Finish"))
        self.groupBox_player.setTitle(_translate("Dialog", "Player new In/old Out Result"))
        self.GetPlayerResult.setText(_translate("Dialog", "Get Player Result"))
        self.pushButton_open2.setText(_translate("Dialog", "Open"))
        self.label_6.setText(_translate("Dialog", "Excel File"))
        self.label_7.setText(_translate("Dialog", "In/Out"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
