import sys
import webbrowser
import copy

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,\
    QMainWindow, QTextEdit, QFileDialog, QLabel, QHBoxLayout, QTabWidget, QGridLayout
from PyQt5.QtGui import QIcon, QFont, QColor

from Modules.ExecutableFiles.ELF_read import ELFReader

class ELFTab(QWidget):

    def __init__(self):
        super().__init__()
        self.elf_hendler()

    def elf_hendler(self):

