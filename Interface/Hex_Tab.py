import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont

from Interface.Hex_Wiget import HexWidget


class HexTab(QWidget):
    row = ""

    def __init__(self):
        super().__init__()
        self.tab_hex()
        self.location_on_widget()

    def tab_hex(self):
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

        self.hex_wid = HexWidget()
        self.hex_wid.set_page(hex_row_label, hex_row_line, ascii_row_line)
        self.hex_wid.repaint_page()
        # self.hex_wid.widget_update.connect(self.gopa)
        self.timer = QTimer()
        self.timer.timeout.connect(self.history_update)
        self.timer.start(1000)

        self.btn_next_page = QPushButton("Next page")
        self.btn_next_page.clicked.connect(self.hex_wid.repaint_page)

        self.btn_early_page = QPushButton("Early page")

        self.btn_delete_last = QPushButton("Cansel last")
        self.btn_delete_last.clicked.connect(self.history_del_last)

        self.btn_delete_all = QPushButton("Cansel all")
        self.btn_delete_all.clicked.connect(self.history_del_all)

        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setMaximumSize(128, 400)

    def location_on_widget(self):
        self.layout = QGridLayout()
        # self.layout = QHBoxLayout()

        #self.layout.setColumnMinimumWidth(1, 10)
        #self.layout.setColumnStretch(1, 0)

        self.layout.addWidget(self.hex_wid, 1, 0, 5, 1)
        self.layout.addWidget(self.history_list, 1, 2, 1, 2)
        self.layout.addWidget(self.btn_next_page, 3, 2)
        self.layout.addWidget(self.btn_early_page, 3, 3)
        self.layout.addWidget(self.btn_delete_last, 2, 2)
        self.layout.addWidget(self.btn_delete_all, 2, 3)
        self.setLayout(self.layout)

    def keyReleaseEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        # Enter
        if key == 16777220 and not eventQKeyEvent.isAutoRepeat():
            print("Contact")
            self.history_update()

    def history_update(self):
        change_form = copy.deepcopy(self.hex_wid.change_list)
        change_str = "column | row | old | new\n"
        for key in change_form:
            value = change_form.get(key)
            change_str += f"{key[0]} | {key[1:]} | {value[0:2]} | {value[2:4]}\n"
        self.history_list.setText(change_str)

    # TODO: добавить возможность удалять определенное кол-во изменений
    def history_del_last(self):
        self.hex_wid.history_del()

    def history_del_all(self):
        self.hex_wid.change_list = {}


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = HexTab()
    application.show()

    sys.exit(app.exec())