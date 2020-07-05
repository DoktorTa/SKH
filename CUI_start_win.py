import curses
import curses.textpad
from CUI import CUI
from Check_box import CheckBox


class CUI_start(CUI):
    """
    Класс отвечающий за экран начала работы, его задачей является:
        * Определение режама работы программы
        * Задание адреса файла в ФС
        * Приведение читателя кода в ужас

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **start_menu** - Метод отвечаюший за отрисовку стартового экрана

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **box_flag**: bool - Положение чекбокса для определения режима работы
            1) False - Работа как ФС ридер
            2) True - Работа как Хекс редактор
        **address**: str - Имя файла с которым будет работать ФС ридер или
            Хекс редактор
    """
    box_flag = False

    def __init__(self, stdscr):
        super(CUI_start, self).__init__()
        self.start_menu(stdscr)

    def start_menu(self, stdscr):
        k = 0
        cursor_x = 0
        cursor_y = 1
        text_check = "Open for reading only hex editor"
        next = "Enter"

        stdscr.clear()
        stdscr.refresh()

        b = CheckBox()

        while k != ord('q'):
            height, width = stdscr.getmaxyx()
            size_monitor_y = (width // 3)
            size_monitor_x = (height // 5) * 2
            curses.curs_set(0)
            stdscr.clear()

            if k == curses.KEY_DOWN:
                cursor_x = (cursor_x + 1) % 3
            elif k == curses.KEY_UP:
                cursor_x = (cursor_x - 1) % 3
            elif cursor_x == 0 and (k == curses.KEY_ENTER or k == 10):
                stdscr, self.address = self.line_edit(stdscr, size_monitor_x, size_monitor_y)
            elif (k == curses.KEY_ENTER or k == 10) and cursor_x == 1:
                b.change(stdscr, size_monitor_x + 1, size_monitor_y, text_check)
                self.box_flag = b.mode
            elif (k == curses.KEY_ENTER or k == 10) and cursor_x == 2:
                break

            statusbarstr = "Press 'q' to exit |"
            stdscr = self.under_line(stdscr, statusbarstr)

            if cursor_x == 0:
                stdscr.addstr(size_monitor_x, size_monitor_y, self.address.encode('utf-8'), curses.A_REVERSE)
                stdscr = b.box(stdscr, size_monitor_x + 1, size_monitor_y, text_check)
                stdscr.addstr(size_monitor_x + 2, size_monitor_y, next)  # , curses.color_pair(1))
            elif cursor_x == 1:
                stdscr.addstr(size_monitor_x, size_monitor_y, self.address.encode('utf-8'))
                b.refresh_box(stdscr, size_monitor_x + 1, size_monitor_y, text_check)
                stdscr.addstr(size_monitor_x + 2, size_monitor_y, next)  # , curses.color_pair(1))
            elif cursor_x == 2:
                stdscr = b.box(stdscr, size_monitor_x + 1, size_monitor_y, text_check)
                stdscr.addstr(size_monitor_x, size_monitor_y, self.address.encode('utf-8'))
                stdscr.addstr(size_monitor_x + 2, size_monitor_y, next, curses.A_REVERSE)

            stdscr.refresh()

            k = stdscr.getch()

