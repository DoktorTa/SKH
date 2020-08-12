import logging
import struct
import copy

from Modules.ExecutableFiles.ELF_data import ELFData, ELFTableHeader, ELFHeaderSection


class ELFReader:
    data: ELFData

    def __init__(self, data: ELFData, file):
        self.data = data
        self.file = file

    def create_name_all_section(self):
        buf = []
        name = ""
        symbol = "."
        count_section = len(self.data.section_header_records) - 1

        section_name_data = self.__name_segment_get()

        for inc in range(count_section):
            section = self.data.section_header_records.pop(0)
            sh_name = section.program_header_section_fileds.get("sh_name") + 1

            while ord(symbol) != 0:
                symbol = section_name_data[sh_name]
                symbol = chr(symbol)
                name += symbol
                sh_name += 1

            section.program_header_section_fileds.update({"sh_name": name})
            buf.append(section)

            name = ""
            symbol = "."

            logging.debug(f"{str(section)}")

        self.data.section_header_records = copy.deepcopy(buf)

    def program_header_section_read(self):
        section_table_seek = self.data.e_end_load_record.get("e_shoff")
        if section_table_seek == 0:
            logging.info(f"Смешение таблицы секций равно 0, она не существует.")
        else:
            count_records = self.data.e_end_load_record.get("e_shnum")

            if self.data.bit_class == 32:
                element_size = 40
            else:  # self.data.bit_class == 64
                element_size = 64

            for inc in range(count_records):
                section = ELFHeaderSection()

                self.file.seek(section_table_seek + (inc * element_size))
                element_b = self.file.read(element_size)

                section = self._program_header_section_init(element_b, section)
                self.data.section_header_records.append(section)

    def _program_header_section_init(self, element_b: bytes, section: ELFHeaderSection) -> ELFHeaderSection:
        if self.data.bit_class == 32:
            section_format = "10i"
            section_keys = ["sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset",
                            "sh_size", "sh_link", "sh_info", "sh_addralign", "sh_entsize"]
        else:  # self.data.bit_class == 64
            section_format = "2i4q2i2q"
            section_keys = ["sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset",
                            "sh_size", "sh_link", "sh_info", "sh_addralign", "sh_entsize"]

        struct_section = struct.unpack(self.data.byte_order + section_format, element_b)
        for inc in range(len(struct_section)):
            section.program_header_section_fileds.update({section_keys[inc]: struct_section[inc]})

        # logging.debug(f"{str(section)}")
        return section

    def __name_segment_get(self) -> bytes:
        last_segment = self.data.section_header_records.pop()
        last_segment_seek = last_segment.program_header_section_fileds.get("sh_offset")
        last_segment_size = last_segment.program_header_section_fileds.get("sh_size")

        self.file.seek(last_segment_seek)
        last_segment_data = self.file.read(last_segment_size)

        return last_segment_data

    def program_header_table_read(self):
        table_header_seek = self.data.e_end_load_record.get("e_phoff")
        if table_header_seek == 0:
            logging.info(f"Смешение таблицы заголовков равно 0, она не существует")
        else:
            count_records = self.data.e_end_load_record.get("e_phnum")

            if self.data.bit_class == 32:
                element_table_size = 32
            else:  # self.data.bit_class == 64
                element_table_size = 56

            for inc in range(count_records):
                table_header = ELFTableHeader()

                self.file.seek(table_header_seek + (inc * element_table_size))
                element_table = self.file.read(element_table_size)

                table_header = self._program_header_table_init(element_table, table_header)
                self.data.tables_header_records.append(table_header)

    def _program_header_table_init(self, element_table: bytes, table_header: ELFTableHeader) -> ELFTableHeader:
        if self.data.bit_class == 32:
            header_format = "l7i"
            header_keys = ["p_type", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_flags", "p_align"]
        else:  # self.data.bit_class == 64
            header_format = "li6q"
            header_keys = ["p_type", "p_flags", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_align"]

        struct_header = struct.unpack(self.data.byte_order + header_format, element_table)
        for inc in range(len(struct_header)):
            table_header.program_header_fields.update({header_keys[inc]: struct_header[inc]})

        logging.debug(str(table_header))
        return table_header

    def load_header_read(self):
        max_size_load_header = 64
        try:
            self.file.seek(0)
            load_sector = self.file.read(max_size_load_header)
            self._e_load_init(load_sector)
        except EOFError:
            logging.error(f"Размер файла недостаточен.")

    def _e_load_init(self, e_load: bytes):

        self.__e_ident_init(e_load)

        e_midel = e_load[16:24]
        e_midel_format = self.data.byte_order + "2hi"
        struct_elf = struct.unpack(e_midel_format, e_midel)
        elf_e_midle = ["e_type", "e_machine", "e_version"]
        elf_e_midle_value = [self.data.et_value, self.data.em_value, self.data.ev_version_value]
        for inc in range(3):
            try:
                value_group = elf_e_midle_value[inc]
                self.data.e_middle_load_record.update({elf_e_midle[inc]: value_group.get(struct_elf[inc])})
            except KeyError:
                value_group = elf_e_midle_value[inc]
                value_group.update({struct_elf[inc]: ("", "")})
                self.data.e_middle_load_record.update({elf_e_midle[inc]: value_group.get(struct_elf[inc])})

        if self.data.e_ident.get("ei_class") == self.data.elf_class_value.get(1):
            e_end_format = "4i6h"
            last_point = 28
            self.data.bit_class = 32
        else:  # self.data.e_ident.get("ei_class") == self.data.ELF_CLASS_64:
            e_end_format = "3qi6h"
            last_point = 40
            self.data.bit_class = 64

        e_end = e_load[24:24 + last_point]
        struct_elf = struct.unpack(e_end_format, e_end)
        elf_e_end = ["e_entry", "e_phoff", "e_shoff", "e_flags", "e_ehsize",
                     "e_phentsize", "e_phnum", "e_shentsize", "e_shnum", "e_shstrndx"]
        for inc in range(10):
            self.data.e_end_load_record.update({elf_e_end[inc]: struct_elf[inc]})

        logging.debug(str(self.data))

    def __e_ident_init(self, e_load: bytes):
        elf_e_ident = ["ei_mag0", "ei_class", "ei_data", "ei_version", "ei_osabi", "ei_abiversion",
                       "ei_pad0", "ei_pad1", "ei_pad2", "ei_pad3", "ei_pad4", "ei_pad5", "ei_pad6"]

        elf_e_ident_value = [self.data.elf_signature, self.data.elf_class_value, self.data.elf_data_value,
                             self.data.ev_version_value, self.data.elf_os_abi_value]

        e_ident = e_load[:16]
        e_ident_format = "4s12b"
        struct_elf = struct.unpack(e_ident_format, e_ident)
        for inc in range(5):
            try:
                value_group = elf_e_ident_value[inc]
                self.data.e_ident.update({elf_e_ident[inc]: value_group.get(struct_elf[inc])})
            except KeyError:
                value_group = elf_e_ident_value[inc]
                value_group.update({struct_elf[inc]: ("", "")})
                self.data.e_ident.update({e_ident[inc]: value_group.get(struct_elf[inc])})

        if self.data.e_ident.get("ei_data") == self.data.elf_data_value.get(1):
            self.data.byte_order = "<"
        else:  # self.data.e_ident.get("ei_data") == self.data.ELF_DATA_2MSB
            self.data.byte_order = ">"
