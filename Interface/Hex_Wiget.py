from PyQt5.QtWidgets import QWidget, QTextEdit, QTableWidget,\
    QTableWidgetItem, QLineEdit, QItemDelegate, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Modules.HexEditor.Hex_presentor import HexPresentor


# Некоторые не snake_case ввиду унификации с pyqt5 используюший CamelCase.

class HexDelegate(QItemDelegate):
    __read_only = False

    def __init__(self, read_mode=False):
        super().__init__()
        self.__read_only = read_mode

    def createEditor(self, parent, option, index):
        line = QLineEdit(parent)
        if self.__read_only:
            line.setReadOnly(True)
        line.setInputMask("HH")
        return line


class HexWidget(QWidget):
    """
        Класс создает виджет хекс редактора и предостовляет редактирование.
        Кормите данные через set_page
        , обновляйте данные на экране через repaint_page,
        для подтверждения изменений обязательно кликайте энтер.

        self.txt = QTableWidget
        self.asc = QTextEdit

        Атрибуты:
        ~~~~~~~~~~~~~~~~~~
            **change_list**: dict - словарь с изменениями типа
             {'600000010': '1613'}
                Первый символ ключа - номер колонны, остальные номер строкиб
                Первые два символа значения - первоначальный байт,
                 остальные текушее сохраненное состояние
    """
    __pos_x = 1
    __pos_y = 1

    __read_only = False

    __colonum_hend = ()

    __row_num = []
    __hex_matrix = []
    __ascii_matrix = []

    change_list = {}

    __last_row_num = 0

    # Инициализировать поля и задать местоположение
    def __init__(self, block_row_size=16):
        super().__init__()
        self.hex_presentor = HexPresentor()
        self.__ascii_matrix = [['0', '1', '2', '3', '4', '5', '6', '7',
                                '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]
        self.__hex_matrix = [['00', '01', '02', '03', '04', '05', '06', '07',
                              '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
        self.__draw_widget(block_row_size)
        self.show()

    def setReadOnly(self, read: bool):
        self.__read_only = read
        self.txt.setItemDelegate(HexDelegate(self.__read_only))

    def set_page(self, row_num: list, hex_list: list, ascii_list: list):
        """
            Функция уставнавливает значения строк и
             хекс матриц для следующей перерисовки.
        """
        # TODO: Проверки на размернось масивов
        self.__row_num = row_num
        self.__hex_matrix = hex_list
        self.__ascii_matrix = ascii_list

    def repaint_page(self):
        """
            Функция обновления таблиц
             по вшитому с помощью set_page представлению.
        """
        self.txt.setRowCount(len(self.__row_num))
        self.txt.setVerticalHeaderLabels(self.__row_num)
        self._hex_matrix_loop()
        self._ascii_matrix_loop()

    # Ресует первичный виджет
    def __draw_widget(self, block_row_size: int):
        self.__hex_matrix_table(block_row_size)
        self.__ascii_matrix_table()

        layout = QGridLayout()
        layout.setColumnMinimumWidth(1, 10)
        layout.setColumnMinimumWidth(3, 10)
        layout.setColumnStretch(1, -1)
        layout.setColumnStretch(3, 1)
        layout.addWidget(self.txt, 0, 0)
        layout.addWidget(self.asc, 0, 2)
        self.setLayout(layout)

    def history_del(self):
        if len(self.change_list) is not 0:
            history_last_point = self.change_list.popitem()
            # key,  value = history_last_point
            # self.txt.setItem(int(int(key[1:]) / 10),
            #                  int(key[0]),
            #                  QTableWidgetItem(value[0:2]))

    # Функция которая формирует лог изменений, лог расширяем
    def __edit_item(self):
        items = self.txt.selectedItems()
        row = self.txt.currentItem().row()
        column = self.txt.currentItem().column()

        index = str(hex(column)[2:]) + str(self.__row_num[row])
        if str(self.__hex_matrix[row][column]) != str(items[0].text()):
            byte = str(self.__hex_matrix[row][column]) + str(items[0].text())
            self.change_list.update({index: byte})
        self.txt.editItem(items[0])

    def keyReleaseEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        ENTER_PRESSED = 16777220
        if key == ENTER_PRESSED and not eventQKeyEvent.isAutoRepeat():
            self.__edit_item()

    # Инициализация аски матрицы
    def __ascii_matrix_table(self):
        self.asc = QTextEdit()
        self.asc.setReadOnly(True)
        self.asc.setFont(QFont('Courier New', 8))
        # TODO: нужна нормальная размерность для отрисовки.
        self.asc.setMinimumSize(8 * 16, 250)
        self.asc.setMaximumSize(8 * 16, 1000)

        self._ascii_matrix_loop()

    # Инициализыция
    def __hex_matrix_table(self, block_row_size: int):
        # Создает заголовки колон в hex формате с помошью длинны первой строки
        colonum_hend = [
            hex(i)[2:] for i in range(0, len(self.__hex_matrix[0]))]

        self.txt = QTableWidget()
        self.txt.setColumnCount(16)
        self.txt.setRowCount(block_row_size)
        # TODO: нужна нормальная размерность для отрисовки.
        self.txt.setMinimumSize(8 * 87 + 2, 200)
        self.txt.setMaximumSize(8 * 87 + 2, 1000)
        self.txt.setHorizontalHeaderLabels(colonum_hend)
        self.txt.setFont(QFont('Courier New', 10))

        self.txt.setItemDelegate(HexDelegate(self.__read_only))

        self._hex_matrix_loop()

    def _ascii_matrix_loop(self):
        """
            Метод обновляет аски матрицу виджета в соответствии с ascii_matrix
        """
        self.asc.clear()
        inc_j = 0
        for line in self.__ascii_matrix:
            inc_j += 1
            inc_i = 0
            for symbol in line:
                inc_i += 1
                self.asc.insertPlainText(symbol)
            self.asc.insertPlainText("\n")

    def _hex_matrix_loop(self):
        """
            Метод обновляет хекс матрицу виджета в соответствии с hex_matrix
        """
        inc_j = -1
        for line in self.__hex_matrix:
            inc_j += 1
            inc_i = 0
            self.txt.setRowHeight(inc_j, 8)
            for byte in line:
                self.txt.setColumnWidth(inc_i, 8)
                item_in_cell = QTableWidgetItem(byte)
                item_in_cell.setFont(QFont('Courier New', 10))
                item_in_cell.setTextAlignment(
                    Qt.AlignVCenter | Qt.AlignHCenter)
                self.txt.setItem(inc_j, inc_i, item_in_cell)
                inc_i += 1
        self.txt.resizeRowsToContents()

    def data_to_format(self, data: bytes, step=16, early=False):
        """
            Форматирует байтовое представление
             в пердстовление шеснадцатирчного редактора.
            А так же задает и перерисовывает страницу.
            Вызываете этот метод если вам необходимо
             перерисовать виджет под новые данные.
        """
        rows, hex_rows, ascii_rows = self.hex_presentor\
            .present(data, step, self.__last_row_num, early)
        try:
            if int(rows[0]) < 0:
                raise ValueError
        except IndexError:
            raise ValueError
        self.__last_row_num = (int(rows[len(rows) - 1]) // step) + 1
        self.set_page(rows, hex_rows, ascii_rows)
        self.repaint_page()
