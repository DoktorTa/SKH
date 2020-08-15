import unittest

from Modules.FS.EXT2_command_sys import CommandEXT2
from Modules.FS.EXT2_data import EXT2Data
from Modules.FS.EXT2_read import EXT2Reader


class TestComSysEXT2(unittest.TestCase):

    def test_conversion(self):
        com_sys = CommandEXT2
        elements_ok = []
        elements_not_ok = []

        test_1 = (['00000002', '000c', '01', '02', '.'], ['.', 'D', 0, 0, '00000002', 0])
        test_2 = (['99999999', '000c', '02', '02', '..'], ['..', 'D', 0, 0, '99999999', 0])
        test_3 = (['00000000', '000c', '0b', '02', 'NETTENANETA'], ['NETTENANETA', 'D', 0, 0, '00000000', 0])
        test_4 = (['00000baa', '000c', '0', '03', ''], ['', 'F', 0, 0, '00000baa', 0])
        test_5 = (['00000000', '000c', '0', '03', ''], [])

        # ['', 'F', 0, 0, '00000000', 0]
        elements_ok.append(([test_1[0]], [test_1[1]]))
        elements_ok.append(([test_2[0]], [test_2[1]]))
        elements_ok.append(([test_3[0]], [test_3[1]]))
        elements_ok.append(([test_4[0]], [test_4[1]]))
        elements_ok.append(([test_5[0]], []))

        elements_ok.append(([test_2[0], test_3[0], test_4[0]], [test_2[1], test_3[1], test_4[1]]))

        elements_ok.append(([test_1[0], test_2[0], test_3[0], test_4[0]], [test_1[1], test_2[1], test_3[1], test_4[1]]))

        elements_not_ok.append(([test_1[0]], [test_1[0]]))
        elements_not_ok.append(([test_2[0]], [test_1[1]]))

        elements_not_ok.append(([test_2[0], test_1[0]], [test_1[1], test_2[1]]))
        elements_not_ok.append(([test_2[0], test_3[0]], [test_3[0], test_4[1]]))

        elements_not_ok.append(([test_1[1], test_2[1], test_3[1], test_4[1]], [test_1[0], test_2[0], test_3[0], test_4[0]]))

        for element in elements_ok:
            element_old, element_new = element
            self.assertEqual(com_sys._conversion(element_old), element_new)

        for element in elements_not_ok:
            element_old, element_new = element
            self.assertNotEqual(com_sys._conversion(element_old), element_new)

    def test_cd(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as file:
            # data = EXT2Data()
            # p = EXT2Reader(data, file)
            com = CommandEXT2(file)
            root = com.get_root()

            root_dir = [['.', 'D', 0, 0, '00000002', 0],
                        ['..', 'D', 0, 0, '00000002', 0],
                        ['lost+found', 'D', 0, 0, '0000000b', 0],
                        ['ext2_test', 'D', 0, 0, '00002e51', 0]]
            lost_found_dir = [['.', 'D', 0, 0, '0000000b', 0], ['..', 'D', 0, 0, '00000002', 0]]
            ext2_test_dir = [['.', 'D', 0, 0, '00002e51', 0],
                             ['..', 'D', 0, 0, '00000002', 0],
                             ['fdd.img', 'F', 0, 0, '00002e52', 0],
                             ['test12.img', 'F', 0, 0, '00002e53', 0],
                             ['script', 'F', 0, 0, '00002e54', 0],
                             ['1.x', 'F', 0, 0, '00002e55', 0],
                             ['TestC0', 'D', 0, 0, '00002e56', 0]]
            testc0_dir = [['.', 'D', 0, 0, '00002e56', 0],
                          ['..', 'D', 0, 0, '00002e51', 0],
                          ['TestC1', 'D', 0, 0, '00002e57', 0],
                          ['file0.txt', 'F', 0, 0, '00002e5a', 0]]
            testc1_dir = [['.', 'D', 0, 0, '00002e57', 0],
                          ['..', 'D', 0, 0, '00002e56', 0],
                          ['file1.txt', 'F', 0, 0, '00002e58', 0],
                          ['file2.txt', 'F', 0, 0, '00002e59', 0]]

            self.assertEqual(root, root_dir)

            self.assertEqual(com.cd(root_dir, 2), (lost_found_dir, 0))
            self.assertEqual(com.cd(root_dir, 3), (ext2_test_dir, 0))
            self.assertEqual(com.cd(ext2_test_dir, 6), (testc0_dir, 0))
            self.assertEqual(com.cd(testc0_dir, 2), (testc1_dir, 0))

            self.assertEqual(com.cd(ext2_test_dir, 1), (root_dir, 0))
            self.assertEqual(com.cd(ext2_test_dir, 0), (ext2_test_dir, 0))

            self.assertEqual(com.cd(root_dir, 5), (root_dir, -1))

    def test_read(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\t_ext2.img", "rb") as file:
            with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\FS\Test_blocks_ext2.txt", "r") as file_blocks:
                # data = EXT2Data()
                # p = EXT2Reader(data, file)
                com = CommandEXT2(file)
              root = com.get_root()
                dir, b = com.cd(root, 3)
                # print(dir)

                first_block = file_blocks.read(2048)
                next_line = file_blocks.read(1)
                second_block = file_blocks.read(2048)

                self.assertEqual(com.read(dir, 3, 1, 0), (first_block, 1, 0))
                self.assertEqual(com.read(dir, 3, 2, 0), (first_block + second_block, 2, 0))
                self.assertEqual(com.read(dir, 3, -1, 1), (first_block, 0, 0))
                self.assertEqual(com.read(dir, 3, -2, 2), (first_block + second_block, 0, 0))
