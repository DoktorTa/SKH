import unittest

from Modules.HexEditor.Hex_save import HexSave


class TestHexSave(unittest.TestCase):
    def test_create_list(self):
        test_data = {'000000000': '3120', '100000016': '3120', '200000032': '3120', 'f00001008': '3120', '000001024': '3220',
                     '500001264': '3220'}
        answer = ({0: '3120', 17: '3120', 34: '3120', 1023: '3120',
                  1024: '3220', 1269: '3220'}, [0, 17, 34, 1023, 1024, 1269])

        hex_s = HexSave
        self.assertEqual(hex_s._HexSave__create_list(test_data), answer)

    def test_write_on_file(self):
        test_history = {'000000000': '3120', '100000016': '3120', '200000032': '3120', 'f00001008': '3120', '000001024': '3220',
                        '500001264': '3220'}
        hex_s = HexSave(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\numbe.txt', test_history)
        with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\numbe_test.txt', 'rb') as file_answer:
            with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\numbe.txt', 'rb') as file_test:
                test_data = file_test.read()
                answer_data = file_answer.read()
                print("\n", test_data, '\n', answer_data)
                self.assertEqual(test_data, answer_data)
        with open(r'A:\Programming languages\In developing\Python\SKH\TestModules\HexEditor\numbe.txt', 'w') as file:
            file.write('1' * 1024 + '2' * 1024)


if __name__ == '__main__':
    unittest.main()
