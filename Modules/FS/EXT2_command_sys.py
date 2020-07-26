import logging

from Modules.FS.EXT2_data import EXT2Data, EXT2DescriptorGroup, EXT2Inode
from  Modules.FS.EXT2_read import EXT2Reader


class CommandEXT2:
    ext2_fs = 0
    root = []

    def __init__(self, ext2_fs: EXT2Reader):
        self.ext2_fs = ext2_fs
        root = self.ext2_fs.root_catalog_read()
        print(root)

    def cd(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    data = EXT2Data()
    p = EXT2Reader(data)
    com = CommandEXT2(p)