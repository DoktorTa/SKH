import logging
import math

from Modules.FS.EXT2_data import EXT2Data
from Modules.FS.EXT2_read import EXT2Reader
from Modules.FS.Interface_FS import IFSWork


class CommandEXT2(IFSWork):
    __ext2_fs = 0
    __root = []
    __pwd = ""

    def __init__(self, ext2_fs: EXT2Reader):
        self.__ext2_fs = ext2_fs
        self.root = self.__ext2_fs.root_catalog_read()
        self.root = self._conversion(self.root)

    @staticmethod
    def _conversion(catalog_old: list) -> list:
        """
            [inode_num, rec_len, name_len, file_type, name_ascii]
            ->
            [Имя, Аттрибут, Дата последней записи, Размер в байтах, Номер первого кластера элемента, Длинное имя]
        """
        catalog_new = []

        for element_old in catalog_old:
            file_type = element_old[3]

            if file_type == "":
                file_type = "D"
            else:
                file_type = "F"

            element_new = [element_old[4], file_type, 0, 0, element_old[0], 0]
            catalog_new.append(element_new)

        return catalog_new

    def cd(self, dir_now: list, num_in_dir: int) -> (list, int):
        catalog = []
        error = 0

        try:
            element_dir = dir_now[num_in_dir]
            inode_num = int(element_dir[4], 16)
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return dir_now, error

        elements_list = self.__ext2_fs.inode(inode_num)
        for block in elements_list:
            if block == "00000000":
                break

            part_catalog_hex = self.__ext2_fs.read_block(int(block, 16)).hex()
            part_catalog = self.__ext2_fs.linked_directory_entry(part_catalog_hex)
            part_catalog = self._conversion(part_catalog)
            catalog += part_catalog

        return catalog, error

    def read(self, dir_now: list, num_in_dir: int, count: int, pointer: int) -> (str, list, int, int):
        catalog = []
        error = 0
        blocks = ""
        step = 1

        try:
            element_dir = dir_now[num_in_dir]
            inode_num = int(element_dir[4], 16)
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return "", [], 0, error

        elements_list = self.__ext2_fs.inode(inode_num)
        if count < 0:
            count = math.fabs(count)
            step = -1

        for i in range(count):
            try:
                block = elements_list[pointer]
                pointer += step
            except LookupError:
                error = -1
                logging.error(f"No reading is possible. All blocks: {len(elements_list)}, required item: {pointer}")
                return blocks, elements_list, pointer, error
            block_hex = self.__ext2_fs.read_block(int(block, 16)).hex()
            blocks += block_hex

        return blocks, elements_list, pointer, error

    def pwd(self) -> str:
        return self.__pwd

    def root(self) -> list:
        return self.__root


if __name__ == '__main__':
    with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as file:
        logging.basicConfig(level=logging.DEBUG)
        data = EXT2Data()
        p = EXT2Reader(data, file)
        com = CommandEXT2(p)
        root = com.root
        print(root)
        c, e, p, i = com.read(root, 3, 1, 0)
        print(c, e, p, i)
