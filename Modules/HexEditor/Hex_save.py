import os
from bitstring import BitArray


class HexSave:
    def __init__(self, file_path: str, history: dict, step=16):
        seek_in_file_last = 0

        history, key_list = self.__create_list(history, step)
        with open(file_path, "rb") as file:
            with open(file_path + "cp", "wb") as file_new:

                while len(key_list) != 0:
                    seek_in_file = key_list.pop(0)
                    byte_old_new = history.get(seek_in_file)

                    if seek_in_file_last == 1:
                        seek_in_file_last = 2

                    file.seek(seek_in_file_last)
                    byte_no_change = file.read(seek_in_file - seek_in_file_last)
                    file_new.write(byte_no_change)
                    change_byte = file.read(1)

                    if change_byte == BitArray(hex=byte_old_new[:2]).bytes:
                        change_byte = BitArray(hex=byte_old_new[-2:]).bytes
                        file_new.write(change_byte)

                    seek_in_file_last = seek_in_file + 1
                else:
                    file_size = os.path.getsize(file.name)
                    byte_no_change = file.read(file_size - seek_in_file_last)
                    file_new.write(byte_no_change)

        self.__end_save(file_path)

    @staticmethod
    def __end_save(file_path: str):
        os.remove(file_path)
        os.rename(file_path + "cp", file_path)

    @staticmethod
    def __create_list(history: dict, step=16) -> (dict, list):
        history_sort = {}

        for key in history:
            value = history.get(key)
            column = int(key[0:1], step)
            num = int((int(key[1:])) + int(column))
            history_sort.update({num: value})

        key_list = list(history_sort.keys())
        key_list.sort()

        return history_sort, key_list

