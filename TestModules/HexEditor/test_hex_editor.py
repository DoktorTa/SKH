import unittest

from Modules.HexEditor.Hex_presentor import HexPresentor


class TestHexPresentor(unittest.TestCase):

    def test_row_creator(self):
        hex_e = HexPresentor()

        answer = [['00000000', '00000016', '00000032', '00000048', '00000064'],
                  ['00000000', '00000008', '00000016', '00000024', '00000032', '00000040', '00000048', '00000056'],
                  ['00000032', '00000064', '00000096', '00000128'],
                  ['00000004', '00000008', '00000012', '00000016']]
        self.assertEqual(hex_e.row_creator(5, 16, 0), answer[0])
        self.assertEqual(hex_e.row_creator(8, 8, 0), answer[1])
        self.assertEqual(hex_e.row_creator(4, 32, 1), answer[2])
        self.assertEqual(hex_e.row_creator(4, 4, 1), answer[3])

    def test_ascii_creator(self):
        hex_e = HexPresentor()
        answer = []
        pass

    def test_hex_presentor(self):
        hex_e = HexPresentor()

        data = [b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
                b'\x00\x01\x02\x03\x04\x05\x06\x07',
                b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f',
                b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f']
        answer = [['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f'],
                  ['00', '01', '02', '03', '04', '05', '06', '07'],
                  ['00', '01', '02', '03'],
                  ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f',
                   '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f']]
        steps = []

        for inc in range(4):
            self.assertEqual(hex_e.hex_presentor(data[inc]), answer[inc])
