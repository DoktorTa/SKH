import unittest
from Modules.FS.FAT_comand_sys import CommandFAT3216
from Modules.FS.FAT3216_data import FATData


class TestComSysFAT3216(unittest.TestCase):

    def test_cd(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            c = CommandFAT3216(file)

            answer_0 = [['.          ', '10', '5072', 0, 3, ''],
                        ['..         ', '10', '5072', 0, 0, ''],
                        ['1D         ', '10', '5072', 0, 4, ''],
                        ['2D         ', '10', '5072', 0, 16, ''],
                        ['3D         ', '10', '5072', 0, 17, ''],
                        ['1F      TXT', '20', '5072', 13, 18, '1\x00F\x00.\x00t\x00x\x00t\x00\x00\x00ÿÿÿÿÿÿÿÿÿÿÿÿ']]
            answer_1 = [['T16        ', '10', '5072', 0, 3, '']]
            error_0 = 0
            error_1 = 1

            self.assertEqual(c.cd(c.root, 0), (answer_0, error_0))
            self.assertEqual(c.cd(answer_0, 1), (answer_1, error_0))
            self.assertEqual(c.cd(answer_0, 5), (answer_0, error_1))
            self.assertEqual(c.cd(c.root, 10), (c.root, -1))

    def test_read(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            c = CommandFAT3216(file)

            file.seek(122880)
            answer = file.read(2048)
            answer = answer.hex()
            claster_sq = [3]
            error = 0
            self.assertEqual(c.read(c.root, 0, 1, 0), (answer, 1, error))
            self.assertEqual(c.read(c.root, 10, 1, 0), ("", 0, -1))


if __name__ == '__main__':
    unittest.main()
