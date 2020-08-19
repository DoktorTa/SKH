import unittest

from Modules.HexEditor.Read_file import HexOpen


class TestOpenFile(unittest.TestCase):
    def test_get_page(self):
        with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\num.txt', r"rb") as file:
            answer = file.read(1024)
            file.seek(0)

            error = 0

            h_open = HexOpen(file)
            len_block = h_open.get_len_block

            for inc in range(5):
                answer = file.read(len_block)
                file.seek(len_block * inc)
                self.assertEqual(h_open._get_page(), (answer, error))

        self.assertEqual(h_open._get_page(), (b'', -1))

    def test_get_data(self):
        with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\num.txt', r"rb") as file:
            answer = file.read()
            error = 0

            file.seek(0)
            h_open = HexOpen(file)

            self.assertEqual(h_open.get_data(20), (answer, error))

            self.assertEqual(h_open.get_data(-20), (answer, error))


if __name__ == '__main__':
    unittest.main()
