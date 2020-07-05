import curses
import curses.textpad


class CUI:
    """
    Класс реализующий основные методы интерфейсов

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **line_edit** - Метод создает область для редактирования
        **under_line** - Метод формирует зарезервированные строки
        **nav** - Метод осуществляет передвижение в списках возврашая
            результат передвижения

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **address**: str - Адрес файла работы
    """
    address = "___"

    def __init__(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def line_edit(self, stdscr, x: int, y: int, left_pos=1, right_pos=60):
        win = curses.newwin(left_pos, right_pos, x, y)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit()
        stdscr.addstr(x, y, self.address.encode('utf-8'))

        return stdscr, text

    @staticmethod
    def under_line(stdscr, status_bar_str: str):
        height, width = stdscr.getmaxyx()
        size_win = f"Width: {width}, Height: {height}"

        stdscr.addstr(height - 2, 0, size_win, curses.color_pair(1))
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, status_bar_str)
        stdscr.addstr(height - 1, len(status_bar_str), " " * (width - len(status_bar_str) - 1))
        stdscr.attroff(curses.color_pair(3))

        return stdscr

    @staticmethod
    def nav(dest: int, position: int, scope: int) -> int:
        position += dest
        if position < 0:
            position = scope - 1
        elif position >= scope:
            position = 0

        return position
