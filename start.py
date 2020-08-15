import sys

from PyQt5.QtWidgets import QApplication

from Interface.GUI_HeX import Hex_view

app = QApplication(sys.argv)
ex = Hex_view()
sys.exit(app.exec_())