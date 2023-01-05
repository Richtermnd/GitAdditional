import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QDialogButtonBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets


class Form(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.accepted.connect(self.return_data)

    def get_data(self):
        res = []
        for row in range(self.formLayout.rowCount()):
            field = self.formLayout.itemAt(row, QFormLayout.FieldRole).widget()
            data = field.text()
            if not data:
                raise TypeError
            res.append(data)
        return res

    def return_data(self):
        try:
            res = self.get_data()
        except TypeError:
            return
        self.parentWidget().add_coffee(res)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.add_action.triggered.connect(self.show_form)
        self.loadTable()

    def loadTable(self):
        cur = self.con.cursor()
        res = cur.execute("""SELECT * FROM coffee""").fetchall()
        headers = [elem[0] for elem in cur.execute("""SELECT * FROM coffee""").description]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def show_form(self):
        self.form = Form(parent=self)
        self.form.show()

    def add_coffee(self, data):
        cur = self.con.cursor()
        cur.execute('''INSERT INTO coffee(grade, roast, ground, description, price, weight) 
                       VALUES(?, ?, ?, ?, ?, ?)''', data)
        self.con.commit()
        self.loadTable()

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())