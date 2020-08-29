import logging

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTabWidget

from Interface.Hex_Tab import HexTab
from Interface.ELF_Tab import ELFTab, InvalidFileTypeException
from Interface.Total_Com_Tab import TotalTab


class TabWidgetManager(QWidget):
    """
        Класс который отвечает за открытие фкладок с модулями и предоставление им файлов.
    """

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.__close_tab)

        self.tabs.resize(300, 200)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @staticmethod
    def __create_property_file(tab, file_path: str):
        """
            Метод открывает файл в режиме "rb" добовляя его обьект во вкладку модуля.
            Нужен для модулей которым требуется постоянно открытый файл.
        """
        tab.file = open(file_path, 'rb')
        return tab

    @staticmethod
    def __delete_property_file(tab):
        """
            Метод гарантирует закрытие файла из вкладки модуля.
        """
        try:
            tab.file.close()
        except ProcessLookupError:
            logging.error(f"This file is close")
        return tab

    def __close_tab(self, current_index):
        current_widget = self.tabs.widget(current_index)
        self.__delete_property_file(current_widget)
        current_widget.deleteLater()
        self.tabs.removeTab(current_index)

    def __choice_fs(self, fs: str):
        """
            Запускает выбранный тип файловой системы.
        """
        if fs == "FAT":
            self.total_com.fat_load(self.tab_fs_com_sys.file)
        elif fs == "EXT":
            self.total_com.ext_load(self.tab_fs_com_sys.file)

    def tab_total_com(self, file_path, fs: str):
        """
            Вкладка виджета модуля файловой системы.
        """
        self.total_com = TotalTab()
        self.tab_fs_com_sys = QWidget()
        self.tab_fs_com_sys = self.__create_property_file(self.tab_fs_com_sys, file_path)

        self.__choice_fs(fs)

        self.tabs.addTab(self.tab_fs_com_sys, f"{fs}")

        self.tab_fs_com_sys.layout = QHBoxLayout()
        self.tab_fs_com_sys.layout.addWidget(self.total_com)
        self.tab_fs_com_sys.setLayout(self.tab_fs_com_sys.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab_elf(self, file_path: str):
        """
            Вкладка виджета модуля исполняемых файлов.
        """

        with open(file_path, "rb") as file:
            try:
                self.elf = ELFTab(file)
            except InvalidFileTypeException:
                logging.error(f"It's not elf file: {file_path}")
                return

        self.tab_executable_file = QWidget()

        self.tab_executable_file.layout = QHBoxLayout()
        self.tab_executable_file.layout.addWidget(self.elf)
        self.tab_executable_file.setLayout(self.tab_executable_file.layout)

        self.tabs.addTab(self.tab_executable_file, "ELF")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab_hex(self, file_path: str):
        """
            Вкладка виджета модуля шестнадцатиричного редактора.
        """

        self.tab_hex_ed = QWidget()
        self.tab_hex_ed = self.__create_property_file(self.tab_hex_ed, file_path)
        self.hex_wid = HexTab(self.tab_hex_ed.file)

        self.hex_wid.set_file_path(file_path)

        self.tab_hex_ed.layout = QHBoxLayout()
        self.tab_hex_ed.layout.addWidget(self.hex_wid)
        self.tab_hex_ed.setLayout(self.tab_hex_ed.layout)

        self.tabs.addTab(self.tab_hex_ed, "Hex")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

