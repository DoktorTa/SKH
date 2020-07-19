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
        self.hex_wid = HexTab()

        self.tab1.layout = QHBoxLayout()
        self.tab1.layout.addWidget(self.hex_wid)
        self.tab1.setLayout(self.tab1.layout)

