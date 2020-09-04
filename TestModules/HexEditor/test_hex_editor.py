import unittest

from Modules.HexEditor.Hex_presentor import HexPresentor


class TestHexPresentor(unittest.TestCase):

    def test_row_creator(self):
        hex_e = HexPresentor()

        answer = [['00000000', '00000016', '00000032', '00000048', '00000064'],
                  ['00000000', '00000008', '00000016', '00000024', '00000032',
                   '00000040', '00000048', '00000056'],
                  ['00000032', '00000064', '00000096', '00000128'],
                  ['00000004', '00000008', '00000012', '00000016']]
        self.assertEqual(hex_e._row_creator(5, 16, 0), answer[0])
        self.assertEqual(hex_e._row_creator(8, 8, 0), answer[1])
        self.assertEqual(hex_e._row_creator(4, 32, 1), answer[2])
        self.assertEqual(hex_e._row_creator(4, 4, 1), answer[3])

    def test_ascii_creator(self):
        hex_e = HexPresentor()
        data = [b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e'
                b'\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d'
                b'\x1e'
                b'\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d'
                b'\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c'
                b'\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b'
                b'\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a'
                b'\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69'
                b'\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78'
                b'\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87'
                b'\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96'
                b'\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5'
                b'\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4'
                b'\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3'
                b'\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2'
                b'\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1'
                b'\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0'
                b'\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
                b'']
        answer = [[['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06',
                    '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e',
                    '\x0f'],
                   ['\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16',
                    '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d',
                    '\x1e', '\x1f'],
                   [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
                    '+', ',', '-', '.', '/'],
                   ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
                    ';', '<', '=', '>', '?'],
                   ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O'],
                   ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                    '[', '\\', ']', '^', '_'],
                   ['`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o'],
                   ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '{', '|', '}', '~', '\x7f'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.'],
                   ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                    '.', '.', '.', '.', '.']]]

        self.assertEqual(hex_e._ascii_creator(data[0], 16), answer[0])

    def test_hex_presentor(self):
        hex_e = HexPresentor()

        data = [b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e'
                b'\x0f',
                b'\x00\x01\x02\x03\x04\x05\x06\x07',
                b'\x00\x01\x02\x03\x04\x05\x06\x07',
                b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e'
                b'\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d'
                b'\x1e\x1f',
                b'\x00\x01\x02\x03\x04\x05\x06\x07']
        answer = [[['00', '01', '02', '03', '04', '05', '06', '07',
                    '08', '09', '0a', '0b', '0c', '0d', '0e', '0f']],
                  [['00', '01', '02', '03', '04', '05', '06', '07']],
                  [['00', '01', '02', '03'], ['04', '05', '06', '07']],
                  [['00', '01', '02', '03', '04', '05', '06', '07',
                    '08', '09', '0a', '0b', '0c', '0d', '0e', '0f',
                   '10', '11', '12', '13', '14', '15', '16', '17',
                    '18', '19', '1a', '1b', '1c', '1d', '1e', '1f']],
                  [['00', '01', '02', '03', '04', '05', '06', '07',
                    '00', '00', '00', '00', '00', '00', '00', '00']]]
        steps = [16, 8, 4, 32, 16]

        for inc in range(4):
            self.assertEqual(hex_e._hex_creator(data[inc], steps[inc]),
                             answer[inc])
