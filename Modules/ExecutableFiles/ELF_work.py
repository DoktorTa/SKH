from Modules.ExecutableFiles.ELF_read import ELFReader
from Modules.ExecutableFiles.Interface_Executable_File import IExecutableFile


class ELFWork(IExecutableFile):
    """
        Класс выполняет роль контроллера доступа, интерфейс не является обязательным,
        ввиду отсуцтвия у меня понимани структуры других исполняемых файлов.
    """
    __elf: ELFReader

    def __init__(self, data, file):
        self.__elf = ELFReader(data, file)

    def get_hendler(self) -> dict:
        self.__elf.load_header_read()
        if self.__elf.data.e_ident.get("ei_mag0") == b'\x7fELF':
            extension = "7fELF"
        else:
            extension = None
        hendler = {
            "extension": extension,
            "border": self.__elf.data.byte_order,
            "bitclass": str(self.__elf.data.bit_class),
            "amachine": self.__elf.data.e_middle_load_record.get("e_machine")
        }
        return hendler

    def get_section_table(self) -> list:
        pass

    def get_table_hendler(self) -> list:
        pass
