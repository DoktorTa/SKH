import logging

from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel, QGridLayout, QDialog
from PyQt5.QtGui import QFont, QColor

from Interface.Hex_Wiget import HexWidget
from Modules.FS.FAT_comand_sys import CommandFAT3216
from Modules.FS.EXT2_command_sys import CommandEXT2


class TotalTab(QWidget):
    """
        Виджет коммандной системы.
    """
    work_catalog = []
    __catalog = []
    __pos_y = 0
    __pos_page = 0
    __fs = 0

    def __init__(self):
        super().__init__()
        self._total_left_win()
        self._total_right_win()
        self._button_page()
        self.__grid_widget()

    def fat_load(self, file):
        """
            Стартует загрузку фат 16 и 32.
        """
        self.__fs = CommandFAT3216(file)
        self.generator_catalog(self.__fs.get_root())
        self.__catalog_printer()

    def ext_load(self, file):
        """
            Стартует загрузку еэкст2
        """
        self.__fs = CommandEXT2(file)
        self.generator_catalog(self.__fs.get_root())
        self.__catalog_printer()

    def __grid_widget(self):
        self.layout = QGridLayout()

        self.layout.addWidget(self.catalog_meneger, 1, 1, 2, 1)
        self.layout.addWidget(self.hex_view, 1, 2, 1, 2)
        self.layout.addWidget(self.next_page_button, 2, 3)
        self.layout.addWidget(self.early_page_button, 2, 2)

        self.setLayout(self.layout)

    def next_page(self):
        """
            Следуюшая страница хекс редактора.
        """

        try:
            self.__pos_page += 1
            data, pointer, error = self.__fs.read(self.work_catalog, self.__pos_y, 1, self.__pos_page)
            self.hex_view.data_to_format(data)
        except IndexError:
            self.__pos_page -= 1
            self.__dialog_file_end("File is end.")

    def early_page(self):
        """
            Предудушая страница хекс редактора.
        """

        try:
            self.__pos_page -= 1
            data, pointer, error = self.__fs.read(self.work_catalog, self.__pos_y, 1, self.__pos_page)
            self.hex_view.data_to_format(data, early=True)
        except IndexError:
            self.__pos_page += 1
            self.__dialog_file_end("File is end.")

    def __dialog_file_end(self, msg: str):
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.setMinimumSize(250, 100)
        dialog.setWindowTitle("Error")

        dialog.buttonBox = QPushButton("OK")
        dialog.buttonBox.clicked.connect(dialog.accept)

        dialog.error_msg = QLabel(msg)

        dialog.layout = QGridLayout()
        dialog.layout.addWidget(dialog.error_msg, 0, 0, 1, 3)
        dialog.layout.addWidget(dialog.buttonBox, 1, 1)
        dialog.setLayout(dialog.layout)

        dialog.exec_()

    def _button_page(self):
        self.next_page_button = QPushButton("Next")
        self.next_page_button.clicked.connect(self.next_page)

        self.early_page_button = QPushButton('Early')
        self.early_page_button.clicked.connect(self.early_page)

    def _total_right_win(self):
        hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
        hex_row_label = ['00000000']
        ascii_row_line = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]

        self.hex_view = HexWidget()
        self.hex_view.set_page(hex_row_label, hex_row_line, ascii_row_line)
        self.hex_view.repaint_page()
        self.hex_view.setReadOnly(True)

    def _total_left_win(self):
        self.catalog_meneger = QTextEdit()
        self.catalog_meneger.setReadOnly(True)
        self.catalog_meneger.setFont(QFont('Courier New', 10))
        self.catalog_meneger.setMinimumSize(600, 400)
        self.catalog_meneger.setMaximumSize(600, 1000)

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
        except BaseException:  # Вот это хуйня но это хуйня, хуйня нужно убрать и сделать нехуйня.
            data = "01.01.1980"

        return data

    def generator_catalog(self, catalog: list):
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
        up_key = 16777235
        down_key = 16777237
        f3_key = 16777266
        enter_key = 16777220
        if key == up_key and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.__nav(-1, self.__pos_y, len(self.__catalog))
            self.__catalog_printer()
        elif key == down_key and not eventQKeyEvent.isAutoRepeat():
            self.__pos_y = self.__nav(1, self.__pos_y, len(self.__catalog))
            self.__catalog_printer()
        elif key == enter_key and not eventQKeyEvent.isAutoRepeat():
            self.next_dir()
        elif key == f3_key and not eventQKeyEvent.isAutoRepeat():
            self.read_file()

    def read_file(self):
        """
            Чтение файла в шеснадцатиричный просмоторшик.
        """
        pos = 0
        try:
            all_byte_elements, pointer, error = self.__fs.read(self.work_catalog, self.__pos_y, 1, pos)
            if error == 0:
                self.hex_view.data_to_format(all_byte_elements)
        except IndexError:
            logging.error(f"Ощибка при чтении файла {self.work_catalog[self.__pos_y]}")

    def next_dir(self):
        """
            Перемешение в следующую директорию.
        """
        next_dir, error = self.__fs.cd(self.work_catalog, self.__pos_y)
        if error == 0:
            self.generator_catalog(next_dir)
            self.__catalog_printer()

    def __catalog_printer(self):
        """
            Печатает лист директории.
        """
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
    def __nav(dest: int, position: int, scope: int) -> int:
        position += dest
        if position < 0:
            position = scope - 1
        elif position >= scope:
            position = 0

        return position
