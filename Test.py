#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
六合彩号码金额统计程序
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QLineEdit, QPushButton, QHBoxLayout,
                             QGridLayout, QFrame, QDialog, QComboBox, QVBoxLayout, QMessageBox,
                             QDockWidget, QMainWindow, QTableWidget, QAbstractItemView, QHeaderView,
                             QTableWidgetItem)
from PyQt5.QtGui import (QFont, QRegExpValidator)
from PyQt5.QtCore import (Qt, QRegExp)

ROWS_NUM = 12
NUM_MAP = {}

#号码类
class NumberItem(QWidget):
    def __init__(self, num):
        super().__init__()
        self.initUI(num)

    def initUI(self, num):
        self.number_value = num
        self.money = 0
        self.dockWidget = None

        self.history = []

        self.num_label = QLabel("号数：{}      金额：{}￥".format(self.number_value, self.money))
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.num_label.setFont(font)
        # 设置号码信息边框
        self.num_label.setFrameShape(QFrame.Box)
        self.num_label.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")

        layout = QHBoxLayout()
        layout.addWidget(self.num_label)
        self.setLayout(layout)
    #响应鼠标左右键单击事件，显示号码资金历史记录
    def mousePressEvent(self, event):
        if event.button==Qt.LeftButton or event.button==Qt.RightButton:
            self.dockWidget.displayNumberHistory()


    def get_number(self):
        return self.number_value

    def get_money(self):
        return self.money

    def set_money(self, mon):
        self.money = mon
        self.num_label.setText("号数：{}      金额：{}￥".format(self.number_value, self.money))

    def add_money(self, new_monry):
        self.money += new_monry
        self.num_label.setText("号数：{}      金额：{}￥".format(self.number_value, self.money))
        self.history.append(new_monry)

    def minus_money(self, minus):
        self.money -= minus
        self.num_label.setText("号数：{}      金额：{}￥".format(self.number_value, self.money))
        self.history.append(-minus)

    def get_history(self):
        return self.history

#资金历史记录显示dock widget，所有号码历史资金流水
class HistoryDockWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        headers = ['号码', '资金流水记录']
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.horizontalHeader().setFixedHeight(50)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionsClickable(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setWidget(self.tableWidget)

    def displayNumberHistory(self):
        for key in NUM_MAP:
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row+1)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(NUM_MAP[key].get_number()))
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.format_history(NUM_MAP[key].get_history())))

    def format_history(self, h):
        return "    ".join(h)

#交互对话框定义
class EditDialog(QDialog):
    def __init__(self, isAdd):
        super().__init__()
        self.is_add = isAdd
        self.initUI()

    def initUI(self):
        if self.is_add:
            self.combox_label = QLabel("请选择加钱号码：")
            self.setWindowTitle("请选择加钱号码")
        else:
            self.combox_label = QLabel("请选择减钱号码：")
            self.setWindowTitle("请选择减钱号码：")
        self.combox = QComboBox()
        self.combox.setFocus()
        for i in range(1, 50):
            self.combox.addItem("{}".format(i))

        ok = QPushButton("确认")
        cancel = QPushButton("取消")
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(self.combox_label)
        labelLayout.addWidget(self.combox)

        mgrLayout = QHBoxLayout()
        mgrLayout.addWidget(ok)
        mgrLayout.addWidget(cancel)

        layout = QVBoxLayout()
        layout.addLayout(labelLayout)
        layout.addLayout(mgrLayout)
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)

        self.resize(240, 180)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)

    def isAdd(self):
        return self.is_add

    def get_selected(self):
        return self.combox.currentText()

#管理组件类
class Manager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.total_money = 0

        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.setFont(font)

        self.total_label = QLabel("总金额：{}￥".format(self.total_money))
        t_font = QFont()
        t_font.setBold(True)
        t_font.setPointSize(20)
        self.total_label.setFont(t_font)

        self.money_edit = QLineEdit()
        self.money_edit.setValidator(QRegExpValidator(QRegExp("^[1-9][0-9]{1,8}$")))
        self.add_money = QPushButton("加钱")
        editLayout = QHBoxLayout()
        editLayout.addWidget(self.total_label)
        editLayout.setStretchFactor(self.total_label, 2)
        editLayout.addWidget(self.money_edit)
        editLayout.setStretchFactor(self.money_edit, 1)
        editLayout.addWidget(self.add_money)
        editLayout.setStretchFactor(self.add_money, 1)
        self.add_money.clicked.connect(self.add_handle)
        self.money_edit.returnPressed.connect(self.add_handle)

        self.new_num = QLineEdit()
        self.new_num.setValidator(QRegExpValidator(QRegExp("^[1-9][0-9]{1,8}$")))
        self.add_new_num = QPushButton("减钱")
        newLayout = QHBoxLayout()
        newLayout.addWidget(self.new_num)
        newLayout.addWidget(self.add_new_num)
        self.add_new_num.clicked.connect(self.minus_handle)
        self.new_num.returnPressed.connect(self.minus_handle)

        self.reset = QPushButton("重置")
        self.reset.setToolTip("重置按钮将所有号码的金额与总金额数设置为0")
        self.reset.clicked.connect(self.reset_handle)

        manageLayout = QHBoxLayout()
        manageLayout.addLayout(editLayout)
        manageLayout.addSpacing(100)
        manageLayout.addLayout(newLayout)
        manageLayout.addSpacing(100)
        manageLayout.addWidget(self.reset)
        #set strech layout factor
        manageLayout.setStretchFactor(editLayout, 3)
        manageLayout.setStretchFactor(newLayout, 1)

        self.setLayout(manageLayout)

    def add_handle(self):
        money = self.money_edit.text()
        if money is None or money=='' or len(money)==0:
            self.money_edit.setFocus()
            return

        number_selected_dialog = EditDialog(True)
        if number_selected_dialog.exec_():
            select_number = number_selected_dialog.get_selected()
            if number_selected_dialog.isAdd():
                #为号码添加金额
                NUM_MAP[int(select_number)].add_money(int(money))
                #添加总金额
                self.total_money = self.total_money + int(money)
                self.total_label.setText("总金额：{}￥".format(self.total_money))
        self.money_edit.setText("")

    def minus_handle(self):
        money = self.new_num.text()
        if money is None or money=='' or len(money)==0:
            self.new_num.setFocus()
            return

        number_selected_dialog = EditDialog(False)
        if number_selected_dialog.exec_():
            select_number = number_selected_dialog.get_selected()
            # 为号码减去金额
            if int(money) > NUM_MAP[int(select_number)].get_money():
                # 减去金额大于号码剩余金额，提示并终止
                QMessageBox.question("提示",
                                 "您选择的号码余额不足\n剩余：{}￥\n减去：{}".format(NUM_MAP[int(select_number)].get_money(), money),
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                NUM_MAP[int(select_number)].minus_money(int(money))
                # 减去总金额
                # 因为在处理号码金额时候，已经处理了减去金额数大于剩余额的可能，故总金额不可能小于减去的金额
                self.total_money = self.total_money - int(money)
                self.total_label.setText("总金额：{}￥".format(self.total_money))
        self.new_num.setText("")

    def reset_handle(self):
        for key in NUM_MAP.keys():
            NUM_MAP[key].set_money(0)

        self.total_money = 0
        self.total_label.setText("总金额：{}￥".format(self.total_money))

class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        centralWidget = QWidget()
        layout = QGridLayout()
        # 显示每个数字
        row =0
        col =0
        for i in range(1,50):
            num = NumberItem(i)
            col = (i -1) // 12
            row = (i - 1) % 12

            layout.addWidget(num, row, col)
            NUM_MAP[i] = num

        #显示管理组件
        mgr = Manager()
        layout.addWidget(mgr, ROWS_NUM, 0, 1, col)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        #添加dock widget组件，显示号码金额历史信息

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('金额统计')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindows()
    sys.exit(app.exec_())