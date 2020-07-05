class OutHex:
    """
    Класс отвечающий за построение страницы хекс вывода.

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **creator** - Метод отвечающий за сбор страницы хекс вывода
            возвращает лист со структурой:
            [Лист строк, Лист байт, Лист аски символов].
        **row_counter** - Метод отвечающий за счет строки(ее номер).
        **row_ascii** - Метод Отвечающий за создание строки аски символов.
        **row_converter** - Метод отвечающий за создание листа байт.
        **matrix_creator** - Метод отвечающий за создания хекс строки.

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **row**: int - Номер текушей строки.
    """
    row = -10

    def creator(self, claster: str) -> list:
        j = 32
        hex_list = []
        row_list = []
        ascii_list = []
        hex_matrix = []

        while len(claster) != 0:
            row_hex = claster[:j]
            claster = claster[j:]

            row_num, row_hex, row_ascii = self.matrix_creator(row_hex)
            row_list.append(row_num)
            hex_matrix.append(row_hex)
            ascii_list.append(row_ascii)

        hex_list.append(row_list)
        hex_list.append(hex_matrix)
        hex_list.append(ascii_list)
        return hex_list

    def row_counter(self) -> str:
        self.row = self.row + 10
        row = str(f'{self.row:08d}')
        return row

    @staticmethod
    def row_ascii(name_h: str) -> str:
        j = 2
        name = ""
        row_ascii = []

        while len(name_h) != 0:
            name += chr(int(name_h[:j], 16))
            name_h = name_h[j:]
            row_ascii.append(name)

        return name

    @staticmethod
    def row_converter(row_hex: str) -> list:
        j = 2
        row_hex_out = []

        while len(row_hex) != 0:
            row = row_hex[:j]
            row_hex = row_hex[j:]
            row_hex_out.append(row)

        return row_hex_out

    def matrix_creator(self, row_hex: str) -> [str, list, str]:
        row_num = self.row_counter()
        row_ascii = self.row_ascii(row_hex)
        row_hex = self.row_converter(row_hex)
        return row_num, row_hex, row_ascii
