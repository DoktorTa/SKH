import unittest
from Modules.ExecutableFiles.ELF_data import ELFData
from Modules.ExecutableFiles.ELF_data import ELFReader


class TestELFReader(unittest.TestCase):
    def test_e_ident_init(self):
        data = ELFData()
        elf = ELFReader(data)
        e_ident_s = r"7f454c46 02 01 01 000000000000000000"
        e_ident_b = b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00"
        elf.e_ident_init(e_ident_b)

        self.assertEqual(data.e_ident.get("ei_mag0"), data.ELF_SIGNATURE)
        self.assertEqual(data.e_ident.get("ei_class"), data.ELF_CLASS_64)
        self.assertEqual(data.e_ident.get("ei_data"), data.ELF_DATA_2LSB)
        self.assertEqual(data.e_ident.get("ei_version"), data.EV_CURRENT)
        self.assertEqual(data.e_ident.get("ei_osabi"), data.ELF_OS_ABI_NONE)


if __name__ == '__main__':
    unittest.main()
