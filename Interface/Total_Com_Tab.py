import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QColor

from Interface.Hex_Wiget import HexWidget


class TotalTab(QWidget):
    __catalog = []
    __pos_y = 0

    def __init__(self):
        super().__init__()
        self.total_left_win()
        self.grid_widget()

    def grid_widget(self):
        self.layout = QGridLayout()

        self.layout.addWidget(self.catalog_meneger)

        self.setLayout(self.layout)

    def total_left_win(self):
        self.catalog_meneger = QTextEdit()
        self.catalog_meneger.setReadOnly(True)
        self.catalog_meneger.setFont(QFont('Courier New', 10))

        catalog =[['.          ', '10', '5077', 0, 6, ''],
                  ['..         ', '10', '5077', 0, 0, ''],
                  ['4D         ', '10', '5077', 0, 10, ''],
                  ['5D         ', '10', '5077', 0, 12, ''],
                  ['6D         ', '10', '5077', 0, 13, ''],
                  ['2F      TXT', '20', '5077', 66, 14, ''],
                  ['3F      TXT', '20', '5077', 43, 15, ''],
                  ['4F      TXT', '20', '5077', 512, 16, ''],
                  ['5F      TXT', '20', '5077', 6, 17, ''],
                  ['6F      TXT', '20', '5077', 11, 18, ''],
                  ['7F      TXT', '20', '5077', 40, 19, ''],
                  ['8F      TXT', '20', '5077', 10, 20, ''],
                  ['9F      TXT', '20', '5077', 32, 21, ''],
                  ['10F     TXT', '20', '5077', 768, 22, '']]
        self.generator_catalog(catalog)
        self.catalog_printer()

    def generator_catalog(self, catalog):
        for item in catalog:
            terminator_line = "_" * (72 - len(str(item[0])) - len(str(item[1])) - len(str(item[2])) - len(str(item[3])))
            line_item = str(item[0]) + str(terminator_line) + str(item[1]) + str(item[2]) + str(item[3])
            self.__catalog.append(line_item)

    def keyReleaseEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        print(key)
        if key == 16777235 and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.nav(1, self.__pos_y, len(self.__catalog))
            print('released_up', self.__pos_y)
        elif key == 16777237 and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.nav(-1, self.__pos_y, len(self.__catalog))
            print('released_down', self.__pos_y)

    def catalog_printer(self):
        """
            [Имя, Аттрибут, Дата последней записи, Размер в байтах,
                 Номер первого кластера элемента, Длинное имя]
        """
        inc = 0
        for item in self.__catalog:
            inc += 1
            if inc == self.__pos_y:
                self.catalog_meneger.setTextBackgroundColor(QColor(255, 0, 0))
                self.catalog_meneger.insertPlainText(item)
                self.catalog_meneger.setTextBackgroundColor(QColor(255, 255, 255))
            else:
                self.catalog_meneger.insertPlainText(item)
            self.catalog_meneger.insertPlainText("\n")

    @staticmethod
    def nav(dest: int, position: int, scope: int) -> int:
        position += dest
        if position < 0:
            position = scope - 1
        elif position >= scope:
            position = 0

        return position



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = TotalTab()
    application.show()

    sys.exit(app.exec())