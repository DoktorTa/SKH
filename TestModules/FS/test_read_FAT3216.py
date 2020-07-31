import unittest

from Modules.FS.FAT321612_read import Reader


class TestReadFAT3216(unittest.TestCase):

    def test_root_catalog_reader(self):
        r = Reader()

        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            root = ([['T16        ', '10', '5072', 0, 3, '']], 0)
            self.assertEqual(r.root_catalog_read(file), root)

        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t32.img", "rb") as file:
            r.seek_fs = 4128768
            root = ([['SYSTEM~1   ', '16', '5077', 0, 3,
                     ' \x00I\x00n\x00f\x00o\x00r\x00m\x00a\x00t\x00i\x00o\x00n'
                     '\x00\x00\x00S\x00y\x00s\x00t\x00e\x00m\x00 \x00V\x00o\x00l\x00u\x00m\x00e\x00'],
                    ['1D         ', '10', '5077', 0, 6, ''],
                    ['2D         ', '10', '5077', 0, 7, ''],
                    ['3D         ', '10', '5077', 0, 8, ''],
                    ['1F      TXT', '20', '5077', 119, 9, '']], 0)
            self.assertEqual(r.root_catalog_read(file), root)


if __name__ == '__main__':
    unittest.main()
