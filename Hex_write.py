import os


class WriterHex:
    """
    Класс отвечаюший за запись в файл.

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **write_one_byte** - Метод отвечающий за запись в файл,
            сначала создает новый файл в котором проводит изменение,
            после удаляет родительский и переименовывет созданный.
    """
    @staticmethod
    def write_one_byte(address: str, hex_change: list):
        file_changes = "helps_on_work.txt"

        position_row = int(hex_change[0])
        position_table = int(hex_change[1])
        byte_change = hex_change[2]

        seek_cahge = (position_row * 16) + position_table

        with open(address, "rb") as file:
            with open(file_changes, "wb") as file_h:
                b = file.read(seek_cahge)
                file_h.write(b)
                file_h.write(byte_change)
                file.seek(1, 1)
                file_h.write(file.read())
        os.remove(address)
        os.rename(file_changes, address)
