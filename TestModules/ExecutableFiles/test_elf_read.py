import unittest
import logging

from Modules.ExecutableFiles.ELF_data import ELFData, ELFTableHendler
from Modules.ExecutableFiles.ELF_read import ELFReader


class TestELFReader(unittest.TestCase):
    e_load = b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
             b"\x03\x00\x3e\x00\x01\x00\x00\x00\x30\x61\x00\x00\x00\x00\x00\x00" \
             b"\x40\x00\x00\x00\x00\x00\x00\x00\x28\x17\x02\x00\x00\x00\x00\x00" \
             b"\x00\x00\x00\x00\x40\x00\x38\x00\x0b\x00\x40\x00\x1d\x00\x1c\x00"

    def test_program_hendler_table_read(self):
        data = ELFData()
        elf = ELFReader(data, file=0)
        table_hedler = ELFTableHendler()
        e_ident_b = self.e_load
        # elf.e_load_init(e_ident_b)

        table_hedler = b"\x06\x00\x00\x00\x04\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00" \
                       b"\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00" \
                       b"\x68\x02\x00\x00\x00\x00\x00\x00\x68\x02\x00\x00\x00\x00\x00\x00" \
                       b"\x08\x00\x00\x00\x00\x00\x00\x00"

    def test_e_load_init(self):
        data = ELFData()
        elf = ELFReader(data, file=0)
        e_ident_b = self.e_load
        elf.e_load_init(e_ident_b)

        keys = ["ei_mag0", "ei_class", "ei_data", "ei_version", "ei_osabi"]
        true_value = [data.ELF_SIGNATURE, data.ELF_CLASS_64, data.ELF_DATA_2LSB, data.EV_CURRENT, data.ELF_OS_ABI_NONE]
        for inc in range(4):
            self.assertEqual(data.e_ident.get(keys[inc]), true_value[inc])

        keys = ["e_type", "e_machine", "e_version"]
        true_value = [data.ET_DYN, data.EM_X86_64, data.EV_CURRENT]
        for inc in range(2):
            self.assertEqual(data.e_middle_load_record.get(keys[inc]), true_value[inc])

        keys = ["e_entry", "e_phoff", "e_shoff", "e_flags", "e_ehsize",
                "e_phentsize", "e_phnum", "e_shentsize", "e_shnum", "e_shstrndx"]
        true_value = [24880, 64, 137000, 0, 64, 56, 11, 64, 29, 28]
        for inc in range(9):
            self.assertEqual(data.e_end_load_rectord.get(keys[inc]), true_value[inc])


if __name__ == '__main__':
    unittest.main()
