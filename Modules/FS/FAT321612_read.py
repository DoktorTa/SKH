class Reader:
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

    seek_fs = 0  # 4128768
    fat_seek_b = 0
    fs = ""
    bpb_byte_in_sector = 0
    bpb_sector_in_claster = 0
    root_dir_seek_b = 0
    bpb_root_ent_cnt = 0

    # Читает корень диска.
    def root_catalog_read(self, mount_file_sys) -> [list, int]:
        root_catalog = []
        error = 0

        self.mixing(mount_file_sys)
        element_claster = "02"

        if self.fs == "FAT32":
            claster_sequence, error = self.build_cls_sequence(mount_file_sys, element_claster)
            if error == 0:
                root_catalog = self.reder_directory(mount_file_sys, claster_sequence)
        elif self.fs == "FAT16":
            root_catalog = self.read_root_claster_fat16(mount_file_sys)

        return root_catalog, error

    # Собирает корень диска ФС FAT16
    def read_root_claster_fat16(self, mount_file_sys) -> list:
        inc = 0
        len_one_record = 32
        root_catalog_FAT16 = []
        one_record = "ff"

        mount_file_sys.seek(self.root_dir_seek_b + self.seek_fs)

        while self.bpb_root_ent_cnt != inc and one_record[0:2] != "00":
            one_record = mount_file_sys.read(len_one_record)
            one_record = one_record.hex()
            root_element = self.parser_directory(one_record)
            root_catalog_FAT16 += root_element
            inc += 1

        return root_catalog_FAT16

    # Читает директорию как директорию
    def reder_directory(self, mount_file_sys, claster_sequence: list) -> list:
        claster = " "
        catalog = []

        while len(claster) != 0 and len(claster_sequence) != 0:
            claster, claster_sequence = self.read_claster(mount_file_sys, claster_sequence)
            claster = self.parser_directory(claster)
            catalog += claster

        return catalog

    # Читает кластре как дирректорию
    def parser_directory(self, claster) -> list:
        element_ord = "01"
        attr_dir = "10"  # Дирректория
        attr_hidden = "02"  # Скрыто
        # attr_system = "04"  # Системный
        # attr_volume_id = "08"  # Том диска
        attr_long_name = "0f"  # Длинное имя
        attr_file = "20"  # В документации такой штуки нет, но опытным путем это файл
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
                element_l = self.element_long_name(element)
                name_full += element_l[1]
            elif element_attr == attr_dir or element_attr == attr_file or element_attr == attr_info:
                element_d = self.dir_element(element)
                element_d.append(name_full)
                elements_on_dir.append(element_d)
                name_full = ""
            elif element_attr == attr_hidden:
                continue
            else:
                continue

        return elements_on_dir

    # Читает любой элемент как строку байт.
    def read_claster(self, mount_file_sys, claster_sequence: list) -> [int, list]:
        element_claster = claster_sequence.pop(0)
        first_sector = self.root_dir_seek_b // self.bpb_byte_in_sector

        claster_seek = 0

        if self.fs == "FAT32":
            claster_seek = ((element_claster - 2) * self.bpb_sector_in_claster) + first_sector
        elif self.fs == "FAT16":
            root_end_sector = (self.bpb_root_ent_cnt * 32 // self.bpb_byte_in_sector) + first_sector
            claster_seek = ((element_claster - 2) * self.bpb_sector_in_claster) + root_end_sector

        claster_seek = claster_seek * self.bpb_byte_in_sector

        mount_file_sys.seek(claster_seek + self.seek_fs)
        claster = mount_file_sys.read(self.bpb_byte_in_sector * self.bpb_sector_in_claster)
        claster = claster.hex()

        return claster, claster_sequence

    # Определяет формат метки EOF
    def eof_point(self, mount_file_sys, len_fat_record: int) -> int:
        mount_file_sys.seek(self.fat_seek_b + len_fat_record + self.seek_fs)

        record_last = mount_file_sys.read(len_fat_record)
        record_last = record_last.hex()
        record_last = self.reversed_byte_ararry(record_last)
        record_last = int(str(record_last), 16)
        record_last = record_last & ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)

        return record_last

    # Строит цепь кластеров
    def build_cls_sequence(self, mount_file_sys, element_claster: str) -> [list, int]:
        len_fat_record = 0
        len_fat_16_record = 2
        len_fat_32_record = 4

        record_next = 0  # Максимальное значение следующей записи
        record_error = 0
        record_empty = 0

        error = 0
        claster_sequence = []

        if self.fs == "FAT16":
            len_fat_record = len_fat_16_record
            record_next = 0x0fff8
            record_error = 0xfff7
        elif self.fs == "FAT32":
            len_fat_record = len_fat_32_record
            record_next = 0x0ffffff8
            record_error = 0x0ffffff7

        record_last = self.eof_point(mount_file_sys, len_fat_record)

        element_claster = int(str(element_claster), 10)
        element_claster = element_claster & ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)
        claster_sequence.append(element_claster)

        while True:
            mount_file_sys.seek(self.fat_seek_b + (element_claster * len_fat_record) + self.seek_fs)
            element_claster = mount_file_sys.read(len_fat_record)
            element_claster = str(element_claster.hex())
            element_claster = self.reversed_byte_ararry(element_claster)
            element_claster = int(str(element_claster), 16)
            element_claster = element_claster & ~(1 << 28) & ~(1 << 29) & ~(1 << 30) & ~(1 << 31)

            if element_claster == record_last or element_claster == record_empty:
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
    def mixing(self, mount_file_sys):
        root_dir_seek = 0
        load_sector_size = 512

        mount_file_sys.seek(self.seek_fs)
        load_sector_b = mount_file_sys.read(load_sector_size)
        load_sector_h = load_sector_b.hex()

        all_fat_size, root_dir_sector, bpb_root_claster, bpb_reversed_sector, fat_size = self.load_sector(load_sector_h)

        if self.fs == "FAT32":
            root_dir_seek = bpb_reversed_sector + all_fat_size + root_dir_sector
        elif self.fs == "FAT16":
            root_dir_seek = bpb_reversed_sector + all_fat_size

        self.root_dir_seek_b = root_dir_seek * self.bpb_byte_in_sector
        self.fat_seek_b = bpb_reversed_sector * self.bpb_byte_in_sector
        # next_fat_seek_b = (bpb_reversed_sector + fat_size) * self.bpb_byte_in_sector

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
    def element_long_name(self, element_h: str) -> list:
        l_element_ord = element_h[0:2]
        l_element_name_1 = element_h[2:22]
        l_element_attr = element_h[22:24]
        l_element_type = element_h[24:26]
        l_element_chksum = element_h[26:28]
        l_element_name_2 = element_h[28:52]
        l_element_fts_claster_lo = element_h[52:56]
        l_element_name_3 = element_h[56:64]

        l_element_name = str(l_element_name_1 + l_element_name_2 + l_element_name_3)
        l_element_name = self.name_to_ascii(l_element_name)

        l_element = [l_element_ord, l_element_name]

        return l_element

    # Разбирает обычный элемент каталога
    def dir_element(self, element_h: str) -> list:
        element_name = element_h[0:22]
        element_attr = element_h[22:24]

        # Зарезервировано для использования Windows NT
        element_NT = element_h[24:26]
        element_ctr_time_tenth = element_h[26:28]
        element_ctr_time = element_h[28:32]
        element_ctr_data = element_h[32:36]
        element_lst_acc_date = element_h[36:40]
        element_fst_claster_hi = element_h[40:44]
        element_wrt_time = element_h[44:48]
        element_wrt_data = element_h[48:52]
        element_fst_claster_lo = element_h[52:56]
        element_size = element_h[56:64]

        element_ctr_data = self.reversed_byte_ararry(element_ctr_data)
        element_fst_claster_hi = self.reversed_byte_ararry(element_fst_claster_hi)
        element_fst_claster_lo = self.reversed_byte_ararry(element_fst_claster_lo)
        element_size = self.reversed_byte_ararry(element_size)

        element_name = self.name_to_ascii(element_name)

        element_fst_claster = str(element_fst_claster_hi) + str(element_fst_claster_lo)

        element_fst_claster = int(str(element_fst_claster), 16)
        element_size = int(str(element_size), 16)

        element = [element_name, element_attr, element_ctr_data, element_size, element_fst_claster]
        return element

    # Разбирает загрузочный сектор ФС
    def load_sector(self, load_sector_h: str) -> [int, int, int, int, int, int]:
        bpb_eb = load_sector_h[0:6]
        bpb_os_or_fs_identifier = load_sector_h[6:22]
        bpb_byte_in_sector = load_sector_h[22:26]

        # Это значение должно быть степенью 2, которая больше 0
        bpb_sector_in_claster = load_sector_h[26:28]

        # Для томов FAT12 и FAT16 это значение никогда не должно быть
        # ничем иным, чем 1. Для томов FAT32 это значение обычно равно 32.
        bpb_reversed_sector = load_sector_h[28:32]
        bpb_num_fat = load_sector_h[32:34]

        # Для томов FAT12 и FAT16 это значение всегда должно указывать счетчик,
        # который при умножении на 32 приводит к четному кратному
        # BPB_BytsPerSec. Для FAT32 поле всегда 0
        bpb_root_ent_cnt = load_sector_h[34:38]

        # Если это 0, то BPB_TotSec32 должен быть ненулевым.
        # Для томов FAT32 это поле должно быть 0.
        # Для томов FAT12 и FAT16 это поле содержит количество секторов,
        # а BPB_TotSec32 равно 0, если общее количество секторов меньше 0x10000
        bpb_total_sector_16_12 = load_sector_h[38:42]
        bpb_media = load_sector_h[42:44]

        # Это поле является 16-разрядным счетчиком FAT12 / FAT16 секторов,
        # занятых ONE FAT. На томах FAT32 это поле должно быть 0,
        # а BPB_FATSz32 содержит счетчик размеров FAT.
        bpb_fat_size_16_12 = load_sector_h[44:48]
        bpb_sector_on_track = load_sector_h[48:52]
        bpb_num_heads = load_sector_h[52:56]
        bpb_hidden_sector = load_sector_h[56:64]

        # 32-разрядное общее количество секторов в томе.
        # Это количество включает в себя количество всех секторов
        # во всех четырех областях тома. Если это 0, то BPB_TotSec16
        # должен быть ненулевым.
        # Для томов FAT32 это поле должно быть ненулевым.
        # Для томов FAT12 / FAT16 это поле содержит количество секторов,
        # если BPB_TotSec16 равно 0 (количество больше или равно 0x10000).
        bpb_total_sector_32 = load_sector_h[64:72]

        # Это поле является 32-битным счетчиком FAT32 секторов,
        # занятых ONE FAT.
        bpb_fat_size_32 = load_sector_h[72:80]

        bpb_root_ent_cnt = self.reversed_byte_ararry(bpb_root_ent_cnt)
        bpb_byte_in_sector = self.reversed_byte_ararry(bpb_byte_in_sector)
        bpb_fat_size_16_12 = self.reversed_byte_ararry(bpb_fat_size_16_12)
        bpb_fat_size_32 = self.reversed_byte_ararry(bpb_fat_size_32)
        bpb_total_sector_16_12 = self.reversed_byte_ararry(
            bpb_total_sector_16_12)
        bpb_total_sector_32 = self.reversed_byte_ararry(bpb_total_sector_32)
        bpb_reversed_sector = self.reversed_byte_ararry(bpb_reversed_sector)

        bpb_root_ent_cnt = int(str(bpb_root_ent_cnt), 16)
        bpb_byte_in_sector = int(str(bpb_byte_in_sector), 16)
        bpb_fat_size_16_12 = int(str(bpb_fat_size_16_12), 16)
        bpb_fat_size_32 = int(str(bpb_fat_size_32), 16)
        bpb_total_sector_16_12 = int(str(bpb_total_sector_16_12), 16)
        bpb_total_sector_32 = int(str(bpb_total_sector_32), 16)
        bpb_num_fat = int(str(bpb_num_fat), 16)
        bpb_reversed_sector = int(str(bpb_reversed_sector), 16)
        bpb_sector_in_claster = int(str(bpb_sector_in_claster), 16)

        # bpb_sector_in_claster = 2 ** bpb_sector_in_claster

        fs, all_fat_size, root_dir_sector = self.file_sistem_check(bpb_root_ent_cnt,
                                                                   bpb_byte_in_sector,
                                                                   bpb_fat_size_16_12,
                                                                   bpb_fat_size_32,
                                                                   bpb_total_sector_16_12,
                                                                   bpb_total_sector_32,
                                                                   bpb_num_fat,
                                                                   bpb_reversed_sector,
                                                                   bpb_sector_in_claster)

        self.fs = fs
        self.bpb_byte_in_sector = bpb_byte_in_sector
        self.bpb_sector_in_claster = bpb_sector_in_claster
        self.bpb_root_ent_cnt = bpb_root_ent_cnt

        if self.fs == "FAT32":
            bpb_root_claster = self.loaded_fat32(load_sector_h)

            return all_fat_size, root_dir_sector, bpb_root_claster, bpb_reversed_sector, bpb_fat_size_32
        else:
            self.loaded_fat16(load_sector_h)
            not_bpb_root_claster = 0

            return all_fat_size, root_dir_sector, not_bpb_root_claster, bpb_reversed_sector, bpb_fat_size_16_12

    def loaded_fat16(self, load_sector_h: str):
        bs_num_drv = load_sector_h[72:74]

        # Код, который форматирует тома FAT,
        # должен всегда устанавливать этот байт в 0.
        bs_reversed_1 = load_sector_h[74:76]

        # Указывает на наличие следующих трех полей в загрузочном секторе.
        bs_boot_signature = load_sector_h[76:78]
        bs_serian_num_tom = load_sector_h[78:86]
        bs_mets_tom = load_sector_h[86:108]

        # Этой Иуде неверит даже Microsoft
        bs_fs_t = load_sector_h[108:124]

    def loaded_fat32(self, load_sector_h: str) -> int:
        # Биты 0-3 - количество активных FAT на основе нуля.
        # Действителен только если зеркальное отображение отключено.
        # Биты 4-6 - зарезервированы.
        # Бит 7 - 0 означает, что FAT отражается во все FAT .
        # - 1 означает, что активен только один FAT это ссылка на биты 0-3.
        # Биты 8-15 - зарезервированы.
        bpb_ext_flags = load_sector_h[80:84]
        bpb_fs_ver = load_sector_h[84:88]

        # Это номер кластера первого кластера корневого каталога, обычно 2.
        bpb_root_claster = load_sector_h[88:96]

        # Номер сектора структуры FSINFO в зарезервированной области FAT32.
        bpb_fs_info = load_sector_h[96:100]

        # Если не ноль, указывает номер сектора в зарезервированной области
        # тома копии загрузочной записи.
        bpb_bk_boot_sector = load_sector_h[100:104]
        bpb_reversed = load_sector_h[104:128]

        # !!!Далее то же что и в FAT12 и FAT16, но с другим смешением!!!

        bs_num_drv = load_sector_h[128:130]

        # Код, который форматирует тома FAT,
        # должен всегда устанавливать этот байт в 0.
        bs_reversed_1 = load_sector_h[130:132]

        # Указывает на наличие следующих трех полей в загрузочном секторе.
        bs_boot_signature = load_sector_h[132:134]
        bs_serian_num_tom = load_sector_h[134:142]
        bs_mets_tom = load_sector_h[142:164]

        # Этой Иуде неверит даже Microsoft
        bs_fs_t = load_sector_h[164:180]

        bpb_root_claster = self.reversed_byte_ararry(bpb_root_claster)
        bpb_root_claster = int(str(bpb_root_claster), 10)

        return bpb_root_claster

    # Вычисляет версию file system FAT, и размер всех фат таблиц.
    @staticmethod
    def file_sistem_check(bpb_root_ent_cnt, bpb_byte_in_sector,
                          bpb_fat_size_16_12,  bpb_fat_size_32,
                          bpb_total_sector_16_12, bpb_total_sector_32,
                          bpb_num_fat, bpb_reversed_sector,
                          bpb_sector_in_claster) -> [str, int, int]:

        count_of_clusters_fat_12 = 4085
        count_of_clusters_fat_16 = 65525

        root_dir_sector = (((bpb_root_ent_cnt * 32) + (bpb_byte_in_sector - 1)) // bpb_byte_in_sector)

        if bpb_fat_size_16_12 != 0:
            fat_size = bpb_fat_size_16_12
        else:
            fat_size = bpb_fat_size_32

        if bpb_total_sector_16_12 != 0:
            total_sector = bpb_total_sector_16_12
        else:
            total_sector = bpb_total_sector_32

        all_fat_size = bpb_num_fat * fat_size
        data_sector = total_sector - (bpb_reversed_sector + all_fat_size + root_dir_sector)
        count_of_clusters = data_sector // bpb_sector_in_claster

        if count_of_clusters < count_of_clusters_fat_12:
            fs = "FAT12"
        elif count_of_clusters < count_of_clusters_fat_16:
            fs = "FAT16"
        else:
            fs = "FAT32"

        return fs, all_fat_size, root_dir_sector

'''
if __name__ == '__main__':
    way = r"A:\Programming languages\In developing\Python\FAT 32\test16.img"
    mount = open(way, "rb")
    r = Reader()
    r.root_catalog_read(mount)
    mount.close()

    """print(fs)
        print("bpb_reversed_sector: {}".format(bpb_reversed_sector))
        print("total_sector: {}  |bpb_total_sector_16_12: {}".format(total_sector, bpb_total_sector_16_12))
        print("data_sector: {}".format(data_sector))
        print("count_of_clusters: {}".format(count_of_clusters))
        print("bpb_root_ent_cnt: {}".format(bpb_root_ent_cnt))
        print("root_dir_sector: {}".format(root_dir_sector))
        print("all_fat_size: {}  |fat_size: {}  |bpb_fat_size_16_12: {}".format(all_fat_size, fat_size, bpb_fat_size_16_12))
        
        setor_of_claster = ((N - 2) * bpb_sector_in_claster) + first_data_sector
    """
'''
