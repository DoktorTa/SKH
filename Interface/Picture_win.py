from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap


class PictureDialog(QDialog):
    __file_path = ""

    def __init__(self, file_path: str):
        super().__init__()
        self.setModal(False)

        self.__file_path = file_path
        self.__picture_show()
        # self._set_grid()

        self.show()

    def __picture_show(self):
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.__file_path)
        self.label.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(), self.pixmap.height())

    def _set_grid(self):
        self.layout = QGridLayout()

        # self.layout.addWidget(self., 1, 0)

        self.setLayout(self.layout)
