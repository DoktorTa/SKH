import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout, QTableView, QTableWidget,\
    QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt


from Modules.ExecutableFiles.ELF_work import ELFWork


class ELFTab(QWidget):

    def __init__(self, file):
        super().__init__()
        header = self._elf_header(file)
        table_headers = self._getting_table_headers()
        section_table = self._getting_section_table()
        self.header_widget(header)
        self.table_headers_widget(table_headers)
        self.section_table_wiget(section_table)
        self.location_on_widget()

    def section_table_wiget(self, section_table):
        heading_w = ["Name", "Type", "Flags", "Virtual adress", "Offset", "Segment size in file", "Associated section index",
                     "Additional section information", "Required section alignment", "Size in bytes of each record"]

        self.section_table_w = QTableWidget()
        self.section_table_w.setColumnCount(len(heading_w))
        self.section_table_w.setRowCount(len(section_table))
        self.section_table_w.setMinimumSize(300, 100)
        self.section_table_w.setHorizontalHeaderLabels(heading_w)
        self.section_table_w.setFont(QFont('Courier New', 10))

        self.section_table_w.setEditTriggers(QAbstractItemView.NoEditTriggers)

        inc_i = 0
        inc_j = 0
        for header in section_table:
            for key in header:
                value = header.get(key)
                # print(str(value), inc_i, inc_j)
                item_in_cell = QTableWidgetItem(str(value))
                item_in_cell.setFont(QFont('Courier New', 10))
                item_in_cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.section_table_w.setItem(inc_i, inc_j, item_in_cell)
                inc_j += 1

    def header_widget(self, header: dict):
        head = f""

        self.header_layout_w = QLabel()

        for item in header:
            value = header.get(item)
            head += f"{item}: {value}\n"

        self.header_layout_w.setText(head)

    def table_headers_widget(self, table_headers):
        heading_w = ["Type", "Flags", "Offset", "Virtual adress", "Physical adress", "Segment size in file",
                     "Segment size in memory", "Segment alignment"]

        self.table_headers_w = QTableWidget()
        self.table_headers_w.setColumnCount(len(heading_w))
        self.table_headers_w.setRowCount(len(table_headers))
        self.table_headers_w.setMinimumSize(300, 100)
        self.table_headers_w.setHorizontalHeaderLabels(heading_w)
        self.table_headers_w.setFont(QFont('Courier New', 10))

        self.table_headers_w.setEditTriggers(QAbstractItemView.NoEditTriggers)

        inc_i = 0
        inc_j = 0
        for header in table_headers:
            for key in header:
                value = header.get(key)
                # print(str(value), inc_i, inc_j)
                item_in_cell = QTableWidgetItem(str(value))
                item_in_cell.setFont(QFont('Courier New', 10))
                item_in_cell.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                self.table_headers_w.setItem(inc_i, inc_j, item_in_cell)
                inc_j += 1

    def _getting_section_table(self):
        section_table = self.__elf.get_section_table()
        return section_table

    def _getting_table_headers(self):
        table_headers = self.__elf.get_table_header()
        return table_headers

    def _elf_header(self, file) -> dict:
        self.__elf = ELFWork(file)
        header = self.__elf.get_header()
        return header

    def location_on_widget(self):
        self.layout = QGridLayout()
        # self.layout = QHBoxLayout()

        # self.layout.setColumnMinimumWidth(1, 10)
        # self.layout.setColumnStretch(1, 0)

        self.layout.addWidget(self.header_layout_w, 1, 0)
        self.layout.addWidget(self.table_headers_w, 2, 0)
        self.layout.addWidget(self.section_table_w, 3, 0)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
        application = ELFTab(file)
        application.show()

        sys.exit(app.exec())
