import curses
import curses.textpad
from CUI import CUI
import copy
from Hex_editor import HexEdit


class CUIHex(CUI):
    """
    Класс отвечающий за интерфейс хекс редактора.

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **fat_read_hex** - Метод необходим для простого просмотра
            содержимого element_byte на экране редактора.
        **hex_editor** - Метод необходим для работы в режиме Хекс едитора.
        **edit_hex** - Метод отвечает за изменение байта на экране,
            запись этого изменениея в лог.
        **printer_hex_matrix** - Метод отвечает за отрисовку хекс таблицы.
        **hex_menu** - Метод отвечающий за отрисовку интерфейса
            хекс редактора, и перехвата нажатий пользователя.

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **address**: str - Адрес с которым работает редактор
        **hex_change_log**: list - Лист изменений внесенный в файл
        **change**: str - Изменение в данный момент
    """
    address = ""
    hex_change_log = []
    change = ""

    def __init__(self, stdscr):
        super(CUIHex, self).__init__()
        if len(self.address) != 0:
            self.hex_editor(stdscr)

    def fat_read_hex(self, stdscr, element_byte: str):
        hex_ed = HexEdit()
        file = ""
        row_in_reserved = 3
        byte_in_one_row = 16
        height, width = stdscr.getmaxyx()

        element_byte = element_byte[:(height - row_in_reserved) * byte_in_one_row]
        hex_list = hex_ed.gen_hex_out(element_byte)
        self.hex_menu(stdscr, hex_list, hex_ed, file)

    def hex_editor(self, stdscr):
        hex_ed = HexEdit()
        row_in_reserved = 3
        byte_in_one_row = -16
        height, width = stdscr.getmaxyx()

        with open(self.address, "rb") as file:
            count_row = height - row_in_reserved
            hex_ed.seek_early = count_row * byte_in_one_row

            hex_list = hex_ed.next_hex(file, count_row)
            hex_log_save = self.hex_menu(stdscr, hex_list, hex_ed, file)

        hex_ed.save_change(self.address, hex_log_save)

    def edit_hex(self, stdscr, hex_matrix: list, position_hex_x: int, position_hex_y: int):
        len_row = 9
        len_one_byte = 3

        stdscr, self.change = self.line_edit(stdscr, position_hex_x + 1, position_hex_y * len_one_byte + len_row, 1, 3)
        hex_log = [position_hex_x, position_hex_y, self.change]
        self.hex_change_log.append(hex_log)
        element_x = hex_matrix[position_hex_x]
        element_x[position_hex_y] = self.change

        return stdscr

    def printer_hex_matrix(self, stdscr, row_list: list, hex_matrix: list, row_ascii: list, position_hex_x: int, position_hex_y: int):
        len_row = 9
        len_one_byte = 3
        hex_row_line = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']

        for index, element in enumerate(hex_row_line):

            if index == position_hex_y:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            msg = '%s' % element
            stdscr.addstr(0, index * len_one_byte + len_row, msg, mode)

        # Захардкорженая хрень
        for index_x, element_x in enumerate(hex_matrix):
            for index_y, element in enumerate(element_x):

                if (index_x == position_hex_x) and (index_y == position_hex_y):
                    mode = curses.A_REVERSE
                    self.change = '%s' % element
                else:
                    mode = curses.A_NORMAL

                msg = '%s ' % element
                stdscr.addstr(index_x + 1, index_y * len_one_byte + len_row, msg, mode)

            if index_x == position_hex_x:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            stdscr.addstr(index_x + 1, 0, row_list[index_x], mode)

        return stdscr

    def hex_menu(self, stdscr, hex_list: list, hex_ed: HexEdit, file) -> list:
        k = 0
        position_hex_x = 0
        position_hex_y = 0
        hex_log_save = []

        row_list = hex_list[0]
        hex_matrix = hex_list[1]
        row_ascii = hex_list[2]

        stdscr.clear()
        stdscr.refresh()

        while k != ord('q'):
            height, width = stdscr.getmaxyx()
            stdscr.clear()

            if k == curses.KEY_DOWN:
                position_hex_x = self.nav(1, position_hex_x, len(row_list))
            elif k == curses.KEY_UP:
                position_hex_x = self.nav(-1, position_hex_x, len(row_list))
            elif k == curses.KEY_LEFT:
                position_hex_y = self.nav(-1, position_hex_y, 16)
            elif k == curses.KEY_RIGHT:
                position_hex_y = self.nav(1, position_hex_y, 16)
            if type(file) != str:
                if k == curses.KEY_ENTER or k == 10:
                    stdscr = self.edit_hex(stdscr, hex_matrix, position_hex_x, position_hex_y)
                elif k == curses.KEY_F4:
                    count_row = height - 3
                    hex_list = hex_ed.next_hex(file, count_row)
                    row_list = hex_list[0]
                    hex_matrix = hex_list[1]
                    row_ascii = hex_list[2]
                elif k == curses.KEY_F5:
                    count_row = height - 3
                    if hex_ed.seek_early > 0:
                        hex_list = hex_ed.early_hex(file, count_row)
                        row_list = hex_list[0]
                        hex_matrix = hex_list[1]
                        row_ascii = hex_list[2]
                elif k == curses.KEY_F6:
                    hex_log_save = copy.deepcopy(self.hex_change_log)

                statusbarstr = "Press 'q' to exit | 'ENTER' to edit | 'F4' to next page | 'F5' to early page | 'F6' to save change"
            else:
                statusbarstr = "Press 'q' to exit |"

            stdscr = self.printer_hex_matrix(stdscr, row_list, hex_matrix, row_ascii, position_hex_x, position_hex_y)
            stdscr = self.under_line(stdscr, statusbarstr)

            stdscr.refresh()

            k = stdscr.getch()

        return hex_log_save
