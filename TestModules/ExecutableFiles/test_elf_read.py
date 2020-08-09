import unittest
import logging

from Modules.ExecutableFiles.ELF_data import ELFData, ELFTableHendler
from Modules.ExecutableFiles.ELF_read import ELFReader


class TestELFReader(unittest.TestCase):
    e_load = b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
             b"\x03\x00\x3e\x00\x01\x00\x00\x00\x30\x61\x00\x00\x00\x00\x00\x00" \
             b"\x40\x00\x00\x00\x00\x00\x00\x00\x28\x17\x02\x00\x00\x00\x00\x00" \
             b"\x00\x00\x00\x00\x40\x00\x38\x00\x0b\x00\x40\x00\x1d\x00\x1c\x00"

    def test_program_hendler_section_read(self):
        data = ELFData()
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            elf = ELFReader(data, file)
            e_ident_b = self.e_load
            elf._e_load_init(e_ident_b)
            elf.program_hendler_section_read()

            section_hendler_records_answer = []

            # for inc in range(5):
            #     tables_hendler = str(data.section_hendler_records[inc])
            #     self.assertEqual(tables_hendler, str(section_hendler_records_answer[inc]))

    def test_name_section_read(self):
        pass

    def test_program_hendler_table_read(self):
        data = ELFData()
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            elf = ELFReader(data, file)
            e_ident_b = self.e_load
            elf._e_load_init(e_ident_b)
            elf.program_header_table_read()

            tables_hendler_records_answer = [
                {'p_type': 6, 'p_flags': 4, 'p_offset': 64, 'p_vaddr': 64, 'p_paddr': 64, 'p_filesz': 616, 'p_memsz': 616, 'p_align': 8},
                {'p_type': 3, 'p_flags': 4, 'p_offset': 680, 'p_vaddr': 680, 'p_paddr': 680, 'p_filesz': 28, 'p_memsz': 28, 'p_align': 1},
                {'p_type': 1, 'p_flags': 4, 'p_offset': 0, 'p_vaddr': 0, 'p_paddr': 0, 'p_filesz': 13368, 'p_memsz': 13368, 'p_align': 4096},
                {'p_type': 1, 'p_flags': 5, 'p_offset': 16384, 'p_vaddr': 16384, 'p_paddr': 16384, 'p_filesz': 76873, 'p_memsz': 76873, 'p_align': 4096},
                {'p_type': 1, 'p_flags': 4, 'p_offset': 94208, 'p_vaddr': 94208, 'p_paddr': 94208, 'p_filesz': 35088, 'p_memsz': 35088, 'p_align': 4096}
            ]

            for inc in range(5):
                tables_hendler = str(data.tables_hendler_records[inc])
                self.assertEqual(tables_hendler, str(tables_hendler_records_answer[inc]))

    def test_program_hendler_table_init(self):
        data = ELFData()
        elf = ELFReader(data, file=0)
        table_hedler = ELFTableHendler()
        data.bit_class = 64
        data.byte_order = "<"

        table_hedler_b = b"\x06\x00\x00\x00\x04\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00" \
                         b"\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00" \
                         b"\x68\x02\x00\x00\x00\x00\x00\x00\x68\x02\x00\x00\x00\x00\x00\x00" \
                         b"\x08\x00\x00\x00\x00\x00\x00\x00"
        elf._program_header_table_init(table_hedler_b, table_hedler)

        key = ['p_type', 'p_flags', 'p_offset', 'p_vaddr', 'p_paddr', 'p_filesz', 'p_memsz', 'p_align']
        answer = [6, 4, 64, 64, 64, 616, 616, 8]
        for inc in range(8):
            self.assertEqual(table_hedler.program_header_fields.get(key[inc]), answer[inc])

    def test_e_load_init(self):
        data = ELFData()
        elf = ELFReader(data, file=0)
        e_ident_b = self.e_load
        elf._e_load_init(e_ident_b)

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
            self.assertEqual(data.e_end_load_record.get(keys[inc]), true_value[inc])


if __name__ == '__main__':
    unittest.main()
