from PyQt5.QtWidgets import QPushButton, QFileDialog, QComboBox, QDialog,\
    QLineEdit, QGridLayout


class NewProjectWin(QDialog):
    __file_path = ""
    __mode = 0
    _mode_list = {"Hex": 1,
                  "FAT32, FAT16": 2,
                  "ext2": 3,
                  "elf": 4}

    def __init__(self):
        super().__init__()

        self.setModal(True)
        self.setMinimumSize(350, 100)
        self.setWindowTitle("Open Project")

        self.__create_file_line()
        self.__create_file_but()
        self.__create_selection_list()
        self.__create_accept_button()
        self._set_grid()

        self.show()

    def __create_file_line(self):
        self.file_path = QLineEdit()
        self.file_path.setMinimumSize(250, 20)
        self.file_path.setReadOnly(True)

    def __set_file_path(self, file_path: str):
        self.__file_path = file_path
        self.file_path.setText(file_path)

    def __search_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open files", "/home/t")
        self.__set_file_path(file_name[0])

    def __create_file_but(self):
        self.open_file_button = QPushButton('Open file')
        self.open_file_button.clicked.connect(self.__search_file)

    def __set_mode(self, text: str):
        self.__mode = self._mode_list.get(text)

    def __create_selection_list(self):
        self.mode_choice = QComboBox()

        for key in self._mode_list:
            self.mode_choice.addItem(key)

        self.mode_choice.activated[str].connect(self.__set_mode)

    def __create_accept_button(self):
        self.accept_but = QPushButton("Accept")
        self.accept_but.clicked.connect(self.accept)

    def _set_grid(self):
        self.layout = QGridLayout()

        self.layout.addWidget(self.file_path, 1, 0)
        self.layout.addWidget(self.open_file_button, 1, 1)
        self.layout.addWidget(self.mode_choice, 0, 0)
        self.layout.addWidget(self.accept_but, 0, 1)

        self.setLayout(self.layout)

    @property
    def get_file_path(self) -> str:
        return self.__file_path

    @property
    def get_mode(self) -> int:
        return self.__mode
