import unittest
import os

from Modules.HexEditor.Read_file import HexOpen


class TestOpenFile(unittest.TestCase):
    def test_get_page(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + r'\num.txt', r"rb") as file:
            error = 0

            h_open = HexOpen(file)
            len_block = h_open.get_len_block

            for inc in range(5):
                answer = file.read(len_block)
                file.seek(len_block * inc)
                self.assertEqual(h_open._get_page(), (answer, error))

        self.assertEqual(h_open._get_page(), (b'', -1))

    def test_get_data(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + r'\num.txt', r"rb") as file:
            answer = file.read()
            error = 0

            file.seek(0)
            h_open = HexOpen(file)

            self.assertEqual(h_open.get_data(20), (answer, error))

            self.assertEqual(h_open.get_data(-20), (answer, error))


if __name__ == '__main__':
    unittest.main()
