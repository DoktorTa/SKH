class ELFHendlerSection:
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_INIT_ARRAY = 14
    SHT_FINI_ARRAY = 15
    SHT_PREINIT_ARRAY = 16
    SHT_GROUP = 17
    SHT_SYMTAB_SHNDX = 18

    program_hendler_section_fileds = {
        "sh_name": 0,
        "sh_type": 0,
        "sh_flags": 0,
        "sh_addr": 0,
        "sh_offset": 0,
        "sh_size": 0,
        "sh_link": 0,
        "sh_info": 0,
        "sh_addralign": 0,
        "sh_entsize": 0
    }

    def __init__(self):
        self.program_hendler_section_fileds = {}

    def __str__(self) -> str:
        str_f = f"{self.program_hendler_section_fileds}"
        return str_f


class ELFTableHendler:
    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_TLS = 7

    PF_X = 0x1
    PF_W = 0x2
    PF_R = 0x4
    PF_MASKOS = 0x0ff00000
    PF_MASKPROC = 0xf0000000
    PF_name = ["Разрешение на исполнение", "Разрешение на запись", "Разрешение на чтение"]

    program_header_fields = {
        "p_type": 0,
        "p_flags": 0,
        "p_offset": 0,
        "p_vaddr": 0,
        "p_paddr": 0,
        "p_filesz": 0,
        "p_memsz": 0,
        # "p_flags": 0,
        "p_align": 0
    }

    def __init__(self):
        self.program_header_fields = {}

    def __str__(self):
        str_f = f"{self.program_header_fields}"
        return str_f


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

    byte_order = None
    bit_class = None

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

    e_end_load_record = {"e_entry": 0,
                         "e_phoff": 0,
                         "e_shoff": 0,
                         "e_flags": 0,
                         "e_ehsize": 0,
                         "e_phentsize": 0,  # Я очень недоволен этим значением, его можно принять за константу, лишнее.
                         "e_phnum": 0,
                         "e_shentsize": 0,
                         "e_shnum": 0,
                         "e_shstrndx": 0}

    tables_hendler_records = []
    section_hendler_records = []

    def __str__(self) -> str:
        str_f = f"\n" \
                f"{self.e_ident}\n" \
                f"{self.e_middle_load_record}\n" \
                f"{self.e_end_load_record}\n"
        return str_f
