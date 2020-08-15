import copy
import logging
import math

from Modules.FS.FAT321612_read import FATReader
from Modules.FS.FAT3216_data import FATData
from Modules.FS.Interface_FS import IFSWork


class CommandFAT3216(IFSWork):
    """
    Класс отвечает за операции с файловой системой,
        в данный момент реализованы операции:
        * Переемешения по директориям
        * Прочтения файла или директории как байтов

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **cd** - Метод ответственный за перемешение внутри каталогов,
            возврашает лист в стиле рут: [Имя, Аттрибут,
             Дата последней записи, Размер в байтах, 
             Номер первого кластера элемента, Длинное имя]
            , а так же ощибку в случае неудачи перемешения, 
            при удаче переменная ощибки == "".
        **read** - Метод ответственный за чтение элемента, возврашает
            прочитаный кластер, как строка, форматирование это ваша забота,
            длинна прочитанного кластера равно длинне кластера * 2,
            при ощибке возврашается "", кластерную цепь,
            с удаленным прочитанным кластером, ощибку, 
            при удаче переменная ощибки == "".

    Аттрибуты:
    ~~~~~~~~~~~~~~~~~~
        **pwd**: str - Текушая дирректория
        **root**: list - Корневой каталог
    """

    pwd = "/"
    root = []
    _reader = object

    def __init__(self, mount):
        data = FATData()
        self._reader = FATReader(data, mount)
        root, error = self._reader.root_catalog_read()
        self.root = root

    def cd(self, dir_now: str, num_in_dir: int) -> [list, int]:
        root_claster = 0
        error = 0

        try:
            element = dir_now[num_in_dir]
            element_attr = element[1]
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return dir_now, error

        if element_attr == "20":
            error = 1
            return dir_now, error
        elif element_attr == "10":
            num_first_claster = element[4]

            if num_first_claster == root_claster:
                return copy.deepcopy(self.root), error
            else:
                claster_sequence, error = self._reader.build_cls_sequence(num_first_claster)

            if error == 0:
                error = 0
                self.pwd = element[0]
                elements_on_dir = self._reader.reder_directory(claster_sequence)
                return elements_on_dir, error
            else:
                error = 1
                return dir_now, error
        
        else:
            error = 2
            return dir_now, error

    def read(self, dir_now: list, num_in_dir: int, count: int, pointer: int) -> [str, list, str]:
        all_byte_elements = ""
        count_s = 0

        try:
            element = dir_now[num_in_dir]
            num_first_claster = element[4]
        except LookupError:
            error = -1
            logging.error(f"No mixing is possible. Element on dir: {len(dir_now)}, required item: {num_in_dir}")
            return "", 0, error

        claster_sequence, error = self._reader.build_cls_sequence(num_first_claster)
        if count < 0:
            count_s = copy.deepcopy(count)
            pointer += count_s
            count = int(math.fabs(count))

        if error == 0:
            for i in range(count):
                element_byte = self._reader.read_claster(claster_sequence, pointer)
                all_byte_elements += element_byte
                pointer += 1
            if count_s < 0:
                pointer += count_s
            return all_byte_elements, pointer, error
        else:
            error = "Ощибка при чтении элемента"
            return "", pointer, error

    def get_pwd(self) -> str:
        return self.pwd

    def get_root(self) -> list:
        return self.root
