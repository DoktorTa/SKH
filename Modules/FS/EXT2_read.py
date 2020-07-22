import logging


from Modules.FS.EXT2_data import EXT2Data


class EXT2Reader:
    error = ""

    def __init__(self, data: EXT2Data):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as file:
            self.superblockc_read(data, file)
            self.table_descriptor_block(data, file)
            print(str(data))

    def superblockc_read(self, data: EXT2Data, file):
        file.seek(1024)
        superblock = file.read(1024).hex()
        self.super_block_initilaiz(data, superblock)
        if data.s_magic != "ef53":
            self.error = "Файловая система не является EXT2"
            exit()
        logging.debug(f"\nMagic: {data.s_magic}\n"
                      f"State: {data.s_state}\n"
                      f"Error: {data.s_errors}")

    def table_descriptor_block(self, data: EXT2Data, file):
        data.block_size = 1024 << int(data.s_log_block_size)
        seek_descriptor = (int(data.s_first_data_block) + 1) * data.block_size

        logging.debug(f"Seek descriptor block: {seek_descriptor}")

        file.seek(seek_descriptor)
        table_descriptor = file.read(32).hex()
        self.table_descriptor_block_init(data, table_descriptor)

    # Функция получения содержимого inode по его номеру
    def get_inode(self, data: EXT2Data, inode_num: int):
        # Вычисляем номер группы блоков, в которой находится inode с порядковым номером inode_num:
        group = (inode_num - 1) / data.s_inodes_per_group

        index = (inode_num - 1) % data.s_inodes_per_group

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

    @staticmethod
    def table_descriptor_block_init(data: EXT2Data, table_descriptor: str):
        data.bg_block_bitmap = table_descriptor[0:8]  # 0   4
        data.bg_inode_bitmap = table_descriptor[8:16]  # 4   4
        data.bg_inode_table = table_descriptor[16:24]  # 8   4

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
