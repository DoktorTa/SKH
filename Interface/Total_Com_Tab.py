import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QColor

from Interface.Hex_Wiget import HexWidget
from Modules.FS.FAT_comand_sys import CommandFAT3216
from Modules.FS.EXT2_command_sys import CommandEXT2


class TotalTab(QWidget):
    work_catalog = []
    __catalog = []
    __pos_y = 0
    __fs = 0

    def __init__(self):
        super().__init__()
        self.total_left_win()
        self.total_right_win()
        self.grid_widget()

    def fat_load(self, file):
        self.__fs = CommandFAT3216(file)
        self.generator_catalog(self.__fs.get_root())
        self.catalog_printer()

    def ext_load(self, file):
        self.__fs = CommandEXT2(file)
        self.generator_catalog(self.__fs.get_root())
        self.catalog_printer()

    def grid_widget(self):
        self.layout = QGridLayout()

        self.layout.addWidget(self.catalog_meneger, 1, 1)
        self.layout.addWidget(self.hex_view, 1, 2)

        self.setLayout(self.layout)

    def total_right_win(self):
        hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                        ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f'],
                        ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f']]
        hex_row_label = ['00000000', '00000010', '00000020', '00000030',
                         '00000040', '00000050', '00000060', '00000070',
                         '00000080', '00000090', '000000a0', '000000b0',
                         '000000c0', '000000d0', '000000e0', '000000f0']
        ascii_row_line = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                          ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                          ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]

        self.hex_view = HexWidget()
        self.hex_view.set_page(hex_row_label, hex_row_line, ascii_row_line)
        self.hex_view.repaint_page()
        self.hex_view.setReadOnly(True)

    def total_left_win(self):
        self.catalog_meneger = QTextEdit()
        self.catalog_meneger.setReadOnly(True)
        self.catalog_meneger.setFont(QFont('Courier New', 10))
        self.catalog_meneger.setMinimumSize(600, 400)
        self.catalog_meneger.setMaximumSize(600, 1000)

        # self.catalog_meneger.setStyleSheet('down-button { left: 20px }')
        # self.catalog_meneger.setStyleSheet('border-style: solid; border-width: 10px; border-color: white;')

    @staticmethod
    def convert_data(element_data: str) -> str:
        try:
            start_new_era = 1980

            element_data = int(element_data, 16)
            year = element_data >> 9
            month = (element_data - (year << 9)) >> 5
            day = element_data - ((element_data >> 5) << 5)
            year += start_new_era
            data = str(f'{day:02d}') + "." + str(f'{month:02d}') + "." + str(f'{year:04d}')
        except BaseException:
            data = "01.01.1980"

        return data

    def generator_catalog(self, catalog):
        """
            [Имя, Аттрибут, Дата последней записи, Размер в байтах,
                 Номер первого кластера элемента, Длинное имя]
        """
        self.work_catalog = catalog
        self.__catalog = []

        for item in catalog:
            data = self.convert_data(item[2])
            terminator_line = "_" * (72 - len(str(item[0])) - len(data) - len(str(item[3])) - 1)
            line_item = str(item[0]) + str(terminator_line) + str(item[3]) + "|" + str(data)
            self.__catalog.append(line_item)

    def keyReleaseEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        # print(key)
        if key == 16777235 and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.nav(-1, self.__pos_y, len(self.__catalog))
            self.catalog_printer()
        elif key == 16777237 and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.nav(1, self.__pos_y, len(self.__catalog))
            self.catalog_printer()
        elif key == 16777220 and not eventQKeyEvent.isAutoRepeat():
            self.next_dir()
        elif key == 16777266 and not eventQKeyEvent.isAutoRepeat():
            self.read_file()

    def read_file(self):
        pos = 0
        all_byte_elements, pointer, error = self.__fs.read(self.work_catalog, self.__pos_y, 1, pos)
        # if error == 0:
        #     self.hex_view.set_page()

    def next_dir(self):
        next_dir, error = self.__fs.cd(self.work_catalog, self.__pos_y)
        if error == 0:
            self.generator_catalog(next_dir)
            self.catalog_printer()

    def catalog_printer(self):
        self.catalog_meneger.clear()
        inc = 0
        for item in self.__catalog:
            if inc == self.__pos_y:
                self.catalog_meneger.setTextBackgroundColor(QColor(0, 0, 0))
                self.catalog_meneger.setTextColor(QColor(255, 255, 255))
                self.catalog_meneger.insertPlainText(item)
                self.catalog_meneger.setTextColor(QColor(0, 0, 0))
                self.catalog_meneger.setTextBackgroundColor(QColor(255, 255, 255))
            else:
                self.catalog_meneger.insertPlainText(item)
            inc += 1
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