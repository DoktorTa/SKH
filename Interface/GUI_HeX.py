import webbrowser
import os

from PyQt5.QtWidgets import QToolTip, QMessageBox, QDesktopWidget, QAction, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon, QFont

from Interface.Tab_manager import TabWidgetManager
from Interface.New_progect_win import NewProgectWin


class GUIMasterWin(QMainWindow):
    """
        Класс управляющий основным окном иинтерфейса.
    """
    __file_path = ""

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is ЭКРАН')

        self.__start_tabs()
        self.menu_bar_init()

        self.resize(1080, 720)
        self._center()
        self.setWindowTitle('SectionKHex')
        self.show()

    def __start_tabs(self):
        self.tab_widget = TabWidgetManager(self)
        self.setCentralWidget(self.tab_widget)

    def _file_serch(self):
        """
            Функция получает путь до файла.
        """
        file_name = QFileDialog.getOpenFileName(self, "Open files", "/home/jana")
        self.__file_path = file_name[0]

    def __project_open(self):
        self.new_project = NewProgectWin()

        if self.new_project.exec_():
            self.__file_path = self.new_project.get_file_path
            self.__start_project(self.new_project.get_mode)
        else:
            pass

    def __start_project(self, mode: int):
        """
            Функция звпускает проект с выбраным модом

            На самом деле хотелось бы изменить систему выбора,
             возможно стоит передовать лист с модами изначально или вытаскивать его,
             пока подумаю над зависимостями.
        """
        if mode == 1:
            self._open_hex()
        elif mode == 2:
            self._open_fat()
        elif mode == 3:
            self._open_ext()
        elif mode == 4:
            self._open_elf()

    def _open_hex(self):
        if self.__file_path != "":
            self.tab_widget.tab_hex(self.__file_path)

    def _open_elf(self):
        if self.__file_path != "":
            self.tab_widget.tab_elf(self.__file_path)

    def _open_fat(self):
        if self.__file_path != "":
            self.tab_widget.tab_total_com(self.__file_path, "FAT")

    def _open_ext(self):
        if self.__file_path != "":
            self.tab_widget.tab_total_com(self.__file_path, "EXT")

    # Любые события должны быть созданы и зарегестрированны в меню бар.
    def menu_bar_init(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.setWindowIcon(QIcon(path + r"\icon\logo.png"))

        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.setIcon(QIcon(path + r"\icon\exit.png"))
        exit_action.triggered.connect(self.close)

        open_file_action = QAction('&Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open new file')
        open_file_action.setIcon(QIcon(path + r"\icon\open.png"))
        open_file_action.triggered.connect(self.__project_open)
        # self.statusBar()
        help_action = QAction('&Git progect', self)
        help_action.setShortcut('Ctrl+H')
        help_action.setStatusTip('Open git this progect')
        help_action.setIcon(QIcon(path + r'\icon\help.png'))
        help_action.triggered.connect(lambda: webbrowser.open('https://github.com/DoktorTa/SKH'))

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_file_action)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(help_action)

    # Диологовое окно перед выходом.
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Центрирование окна приложения, стоит убрать, ибо зачем?
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
