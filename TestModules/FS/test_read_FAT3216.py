import unittest

from Modules.FS.FAT321612_read import FATReader
from Modules.FS.FAT3216_data import FATData


class TestReadFAT3216(unittest.TestCase):

    def test_root_catalog_reader(self):

        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            data = FATData()
            r = FATReader(data, file)
            root = ([['T16        ', '10', '5072', 0, 3, '']], 0)
            self.assertEqual(r.root_catalog_read(), root)

        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t32.img", "rb") as file:
            data1 = FATData()
            r1 = FATReader(data1, file)
            r1.set_seek_fs(4128768)
            root = ([['SYSTEM~1   ', '16', '5077', 0, 3,
                     ' \x00I\x00n\x00f\x00o\x00r\x00m\x00a\x00t\x00i\x00o\x00n'
                     '\x00\x00\x00S\x00y\x00s\x00t\x00e\x00m\x00 \x00V\x00o\x00l\x00u\x00m\x00e\x00'],
                    ['1D         ', '10', '5077', 0, 6, ''],
                    ['2D         ', '10', '5077', 0, 7, ''],
                    ['3D         ', '10', '5077', 0, 8, ''],
                    ['1F      TXT', '20', '5077', 119, 9, '']], 0)
            self.assertEqual(r1.root_catalog_read(), root)

    def test_mixing(self):
        data = FATData()
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\Test_load_sector_fat.txt", "rb") as file:
            reader = FATReader(data, file)

            fat16_seek_b = 2048
            rootfat16_dir_seek_b = 104448
            reader.set_seek_fs(0)
            reader.mixing()
            self.assertEqual(reader.fat_seek_b, fat16_seek_b)
            self.assertEqual(reader.root_dir_seek_b, rootfat16_dir_seek_b)

            fat32_seek_b = 297984
            rootfat32_dir_seek_b = 4194304
            reader.set_seek_fs(512)
            reader.mixing()
            self.assertEqual(reader.fat_seek_b, fat32_seek_b)
            self.assertEqual(reader.root_dir_seek_b, rootfat32_dir_seek_b)

    def test_build_cls_sequence(self):
        data = FATData()
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t32.img", "rb") as file:
            reader = FATReader(data, file)
            reader.set_seek_fs(4128768)
            reader.root_catalog_read()

            elements_claster = [("02", ([2], 0)), ("03", ([3], 0)), ("04", ([4], 0))]

            for element_claster in elements_claster:
                element_claster, answer = element_claster
                self.assertEqual(reader.build_cls_sequence(element_claster), answer)
