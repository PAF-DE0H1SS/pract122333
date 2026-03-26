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
        elif index == 1:
            self.current_table = "orders"
        else:
            self.current_table = "clients"

    def setup_tab1(self):
        vbox = QtWidgets.QVBoxLayout(self.tab1)

        hbox = QtWidgets.QHBoxLayout()
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Поиск")
        self.search.textChanged.connect(self.load_furniture)
        hbox.addWidget(self.search)

        self.type = QtWidgets.QComboBox()
        self.type.addItems(["Все", "спальная", "кухонная"])
        self.type.currentTextChanged.connect(self.load_furniture)
        hbox.addWidget(self.type)
        vbox.addLayout(hbox)

        self.table1 = QtWidgets.QTableWidget()
        self.table1.setColumnCount(8)
        self.table1.setHorizontalHeaderLabels(
            ["Код", "Название", "Тип", "Страна", "Кол-во", "Материал", "Цвет", "Цена"])
        vbox.addWidget(self.table1)

        hbox2 = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_add.clicked.connect(self.add_furniture)
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_furniture)
        btn_delete = QtWidgets.QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_furniture)
        btn_refresh = QtWidgets.QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_furniture)
        hbox2.addWidget(btn_add)
        hbox2.addWidget(btn_edit)
        hbox2.addWidget(btn_delete)
        hbox2.addWidget(btn_refresh)
        vbox.addLayout(hbox2)

    def setup_tab2(self):
        vbox = QtWidgets.QVBoxLayout(self.tab2)

        self.table2 = QtWidgets.QTableWidget()
        self.table2.setColumnCount(7)
        self.table2.setHorizontalHeaderLabels(["№", "Клиент", "Товар", "Дата", "Скидка", "Цена", "Страна"])
        vbox.addWidget(self.table2)

        hbox = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_add.clicked.connect(self.add_order)
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_order)
        btn_delete = QtWidgets.QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_order)
        btn_refresh = QtWidgets.QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_orders)
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_edit)
        hbox.addWidget(btn_delete)
        hbox.addWidget(btn_refresh)
        vbox.addLayout(hbox)

    def setup_tab3(self)
        vbox = QtWidgets.QVBoxLayout(self.tab3)

        self.table3 = QtWidgets.QTableWidget()
        self.table3.setColumnCount(6)
        self.table3.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Адрес", "Город"])
        vbox.addWidget(self.table3)

        hbox = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_add.clicked.connect(self.add_client)
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_edit.clicked.connect(self.edit_client)
        btn_delete = QtWidgets.QPushButton("Удалить")
        btn_delete.clicked.connect(self.delete_client)
        btn_refresh = QtWidgets.QPushButton("Обновить")
        btn_refresh.clicked.connect(self.load_clients)
        hbox.addWidget(btn_add)
        hbox.addWidget(btn_edit)
        hbox.addWidget(btn_delete)
        hbox.addWidget(btn_refresh)
        vbox.addLayout(hbox)

    def load_furniture(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            sql = "SELECT product_code, name, type, country, items_count, material, color, price FROM furniture"
            params = []

            if self.search.text():
                sql += " WHERE name LIKE ?"
                params.append(f"%{self.search.text()}%")

            if self.type.currentText() != "Все":
                if params:
                    sql += " AND type = ?"
                else:
                    sql += " WHERE type = ?"
                params.append(self.type.currentText())

            cur.execute(sql, params)
            data = cur.fetchall()
            conn.close()

            self.table1.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, val in enumerate(row):
                    if j == 7:
                        self.table1.setItem(i, j, QtWidgets.QTableWidgetItem(f"{val} руб"))
                    else:
                        self.table1.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))
        except Exception as e
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def load_orders(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                        SELECT o.order_id,
                               c.last_name || ' ' || c.first_name,
                               f.name,
                               o.order_date,
                               o.discount_percent,
                               ROUND(f.price * (100 - o.discount_percent) / 100, 2),
                               f.country
                        FROM orders o
                                 JOIN clients c ON o.client_id = c.client_id
                                 JOIN furniture f ON o.product_code = f.product_code
                        """)
            data = cur.fetchall()
            conn.close()

            self.table2.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, val in enumerate(row):
                    if j == 4:
                        self.table2.setItem(i, j, QtWidgets.QTableWidgetItem(f"{val}%"))
                    elif j == 5:
                        self.table2.setItem(i, j, QtWidgets.QTableWidgetItem(f"{val} руб"))
                    else:
                        self.table2.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))
        except Exception as
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def load_clients(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT client_id, last_name, first_name, middle_name, address, city FROM clients")
            data = cur.fetchall()
            conn.close()

            self.table3.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, val in enumerate(row):
                    self.table3.setItem(i, j, QtWidgets.QTableWidgetItem(str(val if val else "")))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
