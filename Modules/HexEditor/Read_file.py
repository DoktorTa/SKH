import logging


class HexOpen:
    __file = 0
    __len_block = 1024

    def __init__(self, file, len_block=1024):
        self.__file = file
        self.__len_block = len_block

    @property
    def get_len_block(self) -> int:
        return self.__len_block

    def get_page(self, early=False) -> (bytes, int):
        error = 0
        data = b''

        if early is True:
            self.__file.seek(self.__len_block, 1)

        try:
            data = self.__file.read(self.__len_block)
        except ValueError:
            logging.error(f"Program can not read file: {self.__len_block, self.__file.name}")
            error = -1

        return data, error
