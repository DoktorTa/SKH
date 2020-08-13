import unittest

from Modules.ExecutableFiles.ELF_work import ELFWork
from Modules.ExecutableFiles.ELF_read import ELFReader
from Modules.ExecutableFiles.ELF_data import ELFData


class TestELFWork(unittest.TestCase):

    def test_get_header(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            data = ELFData()
            elf = ELFWork(file)

            answer = {"extension": "7fELF",
                      "border": "<",
                      "bitclass": "64",
                      "amachine": ("EM_X86_64", "x86-64")}
            self.assertEqual(elf.get_header(), answer)

    def test_get_table_hendler(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            data = ELFData()
            elf = ELFWork(file)

        answer = [
            {'p_type': 6, 'p_flags': 4, 'p_offset': 64, 'p_vaddr': 64, 'p_paddr': 64, 'p_filesz': 616, 'p_memsz': 616, 'p_align': 8},
            {'p_type': 3, 'p_flags': 4, 'p_offset': 680, 'p_vaddr': 680, 'p_paddr': 680, 'p_filesz': 28, 'p_memsz': 28, 'p_align': 1},
            {'p_type': 1, 'p_flags': 4, 'p_offset': 0, 'p_vaddr': 0, 'p_paddr': 0, 'p_filesz': 13368, 'p_memsz': 13368, 'p_align': 4096},
            {'p_type': 1, 'p_flags': 5, 'p_offset': 16384, 'p_vaddr': 16384, 'p_paddr': 16384, 'p_filesz': 76873, 'p_memsz': 76873, 'p_align': 4096}
        ]

        table_heanders = elf.get_table_header()
        for inc in range(4):
            self.assertEqual(table_heanders[inc], answer[inc])

    def test_get_section_table(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            data = ELFData()
            elf = ELFWork(file)

        answer = [
            {'sh_name': '.shstrtab\x00', 'sh_type': 0, 'sh_flags': 0, 'sh_addr': 0, 'sh_offset': 0, 'sh_size': 0, 'sh_link': 0, 'sh_info': 0, 'sh_addralign': 0, 'sh_entsize': 0},
            {'sh_name': 'interp\x00', 'sh_type': 1, 'sh_flags': 2, 'sh_addr': 680, 'sh_offset': 680, 'sh_size': 28, 'sh_link': 0, 'sh_info': 0, 'sh_addralign': 1, 'sh_entsize': 0},
            {'sh_name': 'note.gnu.build-id\x00', 'sh_type': 7, 'sh_flags': 2, 'sh_addr': 708, 'sh_offset': 708, 'sh_size': 36, 'sh_link': 0, 'sh_info': 0, 'sh_addralign': 4, 'sh_entsize': 0},
            {'sh_name': 'note.ABI-tag\x00', 'sh_type': 7, 'sh_flags': 2, 'sh_addr': 744, 'sh_offset': 744, 'sh_size': 32, 'sh_link': 0, 'sh_info': 0, 'sh_addralign': 4, 'sh_entsize': 0},
            {'sh_name': 'gnu.hash\x00', 'sh_type': 1879048182, 'sh_flags': 2, 'sh_addr': 776, 'sh_offset': 776, 'sh_size': 172, 'sh_link': 5, 'sh_info': 0, 'sh_addralign': 8, 'sh_entsize': 0},
            {'sh_name': 'dynsym\x00', 'sh_type': 11, 'sh_flags': 2, 'sh_addr': 952, 'sh_offset': 952, 'sh_size': 3096, 'sh_link': 6, 'sh_info': 1, 'sh_addralign': 8, 'sh_entsize': 24},
            {'sh_name': 'dynstr\x00', 'sh_type': 3, 'sh_flags': 2, 'sh_addr': 4048, 'sh_offset': 4048, 'sh_size': 1460, 'sh_link': 0, 'sh_info': 0, 'sh_addralign': 1, 'sh_entsize': 0},
            {'sh_name': 'gnu.version\x00', 'sh_type': 1879048191, 'sh_flags': 2, 'sh_addr': 5508, 'sh_offset': 5508, 'sh_size': 258, 'sh_link': 5, 'sh_info': 0, 'sh_addralign': 2, 'sh_entsize': 2},
            {'sh_name': 'gnu.version_r\x00', 'sh_type': 1879048190, 'sh_flags': 2, 'sh_addr': 5768, 'sh_offset': 5768, 'sh_size': 112, 'sh_link': 6, 'sh_info': 1, 'sh_addralign': 8, 'sh_entsize': 0},
            {'sh_name': 'rela.dyn\x00', 'sh_type': 4, 'sh_flags': 2, 'sh_addr': 5880, 'sh_offset': 5880, 'sh_size': 4944, 'sh_link': 5, 'sh_info': 0, 'sh_addralign': 8, 'sh_entsize': 24},
            {'sh_name': 'rela.plt\x00', 'sh_type': 4, 'sh_flags': 66, 'sh_addr': 10824, 'sh_offset': 10824, 'sh_size': 2544, 'sh_link': 5, 'sh_info': 24, 'sh_addralign': 8, 'sh_entsize': 24}
        ]

        section_heanders = elf.get_section_table()
        for inc in range(11):
            self.assertEqual(section_heanders[inc], answer[inc])


if __name__ == '__main__':
    unittest.main()
