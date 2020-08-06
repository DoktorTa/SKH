import struct


class ELFData:
    ELF_SIGNATURE = b'\x7fELF'

    ELF_CLASS_NONE = 0
    ELF_CLASS_32 = 1
    ELF_CLASS_64 = 2
    ELF_CLASS_name = ["None", "32", "64"]

    ELF_DATA_NONE = 0
    ELF_DATA_2LSB = 1
    ELF_DATA_2MSB = 2
    ELF_DATA_name = ["None type", "Little endian", "Big endian"]

    EV_NONE = 0
    EV_CURRENT = 1

    ELF_OS_ABI_NONE = 0
    ELF_OS_ABI_HPUX = 1
    ELF_OS_ABI_NETBSD = 2
    ELF_OS_ABI_GNU = 3
    ELF_OS_ABI_SOLARIS = 6
    ELF_OS_ABI_AIX = 7
    ELF_OS_ABI_IRIX = 8
    ELF_OS_ABI_FREEBSD = 9
    ELF_OS_ABI_TRU64 = 10
    ELF_OS_ABI_MODESTO = 11
    ELF_OS_ABI_OPENBSD = 12
    ELF_OS_ABI_OPENVMS = 13
    ELF_OS_ABI_NSK = 14
    ELF_OS_ABI_AROS = 15
    ELF_OS_ABI_FENIXOS = 16
    ELF_OS_ABI_CLOUDABI = 17
    ELF_OS_ABI_OPENVOS = 18
    ELF_OS_ABI_name = ["UNIX System V ABI", "HP-UX", "NetBSD",
                       "Файл использует расширения GNU ELF (GNU/Linux)",
                       "Solaris", "AIX", "IRIX", "FreeBSD", "Tru64 UNIX", "Modesto",
                       "OpenBSD", "OpenVMS", "Non-Stop Kernel", "Amiga Research OS",
                       "FenixOS", "CloudABI", "OpenVOS"]

    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4
    ET_name = ["Неопределённый", "Перемещаемый файл", "Исполняемый файл", "Разделяемый объектный файл", "Core file"]

    EM_NONE = 0  # Неопределено
    EM_386 = 3  # Intel 80386
    EM_PPC = 20  # PowerPC
    EM_PPC64 = 21  # 64-bit PowerPC
    EM_X86_64 = 62  # x86-64

    e_ident = {"ei_mag0": 0,
               "ei_class": 0,
               "ei_data": 0,
               "ei_version": 0,
               "ei_osabi": 0,
               "ei_abiversion": 0,
               "ei_pad": 0}

    e_middle_load_record = {"e_type": 0,  # 2
                            "e_machine": 0,  # Platform # 2
                            "e_version": 0}  # 4

    e_end_load_rectord = {"e_entry": 0,
                         "e_phoff": 0,
                         "e_shoff": 0,
                         "e_flags": 0,
                         "e_ehsize": 0,
                         "e_phentsize": 0,
                         "e_phnum": 0,
                         "e_shentsize": 0,
                         "e_shnum": 0,
                         "e_shstrndx": 0}


class ELFReader:
    data: ELFData

    def __init__(self, data: ELFData):
        self.data = data

    def e_ident_init(self, e_load: bytes):

        elf_e_ident = ["ei_mag0", "ei_class", "ei_data", "ei_version", "ei_osabi", "ei_abiversion",
                       "ei_pad0", "ei_pad1", "ei_pad2", "ei_pad3", "ei_pad4", "ei_pad5", "ei_pad6"]

        e_ident = e_load[:16]
        e_ident_format = "4s12b"
        struct_elf = struct.unpack(e_ident_format, e_ident)
        for inc in range(len(elf_e_ident)):
            self.data.e_ident.update({elf_e_ident[inc]: struct_elf[inc]})

        if self.data.e_ident.get("ei_data") == self.data.ELF_DATA_2LSB:
            byte_order = "<"
        else:  # self.data.e_ident.get("ei_data") == self.data.ELF_DATA_2MSB
            byte_order = ">"

        e_midel = e_load[16:24]
        e_midel_format = byte_order + "2hi"
        struct_elf = struct.unpack(e_midel_format, e_midel)
        elf_e_midle = ["e_type", "e_machine", "e_version"]
        for inc in range(3):
            self.data.e_middle_load_record.update({elf_e_midle[inc]: struct_elf[inc]})

        if self.data.e_ident.get("ei_class") == self.data.ELF_CLASS_32:
            e_end_format = "4i6h"
            last_point = 28
        else:  # self.data.e_ident.get("ei_class") == self.data.ELF_CLASS_64:
            e_end_format = "3qi6h"
            last_point = 40

        e_end = e_load[24:24 + last_point]
        struct_elf = struct.unpack(e_end_format, e_end)
        elf_e_end = ["e_entry", "e_phoff", "e_shoff", "e_flags", "e_ehsize",
                     "e_phentsize", "e_phnum", "e_shentsize", "e_shnum", "e_shstrndx"]
        for inc in range(10):
            self.data.e_end_load_rectord.update({elf_e_end[inc]: struct_elf[inc]})
