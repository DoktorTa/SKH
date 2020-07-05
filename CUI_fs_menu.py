import copy

import curses
import curses.textpad

from CUI import CUI
from comand_sys import Command
from CUI_hex_menu import CUIHex


class CUI_FS_menu(CUI):
    """
    ну
    Класс отвечаюший за работу с ФС:
        * Перемешение по дирректориям
        * Чтение элементов в Хекс едитор

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **reader_fs_menu** - Метод отвечает за отрисовку меню и перехвата
            нажатий пользователя.
        **next_dir** - Метод отвечаюший за вызов директории и подготовку
            ее к отрисовке.
        **read_hex** - Метод отвечающий за передачу управления Хекс едитору.
        **printer_element** - Метод отвечающий за отрисовку диреектории на
            экране.
        **create_element_line** - Метод отвечающий за создание линии файла,
            Название Тип Вермя создания.
        **convert_data** - Метод отвечающий за конвертацию формата даты.

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **address**: str - Адресс с по которому находиться ФС.
        **position**: int - Позиция курсора.
        **elements**: list - Элементы находяшиеся на экране.
    """
    address = ""
    position = 0
    elements = []

    def __init__(self, stdscr):
        super(CUI_FS_menu, self).__init__()
        self.reder_fs_menu(stdscr)

    def reder_fs_menu(self, stdscr):
        k = 0
        error = ""
        stdscr.clear()
        stdscr.refresh()

        mount_file_sys = open(self.address, "rb")
        c = Command(mount_file_sys)
        catalog = copy.deepcopy(c.root)
        height, width = stdscr.getmaxyx()
        self.create_element_line(width, copy.deepcopy(catalog))

        while k != ord('q'):
            curses.curs_set(0)
            stdscr.clear()

            if k == curses.KEY_DOWN:
                self.position = self.nav(1, self.position, len(self.elements))
            elif k == curses.KEY_UP:
                self.position = self.nav(-1, self.position, len(self.elements))
            elif k == curses.KEY_F3:
                self.read_hex(mount_file_sys, stdscr, c, catalog)
            elif k == curses.KEY_ENTER or k == 10:
                stdscr, error, catalog = self.next_dir(stdscr, mount_file_sys, c, catalog)

            stdscr = self.printer_element(stdscr)

            statusbarstr = "Press: 'q' to exit | 'F3' to read element | 'ENTER' to next dir | " + c.pwd + error
            error = ""
            stdscr = self.under_line(stdscr, statusbarstr)

            stdscr.refresh()

            k = stdscr.getch()

    def next_dir(self, stdscr, mount_file_sys, c: Command, catalog: list) -> [object, str, list]:
        height, width = stdscr.getmaxyx()
        attr_dir = "10"
        element = catalog[self.position]

        if element[1] == attr_dir:
            catalog, error = c.cd(mount_file_sys, copy.deepcopy(catalog), self.position)
            self.position = 0
            stdscr.clear()
            self.create_element_line(width, copy.deepcopy(catalog))
            stdscr.refresh()
        else:
            error = "no 'F', only 'd'"

        return stdscr, error, catalog

    def read_hex(self, mount_file_sys, stdscr, c: Command, catalog: list):
        claster_sequence = [1]

        while len(claster_sequence) != 0:
            element_byte, claster_sequence, error = c.read(mount_file_sys, copy.deepcopy(catalog), self.position)
            cui_h = CUIHex(stdscr)
            cui_h.fat_read_hex(stdscr, element_byte)
        stdscr.clear()

    def printer_element(self, stdscr) -> [object]:
        for index, element in enumerate(self.elements):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = '%s' % element
            stdscr.addstr(1 + index, 1, msg, mode)

        return stdscr

    def create_element_line(self, width: int, catalog: list):
        attr_dir = "10"
        recursion = ".          "
        back = "..         "
        self.elements = []

        while len(catalog) != 0:
            element = catalog.pop(0)
            element_name = element[0]
            element_attr = element[1]
            element_create_data = element[2]

            if element_name == recursion:
                element_name = "Recursion  "
            elif element_name == back:
                element_name = "Back       "

            if element_attr == attr_dir:
                element_attr = "D:"
            else:
                element_attr = "F:"

            element_create_data = self.convert_data(element_create_data)
            space_num = (width // 2) - len(element_name) - len(element_create_data) - len(element_attr)
            element = str(element_name) + (space_num * " ") + element_attr + element_create_data
            self.elements.append(element)

    @staticmethod
    def convert_data(element_data: str) -> str:
        start_new_era = 1980

        element_data = int(element_data, 16)
        year = element_data >> 9
        month = (element_data - (year << 9)) >> 5
        day = element_data - ((element_data >> 5) << 5)
        year += start_new_era
        data = str(f'{day:02d}') + "." + str(f'{month:02d}') + "." + str(f'{year:04d}')

        return data
