import logging
import math
import copy

from Modules.FS.EXT2_data import EXT2Data
from Modules.FS.EXT2_read import EXT2Reader
from Modules.FS.Interface_FS import IFSWork


class CommandEXT2(IFSWork):
    """
        Класс командной системы для фс ext2

        Обеспечивает команды для:
            * Перемешения по директориям
            * Чтение определенного колличества блоков из файла в директории
    """
    __ext2_fs = 0
    __root = []
    __pwd = ""

    def __init__(self, ext2_fs: EXT2Reader):
        self.__ext2_fs = ext2_fs
        self.__root = self.__ext2_fs.root_catalog_read()
        self.__root = self._conversion(self.__root)

    @staticmethod
    def _conversion(catalog_old: list) -> list:
        """
            Метод преобразует лист инода в стандартный для фс лист элемента.
            [Номер инода, Длинна записи, длинна имени, Тип записи, Имя в аски кодировке]
            ->
            [Имя, Аттрибут, Дата последней записи, Размер в байтах, Номер первого кластера элемента, Длинное имя]
        """
        # TODO: Реализовать конвертацию по средством чтения инода для более полного заполнения листа элемента.
        catalog_new = []

        for element_old in catalog_old:
            file_type = element_old[3]

            if file_type == "02":
                file_type = "D"
            else:
                file_type = "F"

            element_new = [element_old[4], file_type, 0, 0, element_old[0], 0]

            root_file = ['', 'F', 0, 0, '00000000', 0]
            if element_new == root_file:
                continue

            catalog_new.append(element_new)

        return catalog_new

    def cd(self, dir_now: list, num_in_dir: int) -> (list, int):
        error = 0
        catalog = []

        try:
            element_dir = dir_now[num_in_dir]
            inode_num = int(element_dir[4], 16)
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return dir_now, error

        elements_list = self.__ext2_fs.inode(inode_num)
        for block in elements_list:
            # TODO: Можно добавить механизм выдачи больших каталогов, но я думаю памяти хватит и так.
            if block == 0:
                break

            part_catalog_hex = self.__ext2_fs.read_block(block).hex()
            part_catalog = self.__ext2_fs.linked_directory_entry(part_catalog_hex)
            part_catalog = self._conversion(part_catalog)
            catalog += part_catalog

        return catalog, error

    def read(self, dir_now: list, num_in_dir: int, count: int, pointer: int) -> (str, int, int):
        # TODO: !!!НЕОБХОДИМО!!! Буфферы для листов блоков.
        error = 0
        blocks = ""
        count_s = 0

        try:
            element_dir = dir_now[num_in_dir]
            inode_num = int(element_dir[4], 16)
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return "", 0, error

        elements_list = self.__ext2_fs.inode(inode_num)
        if count < 0:
            count_s = copy.deepcopy(count)
            pointer += count_s
            count = int(math.fabs(count))

        for inc in range(count):
            try:
                block = elements_list[pointer]
                pointer += 1
            except LookupError:
                error = -1
                logging.error(f"No reading is possible. All blocks: {len(elements_list)}, required item: {pointer}")
                break
            block_hex = self.__ext2_fs.read_block(block).hex()
            blocks += block_hex

        if count_s < 0:
            pointer += count_s

        return blocks, pointer, error

    def pwd(self) -> str:
        # TODO: реализовать.
        return self.__pwd

    def root(self) -> list:
        return self.__root


if __name__ == '__main__':
    with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as file:
        logging.basicConfig(level=logging.DEBUG)
        data = EXT2Data()
        p = EXT2Reader(data, file)
        com = CommandEXT2(p)
        root = com.root()
