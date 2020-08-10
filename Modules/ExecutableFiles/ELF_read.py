import logging
import struct
import copy

from Modules.ExecutableFiles.ELF_data import ELFData, ELFTableHendler, ELFHendlerSection


class ELFReader:
    data: ELFData

    def __init__(self, data: ELFData, file):
        self.data = data
        self.file = file

    def create_name_all_section(self):
        buf = []
        name = ""
        sumbol = "."
        count_section = len(self.data.section_hendler_records) - 1

        section_name_data = self.__name_segment_get()

        for inc in range(count_section):
            section = self.data.section_hendler_records.pop(0)
            sh_name = section.program_hendler_section_fileds.get("sh_name") + 1

            while ord(sumbol) != 0:
                sumbol = section_name_data[sh_name]
                sumbol = chr(sumbol)
                name += sumbol
                sh_name += 1

            section.program_hendler_section_fileds.update({"sh_name": name})
            buf.append(section)

            name = ""
            sumbol = "."

            logging.debug(f"{str(section)}")

        self.data.section_hendler_records = copy.deepcopy(buf)

    def program_hendler_section_read(self):
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
                section = ELFHendlerSection()

                self.file.seek(section_table_seek + (inc * element_size))
                element_b = self.file.read(element_size)

                section = self._program_hendler_section_init(element_b, section)
                self.data.section_hendler_records.append(section)

    def _program_hendler_section_init(self, element_b: bytes, section: ELFHendlerSection) -> ELFHendlerSection:
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
            section.program_hendler_section_fileds.update({section_keys[inc]: struct_section[inc]})

        # logging.debug(f"{str(section)}")
        return section

    def __name_segment_get(self) -> bytes:
        last_segment = self.data.section_hendler_records.pop()
        last_segment_seek = last_segment.program_hendler_section_fileds.get("sh_offset")
        last_segment_size = last_segment.program_hendler_section_fileds.get("sh_size")

        self.file.seek(last_segment_seek)
        last_segment_data = self.file.read(last_segment_size)

        return last_segment_data

    def program_header_table_read(self):
        table_hendler_seek = self.data.e_end_load_record.get("e_phoff")
        if table_hendler_seek == 0:
            logging.info(f"Смешение таблицы заголовков равно 0, она не существует")
        else:
            count_records = self.data.e_end_load_record.get("e_phnum")

            if self.data.bit_class == 32:
                element_table_size = 32
            else:  # self.data.bit_class == 64
                element_table_size = 56

            for inc in range(count_records):
                table_hendler = ELFTableHendler()

                self.file.seek(table_hendler_seek + (inc * element_table_size))
                element_table = self.file.read(element_table_size)

                table_hendler = self._program_header_table_init(element_table, table_hendler)
                self.data.tables_hendler_records.append(table_hendler)

    def _program_header_table_init(self, element_table: bytes, table_hendler: ELFTableHendler) -> ELFTableHendler:
        if self.data.bit_class == 32:
            hendler_format = "l7i"
            hendler_keys = ["p_type", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_flags", "p_align"]
        else:  # self.data.bit_class == 64
            hendler_format = "li6q"
            hendler_keys = ["p_type", "p_flags", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_align"]

        struct_hendler = struct.unpack(self.data.byte_order + hendler_format, element_table)
        for inc in range(len(struct_hendler)):
            table_hendler.program_header_fields.update({hendler_keys[inc]: struct_hendler[inc]})

        logging.debug(str(table_hendler))
        return table_hendler

    def _e_load_init(self, e_load: bytes):

        elf_e_ident = ["ei_mag0", "ei_class", "ei_data", "ei_version", "ei_osabi", "ei_abiversion",
                       "ei_pad0", "ei_pad1", "ei_pad2", "ei_pad3", "ei_pad4", "ei_pad5", "ei_pad6"]

        e_ident = e_load[:16]
        e_ident_format = "4s12b"
        struct_elf = struct.unpack(e_ident_format, e_ident)
        for inc in range(len(elf_e_ident)):
            self.data.e_ident.update({elf_e_ident[inc]: struct_elf[inc]})

        if self.data.e_ident.get("ei_data") == self.data.ELF_DATA_2LSB:
            self.data.byte_order = "<"
        else:  # self.data.e_ident.get("ei_data") == self.data.ELF_DATA_2MSB
            self.data.byte_order = ">"

        e_midel = e_load[16:24]
        e_midel_format = self.data.byte_order + "2hi"
        struct_elf = struct.unpack(e_midel_format, e_midel)
        elf_e_midle = ["e_type", "e_machine", "e_version"]
        for inc in range(3):
            self.data.e_middle_load_record.update({elf_e_midle[inc]: struct_elf[inc]})

        if self.data.e_ident.get("ei_class") == self.data.ELF_CLASS_32:
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
