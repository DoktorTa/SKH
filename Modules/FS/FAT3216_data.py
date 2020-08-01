class FATData:
    FAT_version = ''
    # bpb_eb = 0                         # 0    3
    # bpb_os_or_fs_identifier = 0        # 3    11
    bpb_byte_in_sector = 0

    # Это значение должно быть степенью 2, которая больше 0
    bpb_sector_in_claster = 0

    # Для томов FAT12 и FAT16 это значение никогда не должно быть
    # ничем иным, чем 1. Для томов FAT32 это значение обычно равно 32.
    bpb_reversed_sector = 0
    bpb_num_fat = 0

    # Для томов FAT12 и FAT16 это значение всегда должно указывать счетчик,
    # который при умножении на 32 приводит к четному кратному
    # BPB_BytsPerSec. Для FAT32 поле всегда 0
    bpb_root_ent_cnt = 0

    # Если это 0, то BPB_TotSec32 должен быть ненулевым.
    # Для томов FAT32 это поле должно быть 0.
    # Для томов FAT12 и FAT16 это поле содержит количество секторов,
    # а BPB_TotSec32 равно 0, если общее количество секторов меньше 0x10000
    bpb_total_sector_16_12 = 0

    # bpb_media = 0

    # Это поле является 16-разрядным счетчиком FAT12 / FAT16 секторов,
    # занятых ONE FAT. На томах FAT32 это поле должно быть 0,
    # а BPB_FATSz32 содержит счетчик размеров FAT.
    bpb_fat_size_16_12 = 0

    # bpb_sector_on_track = 0
    # bpb_num_heads = 0
    # bpb_hidden_sector = 0

    # 32-разрядное общее количество секторов в томе.
    # Это количество включает в себя количество всех секторов
    # во всех четырех областях тома. Если это 0, то BPB_TotSec16
    # должен быть ненулевым.
    # Для томов FAT32 это поле должно быть ненулевым.
    # Для томов FAT12 / FAT16 это поле содержит количество секторов,
    # если BPB_TotSec16 равно 0 (количество больше или равно 0x10000).
    bpb_total_sector_32 = 0

    # Это поле является 32-битным счетчиком FAT32 секторов,
    # занятых ONE FAT.
    bpb_fat_size_32 = 0

    # v FAT16 load dlc v----------------------------------------------------------------------------------------------------
    # bs_num_drv = load_sector_h[72:74]
    # Код, который форматирует тома FAT,
    # должен всегда устанавливать этот байт в 0.
    # bs_reversed_1 = load_sector_h[74:76]
    # Указывает на наличие следующих трех полей в загрузочном секторе.
    # bs_boot_signature = load_sector_h[76:78]
    # bs_serian_num_tom = load_sector_h[78:86]
    # bs_mets_tom = load_sector_h[86:108]
    # Этой Иуде неверит даже Microsoft
    # bs_fs_t = load_sector_h[108:124]
    # ^ FAT16 load dlc ^----------------------------------------------------------------------------------------------------

    # v FAT16 load dlc v----------------------------------------------------------------------------------------------------
    # Биты 0-3 - количество активных FAT на основе нуля.
    # Действителен только если зеркальное отображение отключено.
    # Биты 4-6 - зарезервированы.
    # Бит 7 - 0 означает, что FAT отражается во все FAT .
    # - 1 означает, что активен только один FAT это ссылка на биты 0-3.
    # Биты 8-15 - зарезервированы.
    # bpb_ext_flags = load_sector_h[80:84]
    # bpb_fs_ver = load_sector_h[84:88]

    # Это номер кластера первого кластера корневого каталога, обычно 2.
    bpb_root_claster = 0

    # Номер сектора структуры FSINFO в зарезервированной области FAT32.
    # bpb_fs_info = load_sector_h[96:100]
    # Если не ноль, указывает номер сектора в зарезервированной области
    # тома копии загрузочной записи.
    # bpb_bk_boot_sector = load_sector_h[100:104]
    # bpb_reversed = load_sector_h[104:128]
    # !!!Далее то же что и в FAT12 и FAT16, но с другим смешением!!!
    # bs_num_drv = load_sector_h[128:130]
    # Код, который форматирует тома FAT,
    # должен всегда устанавливать этот байт в 0.
    # bs_reversed_1 = load_sector_h[130:132]
    # Указывает на наличие следующих трех полей в загрузочном секторе.
    # bs_boot_signature = load_sector_h[132:134]
    # bs_serian_num_tom = load_sector_h[134:142]
    # bs_mets_tom = load_sector_h[142:164]
    # Этой Иуде неверит даже Microsoft
    # bs_fs_t = load_sector_h[164:180]
    # ^ FAT32 load dlc ^----------------------------------------------------------------------------------------------------

    def __str__(self):
        str_f = f"\n" \
                f"FAT version:        {self.FAT_version}" \
                f"Bytes in sectors:   {self.bpb_byte_in_sector}\n" \
                f"Sector per claster: {self.bpb_sector_in_claster}\n" \
                f"Reversed sectors:   {self.bpb_reversed_sector}\n" \
                f"Nums fat table:     {self.bpb_num_fat}\n" \
                f"Root ent cnt:       {self.bpb_root_ent_cnt}\n" \
                f"Total sectors 1:    {self.bpb_total_sector_16_12}\n" \
                f"Total sectors 2:    {self.bpb_total_sector_32}\n" \
                f"FAT size 12, 16:    {self.bpb_fat_size_16_12}\n" \
                f"FAT size 32:        {self.bpb_fat_size_32}\n" \
                f"First root claster: {self.bpb_root_claster}\n"
        return str_f


class FATLongName:
    l_element_ord = 0
    l_element_name_1 = 0
    # l_element_attr = element_h[22:24]
    # l_element_type = element_h[24:26]
    # l_element_chksum = element_h[26:28]
    l_element_name_2 = 0
    # l_element_fts_claster_lo = element_h[52:56]
    l_element_name_3 = 0

    l_element_name = ""

    def __str__(self):
        str_f = f"\n" \
                f"Element\n" \
                f"Ord:                 {self.l_element_ord}\n" \
                f"Name 1:              {self.l_element_name_1}\n" \
                f"Name 2:              {self.l_element_name_2}\n" \
                f"Name 3:              {self.l_element_name_3}\n" \
                f"Name:                {self.l_element_name}\n"
        return str_f


class FATDirectory:
    element_name = 0
    element_attr = 0
    # Зарезервировано для использования Windows NT
    # element_NT = element_h[24:26]
    # element_ctr_time_tenth = element_h[26:28]
    # element_ctr_time = element_h[28:32]
    element_ctr_data = 0
    # element_lst_acc_date = element_h[36:40]
    element_fst_claster_hi = 0
    # element_wrt_time = element_h[44:48]
    # element_wrt_data = element_h[48:52]
    element_fst_claster_lo = 0
    element_size = 0

    element_fst_claster = 0

    def __str__(self):
        str_f = f"\n" \
                f"Element\n" \
                f"Name:                {self.element_name}\n" \
                f"Attributes:          {self.element_attr}\n" \
                f"Creating data:       {self.element_ctr_data}\n" \
                f"First claster high:  {self.element_fst_claster_hi}\n" \
                f"First claster low:   {self.element_fst_claster_lo}\n" \
                f"Size:                {self.element_size}\n" \
                f"First claster:       {self.element_fst_claster}"
        return str_f
