import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable()

    @property
    def con(self):
        return sqlite3.connect('coffee.sqlite')

    def loadTable(self):
        with self.con as con:
            cur = con.cursor()
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

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())