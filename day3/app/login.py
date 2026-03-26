# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore


class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("12 СТУЛЬЕВ")
        self.setFixedSize(350, 200)

        layout = QtWidgets.QGridLayout(self)

        self.label_login = QtWidgets.QLabel("Логин:")
        self.edit_login = QtWidgets.QLineEdit()

        self.label_pass = QtWidgets.QLabel("Пароль:")
        self.edit_pass = QtWidgets.QLineEdit()
        self.edit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        layout.addWidget(self.label_login, 0, 0)
        layout.addWidget(self.edit_login, 0, 1)
        layout.addWidget(self.label_pass, 1, 0)
        layout.addWidget(self.edit_pass, 1, 1)
        layout.addWidget(self.button_box, 2, 0, 1, 2)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())