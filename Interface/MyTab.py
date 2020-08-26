import sys
import webbrowser
import copy

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon, QFont

from Interface.Hex_Wiget import HexWidget
from Interface.Hex_Tab import HexTab
from Interface.ELF_Tab import ELFTab, InvalidFileTypeException
from Interface.Total_Com_Tab import TotalTab


# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.__close_tab)

        self.tabs.resize(300, 200)

        # Add tabs

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #self.l.setText("This is the first tab")

    def __close_tab(self, currentIndex):
        currentQWidget = self.tabs.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabs.removeTab(currentIndex)

    def tab_total_com(self, file, fs: str):
        self.total_com = TotalTab()

        if fs == "FAT":
            self.total_com.fat_load(file)
        elif fs == "EXT":
            self.total_com.ext_load(file)

        self.tab2 = QWidget()

        self.tabs.addTab(self.tab2, "Total com")

        self.tab2.layout = QHBoxLayout()
        self.tab2.layout.addWidget(self.total_com)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab_elf(self, file_path: str):

        with open(file_path, "rb") as file:
            try:
                self.elf = ELFTab(file)
            except InvalidFileTypeException:
                return

        self.tab3 = QWidget()

        self.tab3.layout = QHBoxLayout()
        self.tab3.layout.addWidget(self.elf)
        self.tab3.setLayout(self.tab3.layout)

        self.tabs.addTab(self.tab3, "ELF")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab_hex(self, file):
        self.hex_wid = HexTab(file)

        self.tab1 = QWidget()

        self.tab1.layout = QHBoxLayout()
        self.tab1.layout.addWidget(self.hex_wid)
        self.tab1.setLayout(self.tab1.layout)

        self.tabs.addTab(self.tab1, "Hex")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

