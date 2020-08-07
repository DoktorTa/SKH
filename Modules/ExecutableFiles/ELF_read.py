import logging
import struct

from Modules.ExecutableFiles.ELF_data import ELFData, ELFTableHendler


class ELFReader:
    data: ELFData

    def __init__(self, data: ELFData, file):
        self.data = data
        self.file = file

    def program_header_table_read(self):
        table_hendler_seek = self.data.e_end_load_rectord.get("e_phoff")
        if table_hendler_seek == 0:
            return
        else:
            print(self.data.e_middle_load_record.get("e_phnum"))
            for inc in range(self.data.e_middle_load_record.get("e_phnum")):
                table_hendler = ELFTableHendler()

                if self.data.bit_class == 32:
                    element_table_size = 32
                else:  # self.data.bit_class == 64
                    element_table_size = 56

                self.file.seek(table_hendler_seek)
                element_table = self.file.read(element_table_size)
                self.program_header_table_init(element_table, table_hendler)

    def program_header_table_init(self, element_table: bytes, table_hendler: ELFTableHendler):
        if self.data.bit_class == 32:
            hendler_format = "l7i"
            hendler_keys = ["p_type", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_flags", "p_align"]
        else:  # self.data.bit_class == 64
            hendler_format = "li6q"
            hendler_keys = ["p_type", "p_flags", "p_offset", "p_vaddr", "p_paddr", "p_filesz", "p_memsz", "p_align"]

        struct_hendler = struct.unpack(hendler_format, element_table)
        # for

    def e_load_init(self, e_load: bytes):

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
            self.data.e_end_load_rectord.update({elf_e_end[inc]: struct_elf[inc]})

        logging.debug(str(self.data))
