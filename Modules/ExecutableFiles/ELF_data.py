class ELFHeaderSection:
    """
        Класс который содержит информацию о секциях в elf файле.

        Пожалйуста не используйте значения этих заголовках вне модуля,
         и не добавляете из других компонент,
        вы можете добавить ключ начения напрямую в данный класс.
    """

    sh_type_value = {
        0: ("SHT_NULL", ""),
        1: ("SHT_PROGBITS", ""),
        2: ("SHT_SYMTAB", ""),
        3: ("SHT_STRTAB", ""),
        4: ("SHT_RELA", ""),
        5: ("SHT_HASH", ""),
        6: ("SHT_DYNAMIC", ""),
        7: ("SHT_NOTE ", ""),
        8: ("SHT_NOBITS", ""),
        9: ("SHT_REL", ""),
        10: ("SHT_SHLIB", ""),
        11: ("SHT_DYNSYM", ""),
        14: ("SHT_INIT_ARRAY", ""),
        15: ("SHT_FINI_ARRAY", ""),
        16: ("SHT_PREINIT_ARRAY", ""),
        17: ("SHT_GROUP", ""),
        18: ("SHT_SYMTAB_SHNDX", "")
    }

    program_header_section_fileds = {
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
        self.program_header_section_fileds = {}

    def __str__(self) -> str:
        str_f = f"{self.program_header_section_fileds}"
        return str_f

    @property
    def get_section(self) -> dict:
        """
            Возврашает значения секции.
        """
        return self.program_header_section_fileds


class ELFTableHeader:
    """
        Класс который содержит информацию о заголовках в elf файле.

        Пожалйуста не используйте значения этих заголовках вне модуля,
         и не добавляете из других компанент,
        вы можете добавить ключ начения напрямую в данный класс.
    """

    p_type_value = {
        0: ("PT_NULL", ""),
        1: ("PT_LOAD", ""),
        2: ("PT_DYNAMIC", ""),
        3: ("PT_INTERP", ""),
        4: ("PT_NOTE", ""),
        5: ("PT_SHLIB", ""),
        6: ("PT_PHDR", ""),
        7: ("PT_TLS", "")
    }

    PF_X = 0x1
    PF_W = 0x2
    PF_R = 0x4
    PF_MASKOS = 0x0ff00000
    PF_MASKPROC = 0xf0000000
    PF_name = ["Разрешение на исполнение",
               "Разрешение на запись",
               "Разрешение на чтение"]

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

    @property
    def get_header(self) -> dict:
        """
            Возврашает значения заголовка.
        """
        return self.program_header_fields


class ELFData:
    """
        Класс который содержит информацию о заголовке,
         секциях и заголовках в elf файле.

        Пожалйуста не используйте значения этих заголовках вне модуля,
         и не добавляете из других компонент,
        вы можете добавить ключ начения напрямую в данный класс.
    """

    elf_signature = {b'\x7fELF': ("ELF_SIGNATURE", "")}

    elf_class_value = {
        0: ("ELF_CLASS_NONE", "Unknown bit system"),
        1: ("ELF_CLASS_32", "32 bit system"),
        2: ("ELF_CLASS_64", "64 bit system")
    }

    elf_data_value = {
        0: ("ELF_DATA_NONE", "Unknown endian"),
        1: ("ELF_DATA_2LSB", "Little endian"),
        2: ("ELF_DATA_2MSB", "Big endian")
    }

    ev_version_value = {
        0: ("EV_NONE", ""),
        1: ("EV_CURRENT", "")
    }

    elf_os_abi_value = {
        0: ("ELF_OS_ABI_NONE", ""),
        1: ("ELF_OS_ABI_HPUX", ""),
        2: ("ELF_OS_ABI_NETBSD", ""),
        3: ("ELF_OS_ABI_GNU", ""),
        6: ("ELF_OS_ABI_SOLARIS", ""),
        7: ("ELF_OS_ABI_AIX", ""),
        8: ("ELF_OS_ABI_IRIX", ""),
        9: ("ELF_OS_ABI_FREEBSD", ""),
        10: ("ELF_OS_ABI_TRU64", ""),
        11: ("ELF_OS_ABI_MODESTO", ""),
        12: ("ELF_OS_ABI_OPENBSD", ""),
        13: ("ELF_OS_ABI_OPENVMS", ""),
        14: ("ELF_OS_ABI_NSK", ""),
        15: ("ELF_OS_ABI_AROS", ""),
        16: ("ELF_OS_ABI_FENIXOS", ""),
        17: ("ELF_OS_ABI_CLOUDABI", ""),
        18: ("ELF_OS_ABI_OPENVOS", "")
    }

    et_value = {
        0: ("ET_NONE", "Неопределённый"),
        1: ("ET_REL", "Перемещаемый файл"),
        2: ("ET_EXEC", "Исполняемый файл"),
        3: ("ET_DYN", "Разделяемый объектный файл"),
        4: ("ET_CORE", "Core file")
    }

    em_value = {
        0: ("EM_NONE", "Неопределено"),
        3: ("EM_386", "Intel 80386"),
        20: ("EM_PPC", "PowerPC"),
        21: ("EM_PPC64", "64-bit PowerPC"),
        62: ("EM_X86_64", "x86-64"),

    }

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
                         "e_phentsize": 0,
                         "e_phnum": 0,
                         "e_shentsize": 0,
                         "e_shnum": 0,
                         "e_shstrndx": 0}

    tables_header_records = []
    section_header_records = []

    def __str__(self) -> str:
        str_f = f"\n" \
                f"{self.e_ident}\n" \
                f"{self.e_middle_load_record}\n" \
                f"{self.e_end_load_record}\n"
        return str_f
