import sys

from PyQt5.QtWidgets import QApplication

from Interface.GUI_HeX import GUIMasterWin

app = QApplication(sys.argv)
ex = GUIMasterWin()
sys.exit(app.exec_())