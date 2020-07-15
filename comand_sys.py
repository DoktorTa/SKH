import copy
from FAT321612_read import Reader


class Command:
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
        self._reader = Reader()
        root, error = self._reader.root_catalog_read(mount)
        self.root = root

    def cd(self, mount_file_sys, dir_now: list, num: int) -> [list, str]:
        root_claster = 0
        error = ""
        element = dir_now[num]
        element_attr = element[1]

        if element_attr == "20":
            error = "Элемент являеться файлом, а не директорией"
            return dir_now, error
        elif element_attr == "10":
            num_first_claster = element[4]

            if num_first_claster == root_claster:
                return copy.deepcopy(self.root), error
            else:
                claster_sequence, error = self._reader.build_cls_sequence(mount_file_sys, num_first_claster)

            if error == 0:
                error = ""
                self.pwd = element[0]
                elements_on_dir = self._reader.reder_directory(mount_file_sys, claster_sequence)
                return elements_on_dir, error
            else:
                error = "Ощибка при чтении директроии"
                return dir_now, error
        
        else:
            error = "Работа с этими элементами католога невозможна в данной версии программы"
            return dir_now, error

    def read(self, mount_file_sys, dir_now: list, num: int) -> [str, list, str]:
        element = dir_now[num]
        num_first_claster = element[4]
        claster_sequence, error = self._reader.build_cls_sequence(mount_file_sys, num_first_claster)

        if error == 0:
            error = ""
            element_byte, claster_sequence = self._reader.read_claster(mount_file_sys, claster_sequence)
            return element_byte, claster_sequence, error
        else:
            error = "Ощибка при чтении элемента"
            return "", claster_sequence, error


if __name__ == '__main__':

    way = r"A:\Programming languages\In developing\Python\FAT 32\test16.img"
    mount = open(way, "rb")
    c = Command(mount)
    #print(c.root)
     # x, e, r = c.read(mount, c.root, 0)
    # print(len(x))
    # print(x)
    x, e = c.cd(mount, c.root, 0)
    print(c.pwd, e)
    # z, e = c.cd(mount, x, 4)
    # print(z, e)
    mount.close()
