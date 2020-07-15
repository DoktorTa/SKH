import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QBoxLayout, QLineEdit, QFrame, QHBoxLayout, QPlainTextEdit,\
    QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QFont, QTextLayout, QPainter, QColor, QTextCursor
from PyQt5.QtCore import Qt
import webbrowser

# Поправка: Попробуем отдавать байт который изменили коду который ответственнен за хекс редактор
# возрастут накладные расходы, но тогда высокоуровненвая политика изменениея байтов будет изолирована от деталей в виде гуи


class Hex_widget(QWidget):
    """
        Атрибуты:
        ~~~~~~~~~~~~~~~~~~
            **change_list**: dict - словарь с изменениями типа {'600000010': '1613'}
                Первый символ ключа - номер колонны, остальные номер строкиб
                Первые два символа значения - первоначальный байт, остальные текушее сохраненное состояние
    """
    __pos_x = 1
    __pos_y = 1

    __colonum_hend = ()

    __row_num = []
    __hex_matrix = []
    __ascii_matrix = []

    change_list = {}

    # Инициализировать поля и задать местоположение
    def __init__(self):
        super().__init__()
        self.__ascii_matrix = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]
        self.__hex_matrix = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
        self.__draw_wiget()
        self.show()

    def set_page(self, row_num: list, hex_list: list, ascii_list: list):
        """
            Функция уставнавливает значения строк и хекс матриц для следующей перерисовки
        """
        # TODO: Проверки на размернось масивов
        self.__row_num = row_num
        self.__hex_matrix = hex_list
        self.__ascii_matrix = ascii_list

    def repaint_page(self):
        """
            Функция обновления таблиц
        """
        self.txt.setVerticalHeaderLabels(self.__row_num)
        self.hex_matrix_loop()
        self.ascii_matrix_loop()

    # Ресует первичный виджет
    def __draw_wiget(self):
        self.hex_matrix_table()
        self.ascii_matrix()

        layout = QBoxLayout(QBoxLayout.LeftToRight)
        layout.addWidget(self.txt)
        layout.addWidget(self.asc)
        self.setLayout(layout)

    # Функция которая формирует лог изменений, лог расширяем
    def __edit_item(self):
        # TODO: добавить валидаторы
        items = self.txt.selectedItems()
        row = self.txt.currentItem().row()
        column = self.txt.currentItem().column()

        index = str(hex(column)[2:]) + str(self.__row_num[row])
        byte = str(self.__hex_matrix[row][column]) + str(items[0].text())

        self.change_list.update({index: byte})
        self.txt.editItem(items[0])

        print(self.change_list)

    def keyReleaseEvent(self, eventQKeyEvent):
        # Добавить проверку на то что фокус на виджете
        key = eventQKeyEvent.key()
        if key == 16777220 and not eventQKeyEvent.isAutoRepeat():
            self.__edit_item()

    # Реализовать матрицы
    def ascii_matrix(self):

        self.asc = QTextEdit()
        self.asc.setReadOnly(True)
        self.asc.setFont(QFont("Times", 8, QFont.Bold))
        #asc.setMinimumSize(8 * 16, 250)
        self.asc.setMaximumSize(8 * 16, 1000)

        self.ascii_matrix_loop()

    def ascii_matrix_loop(self):
        inc_j = 0
        for j in self.__ascii_matrix:
            inc_j += 1
            inc_i = 0
            for i in j:
                inc_i += 1
                # if inc_i == self.__pos_y and inc_j == self.__pos_x:
                #     self.asc.setTextBackgroundColor(QColor(255, 0, 0))
                #     self.asc.insertPlainText(i)
                #     self.asc.setTextBackgroundColor(QColor(255, 255, 255))
                # else:
                self.asc.insertPlainText(i)
            self.asc.insertPlainText("\n")

    def hex_matrix_table(self):

        # Создает заголовки колон в hex формате с помошью длинны первой строки
        colonum_hend = [hex(i)[2:] for i in range(0, len(self.__hex_matrix[0]))]

        self.txt = QTableWidget()
        self.txt.setColumnCount(16)
        self.txt.setRowCount(16)
        self.txt.setMaximumSize(8 * 87 + 2, 8 * 51 + 2)
        self.txt.setMaximumSize(8 * 87 + 2, 1000)
        self.txt.setHorizontalHeaderLabels(colonum_hend)
        self.txt.setFont(QFont('Courier New', 10))
        self.hex_matrix_loop()

    def hex_matrix_loop(self):
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
                item_in_cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.txt.setItem(inc_j, inc_i, item_in_cell)
                inc_i += 1
        self.txt.resizeRowsToContents()


if __name__ == '__main__':
    hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                    ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                    ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
    hex_row_label = ['00000000', '00000010', '00000020', '00000030',
                     '00000040', '00000050', '00000060', '00000070',
                     '00000080', '00000090', '000000a0', '000000b0',
                     '000000c0', '000000d0', '000000e0', '000000f0']
    ascii_row_line = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                      ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                      ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]

    app = QApplication(sys.argv)
    h = Hex_widget(hex_row_line)
    sys.exit(app.exec_())