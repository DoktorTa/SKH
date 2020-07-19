import sys
import webbrowser
import copy

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

from Interface.Hex_Wiget import HexWidget
from Interface.Hex_Tab import HexTab

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

        self.hex_wid = HexTab()


        self.tab1.layout = QHBoxLayout()
        self.tab1.layout.addWidget(self.hex_wid)
        self.tab1.setLayout(self.tab1.layout)

