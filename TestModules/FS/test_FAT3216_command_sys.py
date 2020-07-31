import unittest
from Modules.FS.FAT_comand_sys import Command


class TestComSysFAT3216(unittest.TestCase):

    def test_cd(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            c = Command(file)

            answer_0 = [['.          ', '10', '5072', 0, 3, ''],
                        ['..         ', '10', '5072', 0, 0, ''],
                        ['1D         ', '10', '5072', 0, 4, ''],
                        ['2D         ', '10', '5072', 0, 16, ''],
                        ['3D         ', '10', '5072', 0, 17, ''],
                        ['1F      TXT', '20', '5072', 13, 18, '1\x00F\x00.\x00t\x00x\x00t\x00\x00\x00ÿÿÿÿÿÿÿÿÿÿÿÿ']]
            answer_1 = [['T16        ', '10', '5072', 0, 3, '']]
            error_0 = ""
            error_1 = "Элемент являеться файлом, а не директорией"

            self.assertEqual(c.cd(file, c.root, 0), (answer_0, error_0))
            self.assertEqual(c.cd(file, answer_0, 1), (answer_1, error_0))
            self.assertEqual(c.cd(file, answer_0, 5), (answer_0, error_1))

    def test_read(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\test16.img", "rb") as file:
            c = Command(file)

            file.seek(122880)
            answer = file.read(2048)
            answer = answer.hex()
            claster_sq = []
            error = ''
            self.assertEqual(c.read(file, c.root, 0), (answer, claster_sq, error))


if __name__ == '__main__':
    unittest.main()
