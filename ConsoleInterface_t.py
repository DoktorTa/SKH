import curses
import curses.textpad
from CUI_start_win import CUI_start
from CUI_fs_menu import CUI_FS_menu
from CUI_hex_menu import CUIHex


def main():
    cui_s = CUI_start
    cui_s = curses.wrapper(cui_s)
    work_flag = cui_s.box_flag

    if work_flag is True:
        cui_hex = CUIHex
        cui_hex.address = cui_s.address
        curses.wrapper(cui_hex)
    elif work_flag is False:
        cui_fs = CUI_FS_menu
        cui_fs.address = cui_s.address
        curses.wrapper(CUI_FS_menu)


if __name__ == '__main__':
    main()
