import unittest

from Modules.FS.EXT2_read import EXT2Reader
from Modules.FS.EXT2_data import EXT2Data, EXT2Inode


class TestReadEXT2(unittest.TestCase):

    def test_revers_block(self):
        red = EXT2Reader

        test_data = [("aa", "aa"), ("aabb", "bbaa"), ("7b5bab", "ab5b7b")]

        for test in test_data:
            data, answer = test
            self.assertEqual(red._reversed_byte_ararry(data), answer)

    def test_superblock_check(self):
        fake_data = EXT2Data()
        red = EXT2Reader(fake_data, 1)

        fake_data.s_magic = "0000"
        red._superblock_check()
        self.assertEqual(red.error, 1)
        fake_data.s_magic = "ef53"
        red.error = 0

        feature = ["0001", "0002", "0004", "0008", "0010"]

        for incompat in feature:
            fake_data.s_feature_incompat = incompat
            red._superblock_check()
            self.assertEqual(red.error, 1)
            red.error = 0

        fake_data.s_feature_incompat = "0000"
        self.assertEqual(red.error, 0)
        red.error = 0

    def test_read_straight_blocks(self):
        fake_data = EXT2Data()

        red = EXT2Reader(fake_data, 1)
        inode_data = []

        inode_data.append(([508, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [508]))

        inode_data.append(([509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 0, 0, 0],
                           [509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520]))

        for element in inode_data:
            inode = EXT2Inode()
            inode_i_block, bloks_list = element
            inode.i_block = inode_i_block
            self.assertEqual(red._read_straight_blocks(inode), bloks_list)
