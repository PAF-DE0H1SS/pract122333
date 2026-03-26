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


    def get_selected_id(self, table):
        row = table.currentRow()
        if row >= 0:
            return table.item(row, 0).text()
        return None

    def add_furniture(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        add_path = os.path.join(current_dir, "add")

        if os.path.exists(add_path):
            subprocess.Popen([sys.executable, add_path])
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл не найден")

    def edit_furniture(self):
        record_id = self.get_selected_id(self.table1)
        if record_id:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            edit_path = os.path.join(current_dir, "edit.py")

            if os.path.exists(edit_path):
                subprocess.Popen([sys.executable, edit_path, "furniture", record_id])
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл edit.py не найден")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")

    def delete_furniture(self):
        row = self.table.currentRow()
        if row >= 0:
            code = self.table.item(row, 0).text()
            if QtWidgets.QMessageBox.question(self, "Удалить", "Удалить?") == QtWidgets.QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM furnitur WHERE product_code=?", (code,))
                    conn.commit()
                    conn.close()
                    self.load_furniture()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def add_order(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Добавить заказ")
        dlg.setModal(True)

        layout = QtWidgets.QFormLayout(dlg)

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SLECT client_id, last_name||' '||first_name FROM clients")
            clients = cur.fetchall()
            cur.execute("SELECT product_code, name FROM furniture")
            goods = cur.fetchall()
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
            return

        client = QtWidgets.QComboBox()
        for c in clients:
            client.addItem(c[1], c[0])

        furniture = QtWidgets.QComboBox()
        for f in goods:
            furniture.addItem(f[1], f[0])

        date = QtWidgets.QDateEdit()
        date.setCalendarPopup(True)
        date.setDate(QtCore.QDate.currentDate())

        discount = QtWidgets.QDoubleSpinBox()
        discount.setMaximum(100)
        discount.setSuffix()

        layout.addRow("Клиент:", client)
        layout.addRow("Товар:", furniture)
        layout.addRow("Дата:", date)
        layout.addRow("Скидка:", discount)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        layout.addRow(btns)

        if dlg.exec_():
            try:
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT INTO orders (client_id,product_code,order_date,discount_percent) VALUES (?,?,?,?)",
                            (client.currentData(), furniture.currentData(), date.date().toString("yyyy-MM-dd"),
                             discount.value()))
                conn.commit()
                conn.close()
                self.load_orders()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_order(self):
        record_id = self.get_selected_id(self.table2)
        if record_id:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            edit_path = os.path.join(current_dir, "edit.py")

            if os.path.exists(edit_path):
                subprocess.Popen([sys.executable, edit_path, "orders", record_id])
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл edit.py не найден")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")

    def delete_order(self):
        row = self.table2.currentRow()
        if row > 0:
            oid = self.table2.item(row, 0).text()
            if QtWidgets.QMessageBox.question(self, "Удалить", "Удалить?") == QtWidgets.QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM orders WHERE order_id=?", (oid,))
                    conn.commit()
                    conn.close()
                    self.load_orders()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def add_client(self):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("Добавить клиента")
        dlg.setModal(True)

        layout = QtWidgets.QFormLayout(dlg)

        last = QtWidgets.QLineEdit()
        first = QtWidgets.QLineEdit()
        middle = QtWidgets.QLineEdit()
        addr = QtWidgets.QLineEdit()
        city = QtWidgets.QLineEdit()

        layout.addRow("Фамилия:", last)
        layout.addRow("Имя:", first)
        layout.addRow("Отчество:", middle)
        layout.addRow("Адрес:", addr)
        layout.addRow("Город:", city)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        layout.addRow(btns)

        if dlg.exec_():
            try:
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT INTO clients (last_name,first_name,middle_name,address,city) VALUES (?,?,?,?,?)",
                            (last.text(), first.text(), middle.text(), addr.text(), city.text()))
                conn.commit()
                conn.close()
                self.load_clients()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_client(self):
        record_id = self.get_selected_id(self.table3)
        if record_id:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            edit_path = os.path.join(current_dir, "edit.py")

            if os.path.exists(edit_path):
                subprocess.Popen([sys.executable, edit_path, "clients", record_id])
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл edit.py не найден")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
# Если вы это проверчете, скажите мне в пятницу - авокадо
    def delete_client(self):
        row = self.table3.currentRow()
        if row >= 0:
            cid = self.table3.item(row, 0).text()
            if QtWidgets.QMessageBox.question(self, "Удалить", "Удалить?") == QtWidgets.QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM clients WHERE client_id=?", (cid,))
                    conn.commit()
                    conn.close()
                    self.load_clients()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__"
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())