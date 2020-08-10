import unittest
import logging
import argparse

from TestModules.FS.test_EXT2_command_sys import TestComSysEXT2
from TestModules.FS.test_read_EXT2 import TestReadEXT2
from TestModules.FS.test_read_FAT3216 import TestReadFAT3216
from TestModules.FS.test_FAT3216_command_sys import TestComSysFAT3216

from TestModules.ExecutableFiles.test_elf_read import TestELFReader
from TestModules.ExecutableFiles.test_elf_work import TestELFWork


def main():
    logging.basicConfig(level=logging.CRITICAL)
    type_w, mode = arguments()

    test_group_fs = unittest.TestSuite()
    if ("a" in type_w) or ("f" in type_w):
        test_group_fs.addTest(TestComSysEXT2('test_conversion'))
        test_group_fs.addTest(TestReadEXT2('test_revers_block'))
        test_group_fs.addTest(TestReadEXT2('test_superblock_check'))
        test_group_fs.addTest(TestReadEXT2('test_read_straight_blocks'))

        test_group_fs.addTest(TestReadFAT3216('test_mixing'))
        if mode[0] == 1:
            test_group_fs.addTest(TestComSysEXT2('test_cd'))
            test_group_fs.addTest(TestComSysEXT2('test_read'))

            test_group_fs.addTest(TestReadFAT3216('test_build_cls_sequence'))
            test_group_fs.addTest(TestReadFAT3216('test_root_catalog_reader'))
            test_group_fs.addTest(TestComSysFAT3216('test_cd'))
            test_group_fs.addTest(TestComSysFAT3216('test_read'))

    if ("a" in type_w) or ("e" in type_w):
        test_group_fs.addTest(TestELFReader('test_e_load_init'))
        test_group_fs.addTest(TestELFReader('test_program_header_table_init'))

        if mode[0] == 1:
            test_group_fs.addTest(TestELFReader('test_program_header_table_read'))
            test_group_fs.addTest(TestELFReader('test_program_header_section_read'))
            test_group_fs.addTest(TestELFReader('test_load_header_read'))
            test_group_fs.addTest(TestELFWork('test_get_header'))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_group_fs)


def arguments() -> (str, int):
    parser = argparse.ArgumentParser(description='Test module script')

    parser.add_argument('-m', action="store", dest="mode", default=0, type=int, nargs=1,
                        help="Если на вашем устройстве сущетсвуют тестовые образы поволяюшие провести полное тестирование,"
                             "а так же вы хотите его провести установите в 1.")
    parser.add_argument('-t', action="store", dest="type", default="a", type=str, nargs=1,
                        help="Вы можете указать через запятую какие модули необходимо протестировать:\n"
                             "a - все модули,\n"
                             "f - модули файловой системы,\n"
                             "e - модули исполняемых файлов\n")

    args = parser.parse_args()
    type_w = args.type
    mode = args.mode
    return type_w, mode


if __name__ == '__main__':
    main()
