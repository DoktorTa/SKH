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

    e_ident = {"ei_mag0": 0,
               "ei_class": 0,
               "ei_data": 0,
               "ei_version": 0,
               "ei_osabi": 0,
               "ei_abiversion": 0,
               "ei_pad": 0}


class ELFReader:
    data: ELFData

    def __init__(self, data: ELFData):
        self.data = data

    def e_ident_init(self, e_ident: bytes):

        elf_e_ident = ["ei_mag0", "ei_class", "ei_data", "ei_version",
                       "ei_osabi", "ei_abiversion", "ei_pad"]
        e_ident_format = "4s6b"
        struct_elf = struct.unpack(e_ident_format, e_ident)
        for inc in range(len(elf_e_ident)):
            self.data.e_ident.update({elf_e_ident[inc]: struct_elf[inc]})
