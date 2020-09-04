from Modules.FS.FAT3216_data import FATData, FATLongName, FATDirectory


class FATReader:
    """
    Класс отвечает за прочтение файловых систем, предостовля доступ к ним.
        Поддерживаемые файловые системы: FAT32, FAT16.

    Методы:
        root_catalog_read - Читает рут каталог, используеться для получения
            доступа к остальным файлам и каталогам, возврашает
            лист папок и файлов которые в свою очередь тоже являються листом
            с содержимым: [Имя, Аттрибут, Дата создания,
             Размер в байтах, Номер первого кластера элемента, Длинное имя]
            Вызывать первым.
        read_claster - Метод который читает следующий в кластерной цепи
            кластер, удаляя прочитаный кластер из этой цепи.
        eof_point - Метод определяющий формат метки EOF используемой в
            fat таблицах файловых систем Fat16, Fat32
        build_cls_sequence - Метод создает кластерную цепь, возвращая
            лист последовательно идущих за собой кластеров
        mixing - Находит смешение до корневого каталога, первой и второй
            таблиц фат, важно упомянуть что он не способен искать смешение
            остальных таблиц даже если они существуют, а так же кол-во байт
            в секторе и секторов в кластере, размер fat таблиц, версию фс
        load_sector - Метод работает с первыми 512 байтами загрузочного
            сектора, определяя их, ФС, другие необходимые константы
        dir_element - Метод работает с элементами каталога возврашая
            все необходимые для работы с ними константы одним листом со
            структурой:
            [Имя, Аттрибут, Время последнего доступа,
             Размер, Номер первого кластера, Длинное имя]
        element_long_name -  Метод работает с длинными именами возврашая
            все необходимые для работы с ними константы одним листом со
            структурой:
            [Определитель(ord), Имя]
        file_sistem_check - Данный метод является статическим,
            но его документация необходима для правильного понимания работы
            и отлова ощибок на ваших образах.
            Метод высчитывает колличество класстеров в области данных ФС
            на основании этого делает ПРЕДПОЛОЖЕНИЕ о ФС образа если:
            count_of_clusters <= 4085 то FAT12
            4085 <= count_of_clusters <= 65525 то FAT16
            65525 <= count_of_clusters то FAT32
        parser_directory - Метод который разбирает каталог как директорию
            возврашает лист из листов с содержимым:
             [Имя, Аттрибут, Дата последней записи, Размер в байтах,
             Номер первого кластера элемента, Длинное имя]
        read_root_claster_fat16 - Метод читающий рут каталог ФС FAT16
            возвращает лист из листов с содержимым: [Имя, Аттрибут,
             Дата последней записи, Размер в байтах,
             Номер первого кластера элемента, Длинное имя]
        reder_directory - Метод преднозначен для формирования директорий по
            их кластерным цепям, возвращает лист из листов с содержимым:
             [Имя, Аттрибут, Дата последней записи, Размер в байтах,
             Номер первого кластера элемента, Длинное имя]

    Аттрибуты:
        seek_fs - Начало файловой системы, измините в случае
            если ваша фс начинаеться не с 0 байта файла.
        fat_seek_b - Начало фат таблицы
        fs - тип ФС
        bpb_byte_in_sector - Колличество байт в секторе
        bpb_sector_in_claster - Колличество секторов в кластере может быть
            равно степеням 2 (2, 4, 8, 16, 32, 64, 128, 256)
        root_dir_seek_b - смешение до корневого карталога
        bpb_root_ent_cnt - Колличество 32 байтных записей в корневом каталоге
            fat16
    """

    __seek_fs = 0  # 4128768
    fat_seek_b = 0
    fs = ""
    root_dir_seek_b = 0
    data: FATData
    mount_file_sys = 0

    def __init__(self, data: FATData, mount_file_sys):
        self.data = data
        self.mount_file_sys = mount_file_sys

    def set_seek_fs(self, seek_fs: int):
        self.__seek_fs = seek_fs

    # Читает корень диска.
    def root_catalog_read(self) -> [list, int]:
        root_catalog = []
        error = 0

        self.mixing()
        element_claster = "02"

        if self.data.FAT_version == "FAT32":
            claster_sequence, error = self.build_cls_sequence(element_claster)
            if error == 0:
                root_catalog = self.reder_directory(claster_sequence)
        elif self.data.FAT_version == "FAT16":
            root_catalog = self.read_root_claster_fat16()

        return root_catalog, error

    # Собирает корень диска ФС FAT16
    def read_root_claster_fat16(self) -> list:
        inc = 0
        len_one_record = 32
        root_catalog_FAT16 = []
        one_record = "ff"

        self.mount_file_sys.seek(self.root_dir_seek_b + self.__seek_fs)

        while self.data.bpb_root_ent_cnt != inc and one_record[0:2] != "00":
            one_record = self.mount_file_sys.read(len_one_record)
            one_record = one_record.hex()
            root_element = self.parser_directory(one_record)
            root_catalog_FAT16 += root_element
            inc += 1

        return root_catalog_FAT16

    # Читает директорию как директорию
    def reder_directory(self, claster_sequence: list) -> list:
        # claster = " "
        catalog = []
        pos = 0

        while len(claster_sequence) != pos:
            claster = self.read_claster(claster_sequence, pos).hex()
            claster = self.parser_directory(claster)
            catalog += claster
            pos += 1

        return catalog

    # Читает кластре как дирректорию
    def parser_directory(self, claster) -> list:
        element_ord = "01"
        attr_dir = "10"  # Дирректория
        attr_hidden = "02"  # Скрыто
        # attr_system = "04"  # Системный
        # attr_volume_id = "08"  # Том диска
        attr_long_name = "0f"  # Длинное имя
        # В документации такой штуки нет, но опытным путем это файл
        attr_file = "20"
        attr_info = "16"

        ord_is_defect = "e5"
        name_full = ""
        elements_on_dir = []

        while element_ord != "":
            element = claster[0:64]
            claster = claster[64:]
            element_ord = element[0:2]

            if element_ord == ord_is_defect:
                continue

            element_attr = element[22:24]

            if element_attr == attr_long_name:
                lond_name = FATLongName()
                self.element_long_name(element, lond_name)
                name_full += lond_name.l_element_name
            elif element_attr == attr_dir\
                    or element_attr == attr_file\
                    or element_attr == attr_info:
                directory = FATDirectory()
                element_d = self.dir_element(element, directory)
                element_d.append(name_full)
                elements_on_dir.append(element_d)
                name_full = ""
            elif element_attr == attr_hidden:
                continue
            else:
                continue

        return elements_on_dir

    # Читает любой элемент как строку байт.
    def read_claster(self, claster_sequence: list, pos: int) -> bytes:
        element_claster = claster_sequence[pos]
        # element_claster = claster_sequence.pop(0)
        first_sector = self.root_dir_seek_b // self.data.bpb_byte_in_sector

        claster_seek = 0

        if self.data.FAT_version == "FAT32":
            claster_seek = ((element_claster - 2)
                            * self.data.bpb_sector_in_claster) + first_sector
        elif self.data.FAT_version == "FAT16":
            root_end_sector = (self.data.bpb_root_ent_cnt * 32
                               // self.data.bpb_byte_in_sector) + first_sector
            e_len = ((element_claster - 2) * self.data.bpb_sector_in_claster)
            claster_seek = e_len + root_end_sector

        claster_seek = claster_seek * self.data.bpb_byte_in_sector

        self.mount_file_sys.seek(claster_seek + self.__seek_fs)
        claster = self.mount_file_sys.read(self.data.bpb_byte_in_sector
                                           * self.data.bpb_sector_in_claster)
        # claster = claster.hex()

        return claster

    # Определяет формат метки EOF
    def _eof_point(self, len_fat_record: int) -> int:
        self.mount_file_sys.seek(self.fat_seek_b
                                 + len_fat_record
                                 + self.__seek_fs)

        record_last = self.mount_file_sys.read(len_fat_record)
        record_last = record_last.hex()
        record_last = self.reversed_byte_ararry(record_last)
        record_last = int(str(record_last), 16)
        record_last = \
            record_last & ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)

        return record_last

    # Строит цепь кластеров
    def build_cls_sequence(self, element_claster: str) -> [list, int]:
        len_fat_record = 0

        record_next = 0  # Максимальное значение следующей записи
        record_error = 0
        record_empty = 0

        error = 0
        claster_sequence = []

        if self.data.FAT_version == "FAT16":
            len_fat_record = self.data.FAT16_LEN_RECORD
            record_next = 0x0fff8
            record_error = 0xfff7
        elif self.data.FAT_version == "FAT32":
            len_fat_record = self.data.FAT32_LEN_RECORD
            record_next = 0x0ffffff8
            record_error = 0x0ffffff7

        record_last = self._eof_point(len_fat_record)

        element_claster = int(str(element_claster), 10)
        element_claster = \
            element_claster & ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)
        claster_sequence.append(element_claster)

        while True:
            self.mount_file_sys.seek(self.fat_seek_b
                                     + (element_claster * len_fat_record)
                                     + self.__seek_fs)
            element_claster = self.mount_file_sys.read(len_fat_record)
            element_claster = str(element_claster.hex())
            element_claster = self.reversed_byte_ararry(element_claster)
            element_claster = int(str(element_claster), 16)
            element_claster = \
                element_claster &\
                ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)

            if element_claster == record_last \
                    or element_claster == record_empty:
                break
            elif element_claster == record_error:
                error = 1  # Файл поврежден
                break
            elif element_claster >= record_next:
                error = 2  # Файл слишком большой
                break
            else:
                claster_sequence.append(element_claster)

        return claster_sequence, error

    # Вычисляет смешение корневого каталога относительно начала образа
    # А так же смешение фат таблиц
    def mixing(self):
        root_dir_seek = 0
        load_sector_size = 512

        self.mount_file_sys.seek(self.__seek_fs)
        load_sector_b = self.mount_file_sys.read(load_sector_size)
        load_sector_h = load_sector_b.hex()

        self.load_sector(load_sector_h)
        all_fat_size, root_dir_sector = self.file_sistem_check()

        if self.data.FAT_version == "FAT32":
            self.loaded_fat32(load_sector_h)
        else:
            self.loaded_fat16(load_sector_h)
            # not_bpb_root_claster = 0

        if self.data.FAT_version == "FAT32":
            root_dir_seek = self.data.bpb_reversed_sector\
                            + all_fat_size\
                            + root_dir_sector
        elif self.data.FAT_version == "FAT16":
            root_dir_seek = self.data.bpb_reversed_sector\
                            + all_fat_size

        self.root_dir_seek_b = root_dir_seek * self.data.bpb_byte_in_sector
        self.fat_seek_b = self.data.bpb_reversed_sector\
                          * self.data.bpb_byte_in_sector

    # Разворот необходим для байт строк состояших из более чем 1 байта
    # Разворачивает шеснадцатиричную строку байтов для верной интерпритации
    @staticmethod
    def reversed_byte_ararry(bytes: str) -> str:
        i = 0
        j = 2
        inc = 0
        list_bytes = []

        while (len(bytes) / 2) != inc:
            one_byte = bytes[i:j]
            list_bytes.append(one_byte)
            i += 2
            j += 2
            inc += 1
        bytes = ""

        while len(list_bytes) != 0:
            one_byte = list_bytes.pop()
            bytes += one_byte

        return bytes

    # Да он собирает аски имя(
    @staticmethod
    def name_to_ascii(name_h: str) -> str:
        i = 0
        j = 2
        name = ""

        while len(name_h) != 0:
            name += chr(int(name_h[i:j], 16))
            name_h = name_h[j:]

        return name

    # !!!Последующие коментарии относяться только с строчке под ними!!!
    # Разбирает длинное имя каталога
    def element_long_name(self, element_h: str, long_name: FATLongName):
        long_name.l_element_ord = element_h[0:2]
        long_name.l_element_name_1 = element_h[2:22]
        long_name.l_element_name_2 = element_h[28:52]
        long_name.l_element_name_3 = element_h[56:64]

        long_name.l_element_name = str(long_name.l_element_name_1
                                       + long_name.l_element_name_2
                                       + long_name.l_element_name_3)
        long_name.l_element_name = self.name_to_ascii(long_name.l_element_name)

    # Разбирает обычный элемент каталога
    def dir_element(self, element_h: str, directory: FATDirectory) -> list:
        directory.element_name = self.name_to_ascii(element_h[0:22])
        directory.element_attr = element_h[22:24]
        directory.element_ctr_data = self.reversed_byte_ararry(
            element_h[32:36])
        directory.element_fst_claster_hi = self.reversed_byte_ararry(
            element_h[40:44])
        directory.element_fst_claster_lo = self.reversed_byte_ararry(
            element_h[52:56])
        directory.element_size = int(str(self.reversed_byte_ararry(
            element_h[56:64])), 16)

        directory.element_fst_claster = \
            int(str(directory.element_fst_claster_hi)
                + str(directory.element_fst_claster_lo), 16)

        element = [directory.element_name,
                   directory.element_attr,
                   directory.element_ctr_data,
                   directory.element_size,
                   directory.element_fst_claster]
        return element

    # Разбирает загрузочный сектор ФС
    def load_sector(self, load_sector_h: str):
        self.data.bpb_byte_in_sector = int(str(self.reversed_byte_ararry(
            load_sector_h[22:26])), 16)
        self.data.bpb_sector_in_claster = int(str(load_sector_h[26:28]), 16)
        self.data.bpb_reversed_sector = int(str(self.reversed_byte_ararry(
            load_sector_h[28:32])), 16)
        self.data.bpb_num_fat = int(str(load_sector_h[32:34]), 16)
        self.data.bpb_root_ent_cnt = int(str(self.reversed_byte_ararry(
            load_sector_h[34:38])), 16)
        self.data.bpb_total_sector_16_12 = int(str(self.reversed_byte_ararry(
            load_sector_h[38:42])), 16)
        self.data.bpb_fat_size_16_12 = int(str(self.reversed_byte_ararry(
            load_sector_h[44:48])), 16)
        self.data.bpb_total_sector_32 = int(str(self.reversed_byte_ararry(
            load_sector_h[64:72])), 16)
        self.data.bpb_fat_size_32 = int(str(self.reversed_byte_ararry(
            load_sector_h[72:80])), 16)
        # bpb_sector_in_claster = 2 ** bpb_sector_in_claster

    def loaded_fat16(self, load_sector_h: str):
        pass

    def loaded_fat32(self, load_sector_h: str):
        self.data.bpb_root_claster = int(str(self.reversed_byte_ararry(
            load_sector_h[88:96])), 16)  # Было 10 а не 16

    # Вычисляет версию file system FAT, и размер всех фат таблиц.
    def file_sistem_check(self) -> [int, int]:

        count_of_clusters_fat_12 = 4085
        count_of_clusters_fat_16 = 65525

        root_dir_sector = (((self.data.bpb_root_ent_cnt * 32)
                            + (self.data.bpb_byte_in_sector - 1))
                           // self.data.bpb_byte_in_sector)

        if self.data.bpb_fat_size_16_12 != 0:
            fat_size = self.data.bpb_fat_size_16_12
        else:
            fat_size = self.data.bpb_fat_size_32

        if self.data.bpb_total_sector_16_12 != 0:
            total_sector = self.data.bpb_total_sector_16_12
        else:
            total_sector = self.data.bpb_total_sector_32

        all_fat_size = self.data.bpb_num_fat * fat_size
        data_sector = total_sector - (self.data.bpb_reversed_sector
                                      + all_fat_size
                                      + root_dir_sector)
        count_of_clusters = data_sector // self.data.bpb_sector_in_claster

        if count_of_clusters < count_of_clusters_fat_12:
            self.data.FAT_version = "FAT12"
        elif count_of_clusters < count_of_clusters_fat_16:
            self.data.FAT_version = "FAT16"
        else:
            self.data.FAT_version = "FAT32"

        return all_fat_size, root_dir_sector
