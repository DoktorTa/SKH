import unittest

from Modules.ExecutableFiles.ELF_work import ELFWork
from Modules.ExecutableFiles.ELF_read import ELFReader
from Modules.ExecutableFiles.ELF_data import ELFData


class TestELFWork(unittest.TestCase):
    def test_get_header(self):
        with open(r"A:\Programming languages\In developing\Python\SKH\TestModules\ExecutableFiles\ls.elf", "rb") as file:
            data = ELFData()
            elf = ELFWork(data, file)

            answer = {"extension": "7fELF",
                      "border": "<",
                      "bitclass": "64",
                      "amachine": "x86-64"}
            self.assertEqual(elf.get_hendler(), answer)


if __name__ == '__main__':
    unittest.main()
