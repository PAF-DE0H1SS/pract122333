# -*- coding: utf-8 -*-

import sys
import sqlite3
import subprocess
import os
import shutil
from PyQt5 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_path = r"W:\pract\day3-day5\db\prackt.db"
        self.current_table = "furniture"
        self.setWindowTitle("12 СТУЛЬЕВ")
        self.setGeometry(100, 100, 900, 500)

        icon_path = r"W:\pract\day3-day5\app\icon\icon.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        top_layout = QtWidgets.QHBoxLayout()

        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setScaledContents(True)

        logo_path = r"W:\pract\day3-day5\app\icon\fotoygol.png"
        if os.path.exists(logo_path):
            pixmap = QtGui.QPixmap(logo_path)
            self.logo_label.setPixmap(
                pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        tabs_container = QtWidgets.QWidget()
        tabs_layout = QtWidgets.QVBoxLayout(tabs_container)
        tabs_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QtWidgets.QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        tabs_layout.addWidget(self.tabs)

        top_layout.addWidget(tabs_container, 1)
        top_layout.addWidget(self.logo_label, 0)

        layout.addLayout(top_layout)

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

        self.ensure_photo_columns()

        self.load_furniture()
        self.load_orders()
        self.load_clients()

    def ensure_photo_columns(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            for table in ["furniture", "orders", "clients"]:
                cur.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cur.fetchall()]
                if "photo_path" not in columns:
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN photo_path TEXT")
            conn.commit()
            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

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
        self.table1.setColumnCount(9)
        self.table1.setHorizontalHeaderLabels(
            ["Фото", "Код", "Название", "Тип", "Страна", "Кол-во", "Материал", "Цвет", "Цена"])
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
        self.table2.setColumnCount(8)
        self.table2.setHorizontalHeaderLabels(["Фото", "№", "Клиент", "Товар", "Дата", "Скидка", "Цена", "Страна"])
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

    def setup_tab3(self):
        vbox = QtWidgets.QVBoxLayout(self.tab3)

        self.table3 = QtWidgets.QTableWidget()
        self.table3.setColumnCount(7)
        self.table3.setHorizontalHeaderLabels(["Фото", "ID", "Фамилия", "Имя", "Отчество", "Адрес", "Город"])
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

            sql = "SELECT product_code, name, type, country, items_count, material, color, price, photo_path FROM furniture"
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
                btn = QtWidgets.QPushButton()
                self.setup_photo_button(btn, row[0], "furniture", row[-1])
                self.table1.setCellWidget(i, 0, btn)

                for j, val in enumerate(row[:-1]):
                    if j == 7:
                        self.table1.setItem(i, j + 1, QtWidgets.QTableWidgetItem(f"{val} руб"))
                    else:
                        self.table1.setItem(i, j + 1, QtWidgets.QTableWidgetItem(str(val)))
        except Exception as e:
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
                               f.country,
                               o.photo_path
                        FROM orders o
                                 JOIN clients c ON o.client_id = c.client_id
                                 JOIN furniture f ON o.product_code = f.product_code
                        """)
            data = cur.fetchall()
            conn.close()

            self.table2.setRowCount(len(data))
            for i, row in enumerate(data):
                btn = QtWidgets.QPushButton()
                self.setup_photo_button(btn, row[0], "orders", row[-1])
                self.table2.setCellWidget(i, 0, btn)

                for j, val in enumerate(row[:-1]):
                    if j == 4:
                        self.table2.setItem(i, j + 1, QtWidgets.QTableWidgetItem(f"{val}%"))
                    elif j == 5:
                        self.table2.setItem(i, j + 1, QtWidgets.QTableWidgetItem(f"{val} руб"))
                    else:
                        self.table2.setItem(i, j + 1, QtWidgets.QTableWidgetItem(str(val)))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def load_clients(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT client_id, last_name, first_name, middle_name, address, city, photo_path FROM clients")
            data = cur.fetchall()
            conn.close()

            self.table3.setRowCount(len(data))
            for i, row in enumerate(data):
                btn = QtWidgets.QPushButton()
                self.setup_photo_button(btn, row[0], "clients", row[-1])
                self.table3.setCellWidget(i, 0, btn)

                for j, val in enumerate(row[:-1]):
                    self.table3.setItem(i, j + 1, QtWidgets.QTableWidgetItem(str(val if val else "")))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def setup_photo_button(self, button, record_id, table, photo_path):
        placeholder = r"W:\pract\day3-day5\app\icon\fotozag.png"
        if photo_path and os.path.exists(photo_path):
            pixmap = QtGui.QPixmap(photo_path)
            if not pixmap.isNull():
                icon = QtGui.QIcon(pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio))
                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(64, 64))
                button.setText("")
            else:
                button.setIcon(QtGui.QIcon(placeholder))
                button.setIconSize(QtCore.QSize(64, 64))
                button.setText("Фото")
        else:
            button.setIcon(QtGui.QIcon(placeholder))
            button.setIconSize(QtCore.QSize(64, 64))
            button.setText("")

        def on_click():
            if photo_path and os.path.exists(photo_path):
                reply = QtWidgets.QMessageBox.question(
                    self, "Фото",
                    "Выберите действие:\nДа - заменить фото\nНет - удалить фото",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
                )
                if reply == QtWidgets.QMessageBox.Yes:
                    self.add_or_replace_photo(record_id, table)
                elif reply == QtWidgets.QMessageBox.No:
                    self.remove_photo(record_id, table)
            else:
                self.add_or_replace_photo(record_id, table)

        button.clicked.connect(on_click)

    def add_or_replace_photo(self, record_id, table):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберите фото", "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if not file_path:
            return

        dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        ext = os.path.splitext(file_path)[1]
        new_name = f"{table}_{record_id}{ext}"
        dest_path = os.path.join(dest_dir, new_name)
        try:
            shutil.copy2(file_path, dest_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось скопировать фото: {e}")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(f"UPDATE {table} SET photo_path = ? WHERE {self.get_id_field(table)} = ?",
                        (dest_path, record_id))
            conn.commit()
            conn.close()
            self.refresh_current_tab()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def remove_photo(self, record_id, table):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(f"SELECT photo_path FROM {table} WHERE {self.get_id_field(table)} = ?", (record_id,))
            row = cur.fetchone()
            if row and row[0] and os.path.exists(row[0]):
                os.remove(row[0])
            cur.execute(f"UPDATE {table} SET photo_path = NULL WHERE {self.get_id_field(table)} = ?", (record_id,))
            conn.commit()
            conn.close()
            self.refresh_current_tab()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def get_id_field(self, table):
        if table == "furniture":
            return "product_code"
        elif table == "orders":
            return "order_id"
        else:
            return "client_id"

    def refresh_current_tab(self):
        index = self.tabs.currentIndex()
        if index == 0:
            self.load_furniture()
        elif index == 1:
            self.load_orders()
        else:
            self.load_clients()

    def get_selected_id(self, table):
        row = table.currentRow()
        if row >= 0:
            return table.item(row, 1).text()
        return None

    def add_furniture(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        add_path = os.path.join(current_dir, "add.py")

        if os.path.exists(add_path):
            subprocess.Popen([sys.executable, add_path])
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл add.py не найден")

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
        row = self.table1.currentRow()
        if row >= 0:
            code = self.table1.item(row, 1).text()
            if QtWidgets.QMessageBox.question(self, "Удалить", "Удалить?") == QtWidgets.QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM furniture WHERE product_code=?", (code,))
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
            cur.execute("SELECT client_id, last_name||' '||first_name FROM clients")
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
        discount.setSuffix("%")

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
        if row >= 0:
            oid = self.table2.item(row, 1).text()
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

    def delete_client(self):
        row = self.table3.currentRow()
        if row >= 0:
            cid = self.table3.item(row, 1).text()
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())