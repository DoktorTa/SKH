import logging
import math

from Modules.FS.EXT2_data import EXT2Data, EXT2DescriptorGroup, EXT2Inode


class EXT2Reader:
    error = ""

    def __init__(self, data: EXT2Data):
        self.data = data
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as self.file:
            self.superblockc_read(data, file)
            root_num_descriptor = 2
            self._table_descriptor_block(file, data)
            self._inode(root_num_descriptor)
            # self.get_inode(data, 8)
            logging.debug(str(data))

    def _table_descriptor_block(self, file, data: EXT2Data):
        block_size = 32
        data.block_size = 1024 << int(data.s_log_block_size)
        data.group_count = math.ceil(int(data.s_blocks_count, 16) / int(data.s_blocks_per_group, 16))
        seek_descriptor = (int(data.s_first_data_block, 16) + 1) * data.block_size
        for i in range(data.group_count):
            file.seek(seek_descriptor + i * block_size)
            buf = file.read(block_size).hex()

            descriptor_g = EXT2DescriptorGroup(i)
            self.table_descriptor_block_init(descriptor_g, buf)
            descriptor_g.start = int(data.s_first_data_block, 16) + i * int(data.s_blocks_per_group, 16)
            descriptor_g.end = descriptor_g.start + int(data.s_blocks_per_group, 16)
            data.group_description_table.append(descriptor_g)

            logging.debug(f"Descriptor: {str(descriptor_g)}")

    def _inode(self, inodes_num, file):
        group_index = (inodes_num - 1) % int(data.s_inodes_per_group, 16)
        block_disc = data.group_description_table[(inodes_num - 1) / int(data.s_inodes_per_group, 16)]
        offset = block_disc.inode_table * data.block_size   # go to inode table
        offset += group_index * data.s_inode_size
        # a = e2inode(inodes_num, self.io, offset, data.s_inode_size)

        file.seek(offset)
        buf = file.read(data.s_inode_size).hex()
        inode = EXT2Inode()
        self.inode_init(inode, buf)

        self.block_list = self._block_list_creater(inode)

    def __list_of_double_indirects(self, block: str):
        blocks = []
        for i in range(self.data.block_size / 4):
            aggregate_element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]))
            if aggregate_element_block is 0:
                return blocks
            ib = self.read_block(aggregate_element_block).hex()
            blocks += self.__list_of_indirects(ib)
        return blocks

    def __list_of_indirects(self, block: str):
        blocks = []
        for i in range(self.data.block_size / 4):
            element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]))
            if element_block is 0:
                return blocks
            blocks.append(element_block)
        return blocks

    def read_block(self, block_num):
        self.file.seek(block_num * self.data.block_size)
        buf = self.file.read(self.data.block_size)
        return buf

    def _block_list_creater(self, inode):
        blocks = []
        first_block_level = 12
        for i in range(first_block_level):
            block_num = inode.i_block[i]
            if block_num == 0:
                return blocks
            blocks.append(block_num)
        if inode.i_block[13] != 0:
            blocks = self.__check_first_double_block(inode, blocks)
        return blocks

    def __check_first_double_block(self, inode: EXT2Inode, blocks: list) -> list:
        double_block = inode.i_block[13]
        i1b = self.read_block(double_block).hex()
        blocks += self.__list_of_indirects(i1b)

        if int(inode.i_block[14]) != 0:
            blocks = self.__check_first_three_block(inode, blocks)
        return blocks

    def __check_first_three_block(self, inode: EXT2Inode, blocks: list) -> list:
        three_block = int(inode.i_block[14])
        i2b = self.read_block(three_block).hex()
        blocks += self.__list_of_double_indirects(i2b)

        if int(inode.i_block[15]) != 0:
            blocks += self.__check_first_name_ref(inode)
        return blocks

    def __check_first_name_ref(self, inode: EXT2Inode):
        # TODO: Рефакторинг всей работы с инодом, срочно ебать, это просто вьетнам нахуй.
        blocks = []
        i3b_num = int(inode.i_block[15])
        block = self.read_block(i3b_num).hex()
        for i in range(self.data.block_size / 4):
            element_block = int(self.reversed_byte_ararry(block[0 + 8 * i:8 + 8 * i]))
            if element_block is 0:
                return blocks
            dib = self.read_block(element_block)
            blocks.extend(self.__list_of_double_indirects(dib))

        return blocks

    def superblockc_read(self, data: EXT2Data, file):
        file.seek(1024)
        superblock = file.read(1024).hex()
        self.super_block_initilaiz(data, superblock)
        if data.s_magic != "ef53":
            self.error = "Файловая система не является EXT2"
            exit()

        logging.debug(f"Magic: {data.s_magic}, State: {data.s_state}, Error: {data.s_errors}")

    # Функция получения содержимого inode по его номеру
    def get_inode(self, data: EXT2Data, inode_num: int):
        # Вычисляем номер группы блоков, в которой находится inode с порядковым номером inode_num:
        group = (inode_num - 1) / int(data.s_inodes_per_group, 16)

        index = (inode_num - 1) % int(data.s_inodes_per_group, 16)

        containing_block = (index * int(data.s_inode_size, 16)) // data.block_size

        #pos = ((__u64)da.bg_inode_table) * data.block_size + (index * int(data.s_inode_size, 16))
        logging.debug(f"Num inode: {inode_num}, Her group: {group}, Index: {index}, Containing block {containing_block}")
    """
            Из таблицы дескрипторов групп извлекаем дескриптор группы group и копируем его в структуру struct ext2_group_desc gd:
            memset((void *)&gd, 0, sizeof(gd));
            memcpy((void *)&gd, buff_grp + (group * (sizeof(gd))), sizeof(gd));
            Вычисляем позицию inode c порядковым номером inode_num в таблице inode группы group и считываем этот inode в структуру struct ext2_inode:
            index = (inode_num - 1) % sb.s_inodes_per_group;
            pos = ((__u64)gd.bg_inode_table) * BLKSIZE + (index * sb.s_inode_size);
            pread64(indev, in, sb.s_inode_size, pos);
            return;
    """

    def inode_init(self, inode: EXT2Inode, inode_byte: str):
        inode.i_mode = self.reversed_byte_ararry(inode_byte[0:4])  # 0	    2
        inode.i_uid = self.reversed_byte_ararry(inode_byte[4:8])  # 2	    2
        inode.i_size = self.reversed_byte_ararry(inode_byte[8:16])  # 4	    4
        inode.i_gid = self.reversed_byte_ararry(inode_byte[48:52])  # 24	    2
        inode.i_links_count = self.reversed_byte_ararry(inode_byte[52:56])  # 26	    2
        for i in range(15):
            inode.i_block.append(self.reversed_byte_ararry(inode_byte[80 + i * 8:88 + i * 8]))  # 40	    15 х 4

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
