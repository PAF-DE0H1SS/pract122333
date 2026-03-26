# -*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt5 import QtWidgets


class EditDialog(QtWidgets.QDialog):
    def __init__(self, table_name, record_id, parent=None):
        super().__init__(parent)
        self.db_path = "W:\pract\day3\db\prackt.db"
        self.table_name = table_name
        self.record_id = record_id
        self.setWindowTitle("Редактировать - {table_name}")
        self.setFixedSize(400, 450)

        self.load_data()
        self.setup_ui()

    def load_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            if self.table_name == "furnitur":
                cur.execute(
                    "SELECT name, type, country, items_count, material, color, price FROM furniture WHERE product_code=?",
                    (self.record_id,))
                self.data = cur.fetchone()
            elif self.table_name == "order":
                cur.execute("SELECT client_id, product_code, order_date, discount_percent FROM orders WHERE order_id=?",
                            (self.record_id,))
                self.data = cur.fetchone()
            elif self.table_name == "client":
                cur.execute("SELECT last_name, first_name, middle_name, address, city FROM clients WHERE client_id=?",
                            (self.record_id,))
                self.data = cur.fetchone()

            conn.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
            self.reject()

    def setup_ui(self):
        layout = QtWidgets.QFormLayout(self)

        if self.table_name == "furniture":
            self.name = QtWidgets.QLineEdit(self.data[0] if self.data else "")
            self.type_cb = QtWidgets.QComboBox()
            self.type_cb.addItems(["спальная", "кухонная"])
            if self.data:
                self.type_cb.setCurrentText(self.data[1])
            self.country = QtWidgets.QLineEdit(self.data[2] if self.data else "")
            self.items = QtWidgets.QSpinBox()
            self.items.setMaximum(100)
            if self.data:
                self.items.setValue(self.data[3])
            self.material = QtWidgets.QLineEdit(self.data[4] if self.data else "")
            self.color = QtWidgets.QLineEdit(self.data[5] if self.data else "")
            self.price = QtWidgets.QDoubleSpinBox()
            self.price.setMaximum(1000000)
            if self.data:
                self.price.setValue(self.data[6])

            layout.addRow("Название:", self.name)
            layout.addRow("Тип:", self.type_cb)
            layout.addRow("Страна:", self.country)
            layout.addRow("Кол-во предметов:", self.items)
            layout.addRow("Материал:", self.material)
            layout.addRow("Цвет:", self.color)
            layout.addRow("Цена:", self.price)

        elif self.table_name == "orders":
            try:
                conn = sqlite3.connect(self.db_path)
                cur = conn.cursor()
                cur.execute("SELECT client_id, last_name||' '||first_name FROM clients")
                self.clients = cur.fetchall()
                cur.execute("SELECT product_code, name FROM furniture")
                self.goods = cur.fetchall()
                conn.close()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
                return

            self.client = QtWidgets.QComboBox()
            for c in self.clients:
                self.client.addItem(c[1], c[0])
            if self.data:
                self.client.setCurrentIndex(self.find_client_index(self.data[0]))

            self.furniture = QtWidgets.QComboBox()
            for f in self.goods:
                self.furniture.addItem(f[1], f[0])
            if self.data:
                self.furniture.setCurrentIndex(self.find_furniture_index(self.data[1]))

            self.date = QtWidgets.QDateEdit()
            self.date.setCalendarPopup(True)
            if self.data:
                self.date.setDate(QtCore.QDate.fromString(self.data[2], "yyyy-MM-dd"))

            self.discount = QtWidgets.QDoubleSpinBox()
            self.discount.setMaximum(100)
            self.discount.setSuffix("%")
            if self.data:
                self.discount.setValue(self.data[3])

            layout.addRow("Клиент:", self.client)
            layout.addRow("Товар:", self.furniture)
            layout.addRow("Дата:", self.date)
            layout.addRow("Скидка:", self.discount)

        elif self.table_name == "clients":
            self.last = QtWidgets.QLineEdit(self.data[0] if self.data else "")
            self.first = QtWidgets.QLineEdit(self.data[1] if self.data else "")
            self.middle = QtWidgets.QLineEdit(self.data[2] if self.data else "")
            self.addr = QtWidgets.QLineEdit(self.data[3] if self.data else "")
            self.city = QtWidgets.QLineEdit(self.data[4] if self.data else "")

            layout.addRow("Фамилия:", self.last)
            layout.addRow("Имя:", self.first)
            layout.addRow("Отчество:", self.middle)
            layout.addRow("Адрес:", self.addr)
            layout.addRow("Город:", self.city)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.save)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def find_client_index(self, client_id):
        for i, c in enumerate(self.clients):
            if c[0] == client_id:
                return i
        return

    def find_furniture_index(self, product_code):
        for i, f in enumerate(self.goods):
            if f[0] == product_code:
                return i
        return

    def save(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            if self.table_name == "furniture":
                cur.execute("""
                            UPDATE furniture
                            SET name=?,
                                type=?,
                                country=?,
                                items_count=?,
                                material=?,
                                color=?,
                                price=?
                            WHERE product_code = ?,
                            """, (self.name.text(), self.type_cb.currentText(), self.country.text(),
                                  self.items.value(), self.material.text(), self.color.text(),
                                  self.price.value(), self.record_id))

            elif self.table_name == "orders":
                cur.execute("""
                            UPDATE orders
                            SET client_id=?,
                                product_code=?,
                                order_date=?,
                                discount_percent=?,
                            WHERE order_id = ?
                            """, (self.client.currentData(), self.furniture.currentData(),
                                  self.date.date().toString("yyyy-MM-dd"), self.discount.value(), self.record_id))

            elif self.table_name == "clients":
                cur.execute("""
                            UPDATE clients
                            SET last_name=?,
                                first_name=?,
                                middle_name=?,
                                address=?,
                                city=?,
                            WHERE client_id = ?
                            """, (self.last.text(), self.first.text(), self.middle.text(),
                                  self.addr.text(), self.city.text(), self.record_id))

            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    import sys
    from PyQt5 import QtCore

    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) < 3:
        QtWidgets.QMessageBox.critical(None, "Ошибка", "Неверные параметры")
        sys.exit(1)

    table_name = sys.argv[1]
    record_id = sys.argv[2]

    dlg = EditDialog(table_name, record_id)
    dlg.show()
    sys.exit(app.exec_())