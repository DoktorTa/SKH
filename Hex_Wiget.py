import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QBoxLayout, QLineEdit, QFrame, QHBoxLayout, QPlainTextEdit,\
    QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QFont, QTextLayout, QPainter, QColor, QTextCursor
import webbrowser

# Поправка: Попробуем отдавать байт который изменили коду который ответственнен за зекс редактор
# возрастут накладные расходы, но тогда высокоуровненвая политика изменениея байтов будет изолирована от деталей в виде гуи


class Hex_widget(QWidget):
    _pos_x = 1
    _pos_y = 1

    # Инициализировать поля и задать местоположение
    def __init__(self):
        super().__init__()
        self.drawWiget()
        self.test()
        self.show()

    def drawWiget(self):
        # self.setMaximumSize(10 * 34 + 8 * 16 + 10, 500)
        layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.hex_matrix_table(self._pos_x, self._pos_y)
        layout.addWidget(self.txt)
        asc = self.ascii_matrix(self._pos_x, self._pos_y)
        layout.addWidget(asc)
        self.setLayout(layout)

    def edit_item(self):
        items = self.txt.selectedItems()
        self.txt.editItem(items[0])
        print(str(items[0].text()), "edit")

    def test(self):
        self.txt.itemEntered.connect(self.edit_item)

    def keyReleaseEvent(self, eventQKeyEvent):
        # Добавить проверку на то что фокус на виджете
        key = eventQKeyEvent.key()
        if key == 16777220 and not eventQKeyEvent.isAutoRepeat():
            self.edit_item()

    # def keyReleaseEvent(self, eventQKeyEvent):
    #     key = eventQKeyEvent.key()
    #     print(key)
    #     if key == 16777235 and not eventQKeyEvent.isAutoRepeat():
    #         self._pos_x = self.nav(-1, self._pos_x, 3)
    #         print('released_up', self._pos_x)
    #     elif key == 16777237 and not eventQKeyEvent.isAutoRepeat():
    #         print('released_down')
    #     elif key == 16777236 and not eventQKeyEvent.isAutoRepeat():
    #         self._pos_y = self.nav(1, self._pos_y, 16)
    #         print('released_right', self._pos_y)
    #     elif key == 16777234 and not eventQKeyEvent.isAutoRepeat():
    #         print('released_left')
    #     elif key == 16777220 and not eventQKeyEvent.isAutoRepeat():
    #
    #         print('enter')

    # Реализовать матрицы
    def ascii_matrix(self, pos_x: int, pos_y: int):
        inc_j = 0
        inc_i = 0
        ascii_row_line = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                          ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                          ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]

        asc = QTextEdit()
        asc.setReadOnly(True)
        asc.setFont(QFont("Times", 8, QFont.Bold))
        #asc.setMinimumSize(8 * 16, 250)
        asc.setMaximumSize(8 * 16, 500)

        for j in ascii_row_line:
            inc_j += 1
            inc_i = 0
            for i in j:
                inc_i += 1
                if inc_i == pos_y and inc_j == pos_x:
                    asc.setTextBackgroundColor(QColor(255, 0, 0))
                    asc.insertPlainText(i)
                    asc.setTextBackgroundColor(QColor(255, 255, 255))
                else:
                    asc.insertPlainText(i)
            asc.insertPlainText("\n")
        return asc

    def hex_matrix_table(self, pos_x: int, pos_y: int):
        inc_j = -1
        inc_i = 0
        hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                        ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                        ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
        self.txt = QTableWidget()
        self.txt.setColumnCount(16)
        self.txt.setRowCount(16)
        #self.txt.setMinimumSize(16 * 40 + 8, 500)
        for j in hex_row_line:
            inc_j += 1
            inc_i = 0
            self.txt.setRowHeight(inc_j, 8)
            for i in j:
                self.txt.setColumnWidth(inc_i, 8)
                self.txt.setItem(inc_j, inc_i, QTableWidgetItem(i))
                inc_i += 1

        return self.txt

    # Реализовать матрицы
    def hex_matrix(self, pos_x: int, pos_y: int):
        inc_j = 0
        inc_i = 0
        hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                        ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                        ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setFont(QFont("Times", 10, QFont.Bold))
        txt.setMinimumSize(10 * 34, 250)
        txt.setMaximumSize(10 * 34, 500)

        for j in hex_row_line:
            inc_j += 1
            inc_i = 0
            for i in j:
                inc_i += 1
                if inc_i == pos_y and inc_j == pos_x:
                    txt.setTextBackgroundColor(QColor(255, 0, 0))
                    txt.insertPlainText(i)
                    txt.setTextBackgroundColor(QColor(255, 255, 255))
                    txt.insertPlainText(" ")
                else:
                    txt.insertPlainText(i + " ")
            txt.insertPlainText("\n")

        return txt

    @staticmethod
    def nav(dest: int, position: int, scope: int) -> int:
        position += dest
        if position < 0:
            position = scope - 1
        elif position >= scope:
            position = 0

        return position


if __name__ == '__main__':
    app = QApplication(sys.argv)
    h = Hex_widget()
    sys.exit(app.exec_())