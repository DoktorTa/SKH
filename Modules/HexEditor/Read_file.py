import math
import logging
import os


class HexOpen:
    __file = 0
    __len_block = 1024

    def __init__(self, file, len_block=1024):
        self.__file = file
        self.__len_block = len_block

    @property
    def get_len_block(self) -> int:
        return self.__len_block

    def get_data(self, count: int) -> (bytes, int):
        data_group = b''
        error = 0

        if count < 0:
            size_file = os.path.getsize(self.__file.name)
            back_to_file = -self.__len_block * int(math.fabs(count))
            if (back_to_file < -size_file) or (self.__file.tell() > back_to_file):
                self.__file.seek(0)
            else:
                self.__file.seek(back_to_file, 1)

        for inc in range(int(math.fabs(count))):
            data_page, error = self._get_page()
            data_group += data_page
            if error == -1:
                return data_group, error

        return data_group, error

    def _get_page(self) -> (bytes, int):
        error = 0
        data_page = b''

        try:
            data_page = self.__file.read(self.__len_block)
        except ValueError:
            logging.error(f"Program can not read file: {self.__len_block, self.__file.name}")
            error = -1

        return data_page, error
