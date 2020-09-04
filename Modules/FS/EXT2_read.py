import logging
import math

from Modules.FS.EXT2_data import EXT2Data, EXT2DescriptorGroup, EXT2Inode


class EXT2Reader:
    error = ""
    data: EXT2Data

    def __init__(self, data: EXT2Data, file):
        self.file = file
        self.data = data

    def root_catalog_read(self) -> list:
        self.superblock_read()
        self._table_descriptor_block()

        blocks_root = self.inode(self.data.EXT2_ROOT_DESCRIPTOR)

        self.file.seek(blocks_root[0] * 1024)
        block_root = self.file.read(self.data.block_size).hex()
        root = self.linked_directory_entry(block_root)

        logging.debug(f"Root: {root},\nBlocks root: {blocks_root}")
        logging.debug(str(self.data))
        return root

    def linked_directory_entry(self, block: str) -> list:
        """
            [inode_num, rec_len, name_len, file_type, name_ascii]
        """
        dir_entry = []
        while True:
            inode_num = self._reversed_byte_ararry(block[0:8])
            if inode_num == "":
                break
            rec_len = self._reversed_byte_ararry(block[8:12])
            name_len = block[12:14]
            file_type = block[14:16]
            name = block[16:16 + 2 * int(name_len, 16)]
            block = block[0 + 2 * int(rec_len, 16):]
            element_block = [inode_num, rec_len, name_len, file_type,
                             self.name_to_ascii(name)]
            dir_entry.append(element_block)
        return dir_entry

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

    def _table_descriptor_block(self):
        """
            Функция читает и преобразует таблицу дискрипторов блоков,
             добовляя ее в EXT2Data
        """
        block_size = 32
        blocks_per_group = int(self.data.s_blocks_per_group, 16)
        first_data_block = int(self.data.s_first_data_block, 16)

        self.data.block_size = 1024 << int(self.data.s_log_block_size, 16)
        self.data.group_count = math.ceil(int(self.data.s_blocks_count, 16)
                                          / blocks_per_group)
        seek_descriptor = (first_data_block + 1) * self.data.block_size

        for i in range(self.data.group_count):
            self.file.seek(seek_descriptor + i * block_size)
            buf = self.file.read(block_size).hex()

            descriptor_g = EXT2DescriptorGroup(i)
            self._table_descriptor_block_init(descriptor_g, buf)

            descriptor_g.start_seek = first_data_block + i * blocks_per_group
            descriptor_g.end_seek = descriptor_g.start_seek + blocks_per_group
            self.data.group_description_table.append(descriptor_g)

    def inode(self, inodes_num: int) -> list:
        """
            Функция обрабатывает инод с помошью его номера,
             и выдает лист его кластеров, или по другому блоков.
        """
        inode_per_group = int(self.data.s_inodes_per_group, 16)
        inode_size = int(self.data.s_inode_size, 16)

        # block_group =(inodes_num - 1) / int(self.data.s_inodes_per_group, 16)
        group_index = (inodes_num - 1) % inode_per_group
        block_disc = self.data.group_description_table[(inodes_num - 1)
                                                       // inode_per_group]
        offset = int(block_disc.bg_inode_table, 16) * self.data.block_size
        offset += group_index * inode_size

        self.file.seek(offset)
        inode_block = self.file.read(inode_size).hex()

        logging.debug(f"Inode num: {inodes_num}, "
                      f"Offset inode: {offset}, "
                      f"Group index: {group_index}, "
                      f"Descriptor block: {block_disc.num_descriptor}")

        inode = EXT2Inode()
        inode = self._inode_init(inode, inode_block)

        block_list = self._read_straight_blocks(inode)

        return block_list

    def _list_of_double_indirects(self, block: str) -> list:
        """
            Читает блоки двойной вложености.
        """
        blocks = []

        for i in range(int(self.data.block_size
                           / self.data.SIZE_BLOCK_IN_BLOCK_TABLE)):
            aggregate_element_block = int(self._reversed_byte_ararry(
                block[0 + 8 * i:8 + 8 * i]), 16)

            if aggregate_element_block is 0:
                return blocks

            ib = self.read_block(aggregate_element_block).hex()
            blocks += self._list_of_indirects(ib)

        return blocks

    def _list_of_indirects(self, block: str) -> list:
        """
            Читает блоки из блока.
        """
        blocks = []

        for i in range(int(self.data.block_size
                           / self.data.SIZE_BLOCK_IN_BLOCK_TABLE)):
            element_block = int(self._reversed_byte_ararry(
                block[0 + 8 * i:8 + 8 * i]), 16)

            if element_block is 0:
                return blocks

            blocks.append(element_block)

        return blocks

    def read_block(self, block_num: int) -> bytes:
        """
            Читает определенный номер блока
        """
        self.file.seek(block_num * self.data.block_size)
        buf = self.file.read(self.data.block_size)
        return buf

    def _read_straight_blocks(self, inode: EXT2Inode) -> list:
        """
            Возврашает полный лист блоков инода
        """
        blocks = []

        for i in range(inode.FIRST_INDIRECT_BLOCK):
            straight_block = inode.i_block[i]

            if straight_block == 0:
                return blocks

            blocks.append(straight_block)

        if inode.i_block[inode.FIRST_SINGLE_INDIRECT_BLOCK - 1] != 0:
            blocks += self._check_first_indirect_block(inode, blocks)
        return blocks

    def _check_first_indirect_block(self, inode: EXT2Inode, blocks: list)\
            -> list:
        """
            Читает и разбирает первый блок ссылки, а так же проверяет второй
             блок ссылки.
        """
        block_num = inode.i_block[inode.FIRST_SINGLE_INDIRECT_BLOCK - 1]
        i1b = self.read_block(block_num).hex()
        blocks += self._list_of_indirects(i1b)

        if inode.i_block[inode.FIRST_DOUBLE_INDIRECT_BLOCK - 1] != 0:
            blocks += self._check_double_indirect_block(inode, blocks)
        return blocks

    def _check_double_indirect_block(self, inode: EXT2Inode, blocks: list)\
            -> list:
        """
            Читает и разбирает второй блок ссылки, а так же проверяет третий
             блок ссылки.

            Из документации EXT2.
            14-я запись в массиве является номером блока первого дважды
            косвенного блока который является блоком, содержащим массив
            идентификаторов косвенных блоков, причем каждый из этих косвенных
             блоков содержит массив блоков, содержащих данные.
        """
        three_block = inode.i_block[inode.FIRST_DOUBLE_INDIRECT_BLOCK - 1]
        i2b = self.read_block(three_block).hex()
        blocks += self._list_of_double_indirects(i2b)

        if inode.i_block[inode.FIRST_TRIPLE_INDIRECT_BLOCK - 1] != 0:
            blocks += self._check_triple_indirect_block(inode, blocks)
        return blocks

    def _check_triple_indirect_block(self, inode: EXT2Inode, blocks: list)\
            -> list:
        """
            Читает и разбирает третий блок ссылки.

            Из документации EXT2.
            15-я запись в массиве является номером блока с тройным непрямым
            блоком который является блоком, содержащим массив дважды косвенных
            идентификаторов блоков, причем каждый из этих дважды косвенных
            блоков содержит массив косвенных блоков, а каждый из этих косвенных
            блоков содержит массив прямых блоков.
            В файловой системе объемом 1 КБ это будет в общей сложности 16777216 блоков на блок с тройной непрямой связью.
        """
        i3b_num = inode.i_block[inode.FIRST_TRIPLE_INDIRECT_BLOCK - 1]
        block = self.read_block(i3b_num).hex()
        for i in range(self.data.block_size
                       / self.data.SIZE_BLOCK_IN_BLOCK_TABLE):
            element_block = int(self._reversed_byte_ararry(
                block[0 + 8 * i:8 + 8 * i]), 16)
            if element_block is 0:
                return blocks
            dib = self.read_block(element_block).hex()
            blocks += self._list_of_double_indirects(dib)
        return blocks

    def _superblock_check(self):
        """
            Выполняет проверку фс, магического числа, и возможность чтения
            модулем.
        """
        incompact = int(str(self.data.s_feature_incompat), 16)

        if self.data.s_magic != "ef53":
            self.error = 1
            logging.error(f"Файловая система не является EXT2, magic number: "
                          f"{self.data.s_magic}, default: ef53")
        elif incompact == self.data.EXT2_FEATURE_INCOMPAT_COMPRESSION \
                or incompact == self.data.EXT2_FEATURE_INCOMPAT_FILETYPE \
                or incompact == self.data.EXT3_FEATURE_INCOMPAT_RECOVER \
                or incompact == self.data.EXT3_FEATURE_INCOMPAT_JOURNAL_DEV \
                or incompact == self.data.EXT2_FEATURE_INCOMPAT_META_BG:
            self.error = 1
            logging.error(f"Не совметимые функции: {incompact}")

    def superblock_read(self):
        """
            Чиатет суперблок, подготавливая его для работы, проверяет фс на
            возможность чтения данный модулем.
        """
        load_block = 1024
        superblock_len = 1024

        self.file.seek(load_block)
        superblock = self.file.read(superblock_len).hex()
        self._superblock_init(superblock)
        self._superblock_check()

        logging.debug(f"Magic: {self.data.s_magic},"
                      f" State: {self.data.s_state},"
                      f" Error: {self.data.s_errors}")

    def _inode_init(self, inode: EXT2Inode, inode_byte: str) -> EXT2Inode:
        """
            Разбирает заптсь инода.
        """
        inode.i_mode = self._reversed_byte_ararry(inode_byte[0:4])  # 0	    2
        inode.i_uid = self._reversed_byte_ararry(inode_byte[4:8])  # 2	    2
        inode.i_size = self._reversed_byte_ararry(inode_byte[8:16])  # 4
        inode.i_gid = self._reversed_byte_ararry(inode_byte[48:52])  # 24
        inode.i_links_count = self._reversed_byte_ararry(inode_byte[52:56])
        inode.i_flags = self._reversed_byte_ararry(inode_byte[64:70])
        for i in range(15):
            inode.i_block.append(int(self._reversed_byte_ararry(
                inode_byte[80 + i * 8:88 + i * 8]), 16))
        return inode

    def _table_descriptor_block_init(self, descriptor_g: EXT2DescriptorGroup,
                                     table_descriptor: str):
        """
            Разбирает запись в таблице дискрипторов блоков.
        """
        descriptor_g.bg_block_bitmap = self._reversed_byte_ararry(
            table_descriptor[0:8])  # 0   4
        descriptor_g.bg_inode_bitmap = self._reversed_byte_ararry(
            table_descriptor[8:16])  # 4   4
        descriptor_g.bg_inode_table = self._reversed_byte_ararry(
            table_descriptor[16:24])  # 8   4

    def _superblock_init(self, superblock: str):
        """
            Разбирает супер блок.
        """
        #  Это значение должно быть меньше или равно
        #  (s_blocks_per_group * количество групп блоков)
        self.data.s_inodes_count = self._reversed_byte_ararry(superblock[0:8])
        self.data.s_blocks_count = self._reversed_byte_ararry(superblock[8:16])

        self.data.s_free_blocks_count = self._reversed_byte_ararry(
            superblock[24:32])  # 12  4
        self.data.s_free_inodes_count = self._reversed_byte_ararry(
            superblock[32:40])  # 16  4

        # Это значение всегда равно 0 для фс с размером блока более 1 КБ и
        # всегда 1 для фс с размером блока 1 КБ.
        self.data.s_first_data_block = self._reversed_byte_ararry(
            superblock[40:48])  # 20  4

        self.data.s_log_block_size = self._reversed_byte_ararry(
            superblock[48:56])  # 24  4
        self.data.s_blocks_per_group = self._reversed_byte_ararry(
            superblock[64:72])  # 32  4
        self.data.s_inodes_per_group = self._reversed_byte_ararry(
            superblock[80:88])  # 40  4
        self.data.s_magic = self._reversed_byte_ararry(
            superblock[112:116])  # 56  2
        self.data.s_state = self._reversed_byte_ararry(
            superblock[116:120])  # 58  2
        self.data.s_errors = self._reversed_byte_ararry(
            superblock[120:124])  # 60  2
        self.data.s_first_ino = self._reversed_byte_ararry(
            superblock[168:176])  # 84  4
        self.data.s_inode_size = self._reversed_byte_ararry(
            superblock[176:180])  # 88  2
        self.data.s_feature_incompat = self._reversed_byte_ararry(
            superblock[192:200])  # 96  4

    # Это нужно уже заменить
    @staticmethod
    def _reversed_byte_ararry(bytes: str) -> str:
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
