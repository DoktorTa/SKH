import os


class HexSave:
    def __init__(self, file_path: str, history: dict, block_len=1024, step=16):
        inc = 0

        history, key_list = self.__create_list(history, step)

        with open(file_path, "rb") as file_org:
            file_org_size = os.path.getsize(file_org.name)
            blocks = int(file_org_size // block_len)
            with open(file_path + "cp", "w") as file_cp:

                while blocks == inc:
                    num_byte = key_list.pop(0)
                    num_block = num_byte // block_len
                    if num_block == inc:

                    # index = str(hex(column)[2:]) + str(self.__row_num[row]): byte

    def __edit_block(self, block: bytes, num_byte: int, old_new_bytes: str, block_len=1024) -> bytes:
        num_byte_in_block = num_byte % block_len
        old_byte = "\x" + old_new_bytes[:2]
        if block[num_byte_in_block] == old_byte:
            block[num_byte_in_block] = new_byte
        return

    def __create_list(self, history: dict, step=16) -> (dict, list):
        history_sort = {}

        for key in history:
            value = history.get(key)
            print(key[0])
            column = 1
            num = int((int(key[1:]) * step) + int(column))
            history_sort.update({num: key})

        key_list = list(history_sort.keys())
        key_list.sort()

        return history_sort, key_list