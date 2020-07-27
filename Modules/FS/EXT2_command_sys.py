import logging

from Modules.FS.EXT2_data import EXT2Data, EXT2DescriptorGroup, EXT2Inode
from Modules.FS.EXT2_read import EXT2Reader
from Modules.FS.Interface_FS import IFSWork


class CommandEXT2(IFSWork):
    ext2_fs = 0
    root = []
    pwd = []

    def __init__(self, ext2_fs: EXT2Reader):
        self.ext2_fs = ext2_fs
        self.root = self.ext2_fs.root_catalog_read()

    def cd(self):
        pass

    def read(self):
        pass

    def get_pwd(self):
        return self.pwd

    def get_root(self):
        return self.root


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    data = EXT2Data()
    p = EXT2Reader(data)
    com = CommandEXT2(p)
    print(com.get_root())
