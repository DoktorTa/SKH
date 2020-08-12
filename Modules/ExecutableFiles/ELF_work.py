import copy

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
        self.__elf.load_header_read()
        self.__elf.program_header_table_read()
        self.__elf.program_header_section_read()
        self.__elf.create_name_all_section()

    def get_hendler(self) -> dict:
        if self.__elf.data.e_ident.get("ei_mag0") == ("ELF_SIGNATURE", ""):
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
        section_header = []

        section_header_records = self.__elf.data.section_header_records

        for section in section_header_records:
            section = copy.deepcopy(section.get_section)
            section_header.append(section)

        return section_header

    def get_table_hendler(self) -> list:
        table_headers = []

        table_headers_records = self.__elf.data.tables_header_records

        for header in table_headers_records:
            header = copy.deepcopy(header.get_header)
            table_headers.append(header)

        return table_headers
