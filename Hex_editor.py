from OutHex import OutHex
from Hex_write import WriterHex


class HexEdit:
    """
    Класс отвечающий за взаимодействие с классами изменения
        и распечатывания байтов файла.

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **next_hex** - Метод отвечает за генерацию следующей страницы
            вывода файля типа: [Лист строк, Лист листов байт, Лист аски].
        **early_hex** - Метод отвечает за генерацию предыдущей страницы
            вывода файла типа: [Лист строк, Лист листов байт, Лист аски].
        **save_change** - Метод отвечает за запись изменений в файл,
            работает отдельно с каждым изменением.
        **gen_hex_out** - Метод отвечает за генрацию листов хекс вывода.

    Атрибуты:
    ~~~~~~~~~~~~~~~~~~
        **seek_next**: int - Смешение для последующей страницы.
        **seek_early**: int - Смешение для предыдушей страницы.
        **row_count**: int - Номер последнего столбца на странице.
    """
    seek_next = 0
    seek_early = 0
    row_count = -10

    def next_hex(self, file, count_row: int) -> list:
        byte_in_one_row = 16

        read_on_file = count_row * byte_in_one_row
        file.seek(self.seek_next)
        self.seek_next += read_on_file
        self.seek_early += read_on_file

        byte_str = file.read(read_on_file)
        hex_str = byte_str.hex()
        hex_list = self.gen_hex_out(hex_str)

        return hex_list

    def early_hex(self, file, count_row: int) -> list:
        byte_in_one_row = 16

        read_on_file = count_row * byte_in_one_row
        self.seek_next -= read_on_file
        self.seek_early -= read_on_file
        self.row_count = self.row_count - (count_row * 20)
        file.seek(self.seek_early)

        byte_str = file.read(read_on_file)
        hex_str = byte_str.hex()
        hex_list = self.gen_hex_out(hex_str)

        return hex_list

    @staticmethod
    def save_change(address: str, hex_log: list):
        write = WriterHex()
        while len(hex_log) != 0:
            one_change = hex_log.pop(0)
            change = one_change[2]
            byte = bytes.fromhex(change)
            one_change[2] = byte
            write.write_one_byte(address, one_change)

    def gen_hex_out(self, hex_str: str) -> list:
        out = OutHex()
        out.row = self.row_count
        hex_list = out.creator(hex_str)
        self.row_count = out.row
        return hex_list
