import sys
import webbrowser
import copy

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

from Hex_Wiget import HexWidget


# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Hex")
        self.tabs.addTab(self.tab2, "For")
        self.tabs.addTab(self.tab3, "Geeks")

        self.tab_hex()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #self.l.setText("This is the first tab")

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

        btn_next_page = QPushButton("Next page")
        btn_next_page.clicked.connect(self.hex_wid.repaint_page)

        btn_early_page = QPushButton("Early page")

        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setMaximumSize(128, 400)

        # {'700000010': '1722'}
        # history_list.setText()

        self.tab1.layout = QHBoxLayout()
        self.tab1.layout.addWidget(self.hex_wid)
        self.tab1.layout.addWidget(btn_next_page)
        self.tab1.layout.addWidget(btn_early_page)
        self.tab1.layout.addWidget(self.history_list)
        self.tab1.setLayout(self.tab1.layout)

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

