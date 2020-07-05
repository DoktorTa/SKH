import curses


class CheckBox:
    """
    Класс реализующий чек бокс

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **box** - Метод создает чек бокс на экране
        **change** - Метод изменяет состояние чек бокса
        **refresh_box** - Метод перересовывающий чек бокс

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **mode**: bool - Текушее положение чек бокса
    """
    mode = False

    def box(self, stdscr, x: int, y: int, text: str):
        if self.mode is True:
            text_box = "[x] " + text
            stdscr.addstr(x, y, text_box)
        elif self.mode is False:
            text_box = "[ ] " + text
            stdscr.addstr(x, y, text_box)
        return stdscr

    def change(self, stdscr, x: int, y: int, text: str):
        if self.mode is True:
            text_box = "[ ] " + text
            stdscr.addstr(x, y, text_box)
            self.mode = False
        elif self.mode is False:
            text_box = "[x] " + text
            stdscr.addstr(x, y, text_box)
            self.mode = True

    def refresh_box(self, stdscr, x: int, y: int, text: str):
        if self.mode is True:
            text_box = "[x] " + text
            stdscr.addstr(x, y, text_box, curses.A_REVERSE)
        elif self.mode is False:
            text_box = "[ ] " + text
            stdscr.addstr(x, y, text_box, curses.A_REVERSE)
