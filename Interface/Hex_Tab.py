import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout, QDialog
from PyQt5.QtGui import QIcon, QFont

from Interface.Hex_Wiget import HexWidget
from Modules.HexEditor.Read_file import HexOpen


class HexTab(QWidget):
    """
        Виджет представляет из себя простой шестандцатиричный редактор.
        .................0..l..0.................
        ..............0.....l.....0..............
        .............0.............0.............
        ............0...............0............
        ............0...............0............
        .............0.0.0.0.0.0.0.0.............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ..............0...........0..............
        ......0..0....0...........0....0..0......
        ...0........0.0...........0.0........0...
        .0...........00...........00...........0.
        0.......................................0
        0.......................................0
        0.......................................0
        .0.....................................0.
    """
    row = ""

    def __init__(self, file):
        super().__init__()
        self.tab_hex()
        self.__create_history_manager()
        self._create_next_page_but()
        self._create_early_page_but()

        self.__location_on_widget()

        self.read_first_block(file)

    def read_first_block(self, file):
        self.hex_reader = HexOpen(file)
        self._reader_data_file(1)

    def _reader_data_file(self, count: int, early=False):
        data, error = self.hex_reader.get_data(count)
        if error == 0:
            try:
                self.hex_wid.data_to_format(data, early=early)
            except ValueError:
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

    def move_next_page(self):
        """
            Перемешает на следующую страницу.
        """
        self._reader_data_file(1)

    def move_early_page(self):
        """
            Перемешает на предыдушую страницу.
        """
        self._reader_data_file(-1, True)

    def tab_hex(self):
        """
            Отвечает за виджет оттображения шеснадцтиричной матрицы на экране.
        """

        hex_row_line = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']]
        hex_row_label = ['00000000']
        ascii_row_line = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']]

        self.hex_wid = HexWidget()
        self.hex_wid.set_page(hex_row_label, hex_row_line, ascii_row_line)
        self.hex_wid.repaint_page()

        # TODO: переделать под событие.
        # Отвечает за обновление истории изменений на экране.
        self.timer = QTimer()
        self.timer.timeout.connect(self.history_update)
        self.timer.start(1000)

    def __create_history_manager(self):

        self.btn_delete_last = QPushButton("Cansel last")
        self.btn_delete_last.clicked.connect(self.history_del_last)

        self.btn_delete_all = QPushButton("Cansel all")
        self.btn_delete_all.clicked.connect(self.history_del_all)

        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setMaximumSize(128, 400)

    def _create_early_page_but(self):
        self.btn_early_page = QPushButton("Early page")
        self.btn_early_page.clicked.connect(self.move_early_page)

    def _create_next_page_but(self):
        self.btn_next_page = QPushButton("Next page")
        self.btn_next_page.clicked.connect(self.move_next_page)

    def __location_on_widget(self):
        self.layout = QGridLayout()

        self.layout.addWidget(self.hex_wid, 1, 0, 5, 1)
        self.layout.addWidget(self.history_list, 1, 2, 1, 2)
        self.layout.addWidget(self.btn_next_page, 3, 2)
        self.layout.addWidget(self.btn_early_page, 3, 3)
        self.layout.addWidget(self.btn_delete_last, 2, 2)
        self.layout.addWidget(self.btn_delete_all, 2, 3)
        self.setLayout(self.layout)

    def keyReleaseEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        enter_key_code = 16777220
        if key == enter_key_code and not eventQKeyEvent.isAutoRepeat():
            self.history_update()

    def history_update(self):
        """
            Обновляет историю изменений  файла.
        """
        change_form = copy.deepcopy(self.hex_wid.change_list)
        change_str = "column | row | old | new\n"
        for key in change_form:
            value = change_form.get(key)
            change_str += f"{key[0]} | {key[1:]} | {value[0:2]} | {value[2:4]}\n"
        self.history_list.setText(change_str)

    # TODO: добавить возможность удалять определенное кол-во изменений, унифицировать.
    def history_del_last(self):
        """
            Удаляет последний элемент из истории.
        """
        self.hex_wid.history_del()

    def history_del_all(self):
        """
            Удаляет всю историю.
        """
        self.hex_wid.change_list = {}
