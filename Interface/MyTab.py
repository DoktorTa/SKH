import sys
import webbrowser
import copy

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

from Interface.Hex_Wiget import HexWidget
from Interface.Hex_Tab import HexTab
from Interface.ELF_Tab import ELFTab
from Interface.Total_Com_Tab import TotalTab


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
        self.tabs.addTab(self.tab2, "Total com")
        self.tabs.addTab(self.tab3, "ELF")

        self.tab_hex()
        self.tab_elf()
        self.tab_total_com()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #self.l.setText("This is the first tab")

    def tab_total_com(self):
        self.total_com = TotalTab()

        self.tab2.layout = QHBoxLayout()
        self.tab2.layout.addWidget(self.total_com)
        self.tab2.setLayout(self.tab2.layout)


    def tab_elf(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            self.elf = ELFTab(file)

        self.tab3.layout = QHBoxLayout()
        self.tab3.layout.addWidget(self.elf)
        self.tab3.setLayout(self.tab3.layout)

    def tab_hex(self):
        self.hex_wid = HexTab()

        self.tab1.layout = QHBoxLayout()
        self.tab1.layout.addWidget(self.hex_wid)
        self.tab1.setLayout(self.tab1.layout)

