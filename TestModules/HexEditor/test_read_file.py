import unittest

from Modules.HexEditor.Read_file import HexOpen


class TestOpenFile(unittest.TestCase):
    def test_get_page(self):
        with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\num.txt', r"rb") as file:
            answer = file.read(1024)
            file.seek(0)

            h_open = HexOpen(file)
            len_block = h_open.get_len_block

            for inc in range(5):
                answer = file.read(len_block)
                file.seek(len_block * inc)
                self.assertEqual(h_open.get_page(), (answer, 0))

            for inc in range(5):
                file.seek(len_block * (5 - inc))
                answer = file.read(len_block)
                self.assertEqual(h_open.get_page(early=True), (answer, 0))

        self.assertEqual(h_open.get_page(), (b'', -1))




if __name__ == '__main__':
    unittest.main()
