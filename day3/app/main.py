# -*- coding: utf-8 -*-

import sys
import sqlite3
import subprocess
import os
from PyQt5 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_path = r"W:\pract\day3\db\prackt.db"
        self.current_table = "furniture"
        self.setWindowTitle("12 СТУЛЬЕВ")
        self.setGeometry(100, 100, 900, 500)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)

        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()

        self.tabs.addTab(self.tab1, "Мебель")
        self.tabs.addTab(self.tab2, "Заказы")
        self.tabs.addTab(self.tab3, "Клиенты")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        menu = self.menuBar()
        menu.addAction("Выход", self.close)

        self.load_furniture()
        self.load_orders()
        self.load_clients()

    def on_tab_changed(self, index):
        if index == 0:
            self.current_table = "furniture"
        elif index