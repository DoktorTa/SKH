import logging
import math

from Modules.FS.EXT2_data import EXT2Data, EXT2DescriptorGroup, EXT2Inode


class EXT2Reader:
    error = ""

    def __init__(self, data: EXT2Data, file):
        self.file = file
        self.data = data

    def root_catalog_read(self):
        self.superblockc_read(self.data)
        self._table_descriptor_block(self.data)

        root_num_descriptor = 2
        blocks_root = self.inode(root_num_descriptor)
        self.file.seek(int(blocks_root[0], 16) * 1024)
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
            inode_num = self.reversed_byte_ararry(block[0:8])
            if inode_num == "":
                break
            rec_len = self.reversed_byte_ararry(block[8:12])
            name_len = block[12:14]
            file_type = block[14:16]
            name = block[16:16 + 2 * int(name_len, 16)]
            block = block[0 + 2 * int(rec_len, 16):]
            element_block = [inode_num, rec_len, name_len, file_type, self.name_to_ascii(name)]
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

    def _table_descriptor_block(self, data: EXT2Data):
        block_size = 32
        data.block_size = 1024 << int(data.s_log_block_size)
        data.group_count = math.ceil(int(data.s_blocks_count, 16) / int(data.s_blocks_per_group, 16))
        seek_descriptor = (int(data.s_first_data_block, 16) + 1) * data.block_size
        for i in range(data.group_count):
            self.file.seek(seek_descriptor + i * block_size)
            buf = self.file.read(block_size).hex()

            descriptor_g = EXT2DescriptorGroup(i)
            self.table_descriptor_block_init(descriptor_g, buf)
            descriptor_g.start_seek = int(data.s_first_data_block, 16) + i * int(data.s_blocks_per_group, 16)
            descriptor_g.end_seek = descriptor_g.start_seek + int(data.s_blocks_per_group, 16)
            data.group_description_table.append(descriptor_g)

            # logging.debug(f"Descriptor: {str(descriptor_g)}")

    def inode(self, inodes_num: int) -> list:
        """
            Функция обрабатывает инод с помошью его номера, и выдает лист его кластеров, или по другому блоков.
        """

        block_group = (inodes_num - 1) / int(self.data.s_inodes_per_group, 16)

        group_index = (inodes_num - 1) % int(self.data.s_inodes_per_group, 16)
        block_disc = self.data.group_description_table[(inodes_num - 1) // int(self.data.s_inodes_per_group, 16)]
        offset = int(block_disc.bg_inode_table, 16) * self.data.block_size
        offset += group_index * int(self.data.s_inode_size, 16)

        logging.debug(f"Inode num: {inodes_num}, "
                      f"Offset inode: {offset}, "
                      f"Group index: {group_index}, "
                      f"Descriptor block: {block_disc.num_descriptor}")

        self.file.seek(offset)
        inode_block = self.file.read(int(self.data.s_inode_size, 16)).hex()

        inode = EXT2Inode()
        inode = self._inode_init(inode, inode_block)

        block_list = self._read_straight_blocks(inode)
        return block_list

    def _list_of_double_indirects(self, block: str) -> list:
        blocks = []

        for i in range(self.data.block_size / self.data.SIZE_BLOCK_IN_BLOCK_TABLE):
            aggregate_element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]), 16)

            if aggregate_element_block is 0:
                return blocks

            ib = self.read_block(aggregate_element_block).hex()
            blocks += self._list_of_indirects(ib)

        return blocks

    def _list_of_indirects(self, block: str) -> list:
        blocks = []

        for i in range(self.data.block_size / self.data.SIZE_BLOCK_IN_BLOCK_TABLE):
            element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]), 16)

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

        if int(inode.i_block[inode.FIRST_SINGLE_INDIRECT_BLOCK], 16) != 0:
            blocks = self._check_first_indirect_block(inode, blocks)

        return blocks

    def _check_first_indirect_block(self, inode: EXT2Inode, blocks: list) -> list:
        block_num = int(inode.i_block[inode.FIRST_SINGLE_INDIRECT_BLOCK], 16)
        i1b = self.read_block(block_num).hex()
        blocks += self._list_of_indirects(i1b)

        if int(inode.i_block[inode.FIRST_DOUBLE_INDIRECT_BLOCK]) != 0:
            blocks = self._check_double_indirect_block(inode, blocks)
        return blocks

    def _check_double_indirect_block(self, inode: EXT2Inode, blocks: list) -> list:
        """
            Из документации EXT2.
            14-я запись в массиве является номером блока первого дважды косвенного блока
            который является блоком, содержащим массив идентификаторов косвенных блоков,
            причем каждый из этих косвенных блоков содержит массив блоков, содержащих данные.
        """
        three_block = int(inode.i_block[inode.FIRST_DOUBLE_INDIRECT_BLOCK], 16)
        i2b = self.read_block(three_block).hex()
        blocks += self._list_of_double_indirects(i2b)

        if int(inode.i_block[inode.FIRST_TRIPLE_INDIRECT_BLOCK]) != 0:
            blocks += self._check_triple_indirect_block(inode, blocks)
        return blocks

    def _check_triple_indirect_block(self, inode: EXT2Inode, blocks: list) -> list:
        """
            Из документации EXT2.
            15-я запись в массиве является номером блока с тройным непрямым блоком;
            который является блоком, содержащим массив дважды косвенных идентификаторов блоков,
            причем каждый из этих дважды косвенных блоков содержит массив косвенных блоков,
            а каждый из этих косвенных блоков содержит массив прямых блоков.
            В файловой системе объемом 1 КБ это будет в общей сложности 16777216 блоков на блок с тройной непрямой связью.
        """
        i3b_num = int(inode.i_block[inode.FIRST_TRIPLE_INDIRECT_BLOCK])
        block = self.read_block(i3b_num).hex()
        for i in range(self.data.block_size / 4):
            element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]))
            if element_block is 0:
                return blocks
            dib = self.read_block(element_block).hex()
            blocks += self._list_of_double_indirects(dib)
        return blocks

    def superblockc_read(self, data: EXT2Data):
        self.file.seek(1024)
        superblock = self.file.read(1024).hex()
        self.super_block_initilaiz(data, superblock)
        if data.s_magic != "ef53":
            self.error = "Файловая система не является EXT2"
            exit()

        logging.debug(f"Magic: {data.s_magic}, State: {data.s_state}, Error: {data.s_errors}")

    # # Функция получения содержимого inode по его номеру
    # def _get_inode(self, data: EXT2Data, inode_num: int):
    #     # Вычисляем номер группы блоков, в которой находится inode с порядковым номером inode_num:
    #     group = (inode_num - 1) / int(data.s_inodes_per_group, 16)
    #     index = (inode_num - 1) % int(data.s_inodes_per_group, 16)
    #     containing_block = (index * int(data.s_inode_size, 16)) // data.block_size
    #     # pos = ((__u64)da.bg_inode_table) * data.block_size + (index * int(data.s_inode_size, 16))
    #     logging.debug(f"Num inode: {inode_num}, Her group: {group}, Index: {index}, Containing block {containing_block}")

    def _inode_init(self, inode: EXT2Inode, inode_byte: str):
        inode.i_mode = self.reversed_byte_ararry(inode_byte[0:4])  # 0	    2
        inode.i_uid = self.reversed_byte_ararry(inode_byte[4:8])  # 2	    2
        inode.i_size = self.reversed_byte_ararry(inode_byte[8:16])  # 4	    4
        inode.i_gid = self.reversed_byte_ararry(inode_byte[48:52])  # 24	    2
        inode.i_links_count = self.reversed_byte_ararry(inode_byte[52:56])  # 26	    2
        inode.i_flags = self.reversed_byte_ararry(inode_byte[64:70])  # 32	    4
        for i in range(15):
            inode.i_block.append(self.reversed_byte_ararry(inode_byte[80 + i * 8:88 + i * 8]))  # 40	    15 х 4
        return inode

    def table_descriptor_block_init(self, descriptor_g: EXT2DescriptorGroup, table_descriptor: str):
        descriptor_g.bg_block_bitmap = self.reversed_byte_ararry(table_descriptor[0:8])  # 0   4
        descriptor_g.bg_inode_bitmap = self.reversed_byte_ararry(table_descriptor[8:16])  # 4   4
        descriptor_g.bg_inode_table = self.reversed_byte_ararry(table_descriptor[16:24])  # 8   4

    def super_block_initilaiz(self, data: EXT2Data, superblock: str):
        #  Это значение должно быть меньше или равно (s_blocks_per_group * количество групп блоков)
        data.s_inodes_count = self.reversed_byte_ararry(superblock[0:8])  # 0   4
        data.s_blocks_count = self.reversed_byte_ararry(superblock[8:16])  # 4   4

        data.s_free_blocks_count = self.reversed_byte_ararry(superblock[24:32])  # 12  4
        data.s_free_inodes_count = self.reversed_byte_ararry(superblock[32:40])  # 16  4

        # Это значение всегда равно 0 для фс с размером блока более 1 КБ и всегда 1 для фс с размером блока 1 КБ.
        data.s_first_data_block = self.reversed_byte_ararry(superblock[40:48])  # 20  4

        data.s_log_block_size = self.reversed_byte_ararry(superblock[48:56])  # 24  4
        data.s_blocks_per_group = self.reversed_byte_ararry(superblock[64:72])  # 32  4
        data.s_inodes_per_group = self.reversed_byte_ararry(superblock[80:88])  # 40  4

        data.s_magic = self.reversed_byte_ararry(superblock[112:116])  # 56  2
        data.s_state = self.reversed_byte_ararry(superblock[116:120])  # 58  2
        data.s_errors =self.reversed_byte_ararry(superblock[120:124])  # 60  2

        data.s_first_ino = self.reversed_byte_ararry(superblock[168:176])  # 84  4
        data.s_inode_size = self.reversed_byte_ararry(superblock[176:180])  # 88  2

    # Это нужно уже заменить
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    data = EXT2Data()
    p = EXT2Reader(data)
