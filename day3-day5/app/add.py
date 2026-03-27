# -*- coding: utf-8 -*-

import sys
import sqlite3
import os
from PyQt5 import QtWidgets, QtGui


class AddDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = r"W:\pract\day3-day5\db\prackt.db"
        self.setWindowTitle("Добавить мебель")
        self.setFixedSize(350, 400)

        icon_path = r"W:\pract\day3-day5\app\icon\icon.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        layout = QtWidgets.QFormLayout(self)

        self.name = QtWidgets.QLineEdit()
        self.type_cb = QtWidgets.QComboBox()
        self.type_cb.addItems(["спальная", "кухонная"])
        self.country = QtWidgets.QLineEdit()
        self.items = QtWidgets.QSpinBox()
        self.items.setMaximum(100)
        self.material = QtWidgets.QLineEdit()
        self.color = QtWidgets.QLineEdit()
        self.price = QtWidgets.QDoubleSpinBox()
        self.price.setMaximum(1000000)

        layout.addRow("Название:", self.name)
        layout.addRow("Тип:", self.type_cb)
        layout.addRow("Страна:", self.country)
        layout.addRow("Кол-во предметов:", self.items)
        layout.addRow("Материал:", self.material)
        layout.addRow("Цвет:", self.color)
        layout.addRow("Цена:", self.price)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.save)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def save(self):
        if not self.name.text():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите название")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                        INSERT INTO furniture (name, type, country, items_count, material, color, price)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (self.name.text(), self.type_cb.currentText(), self.country.text(),
                              self.items.value(), self.material.text(), self.color.text(), self.price.value()))
            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = AddDialog()
    dlg.show()
    sys.exit(app.exec_())