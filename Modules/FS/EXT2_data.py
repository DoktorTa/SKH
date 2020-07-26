class EXT2Data:
    SIZE_BLOCK_IN_BLOCK_TABLE = 4

    s_inodes_count = 0               # 0   4
    s_blocks_count = 0               # 4   4
    # s_r_blocks_count = 0             # 8   4
    s_free_blocks_count = 0          # 12  4
    s_free_inodes_count = 0          # 16  4
    s_first_data_block = 0           # 20  4
    s_log_block_size = 0             # 24  4
    # s_log_frag_size = 0              # 28  4
    s_blocks_per_group = 0           # 32  4
    # s_frags_per_group = 0            # 36  4
    s_inodes_per_group = 0           # 40  4
    # s_mtime = 0                      # 44  4
    # s_wtime = 0                      # 48  4

    # s_mnt_count = 0                  # 52  2
    # s_max_mnt_count = 0              # 54  2
    s_magic = 0                      # 56  2
    s_state = 0                      # 58  2
    s_errors = 0                     # 60  2
    # s_minor_rev_level = 0            # 62  2

    # s_lastcheck = 0                  # 64  4
    # s_checkinterval = 0              # 68  4
    # s_creator_os = 0                 # 72  4
    # s_rev_level = 0                  # 76  4
    # s_def_resuid = 0                 # 80  2
    # s_def_resgid = 0                 # 82  2

    # -- EXT2_DYNAMIC_REV Specific --
    s_first_ino = 0                  # 84  4
    s_inode_size = 0                 # 88  2
    # s_block_group_nr = 0             # 90  2
    # s_feature_compat = 0             # 92  4
    # s_feature_incompat = 0           # 96  4
    # s_feature_ro_compat = 0          # 100 4
    # s_uuid = 0                       # 104 16
    # s_volume_name = 0                # 120 16
    # s_last_mounted = 0               # 136 64
    # s_algo_bitmap = 0                # 200 4

    # -- Performance Hints --
    # s_prealloc_blocks = 0            # 204 1
    # s_prealloc_dir_blocks = 0        # 205 1
    # (alignment) = 0                  # 206 2

    # -- Journaling Support --
    # s_journal_uuid = 0               # 208 16
    # s_journal_inum = 0               # 224 4
    # s_journal_dev = 0                # 228 4
    # s_last_orphan = 0                # 232 4

    # -- Directory Indexing Support --
    # s_hash_seed = 0                  # 236 4 x 4
    # s_def_hash_version = 0           # 252 1
    # 253 3 padding - reserved for future expansion

    # -- Otheroptions --
    # s_default_mount_options = 0      # 256 4
    # s_first_meta_bg = 0              # 260 4
    # 264 760 Unused - reserved for future revisions

    block_size = 0                     # 1, 2, 4, 8 КБ
    group_count = 0
    group_description_table = []       # Содержит в себе дескрипторы

    def __str__(self):
        str_f = f"\n" \
                f"Inodes count:      {self.s_inodes_count} \n" \
                f"Block count:       {self.s_blocks_count} \n" \
                f"Free block count:  {self.s_free_blocks_count} \n" \
                f"Free inodes count: {self.s_free_inodes_count} \n" \
                f"First data block:  {self.s_first_data_block} \n" \
                f"Log block size:    {self.s_log_block_size} \n" \
                f"Block per group:   {self.s_blocks_per_group} \n" \
                f"Inodes per group:  {self.s_inodes_per_group} \n" \
                f"Magic, 'EF53':     {self.s_magic} \n" \
                f"State:             {self.s_state} \n" \
                f"Errors:            {self.s_errors} \n" \
                f"-- EXT2_DYNAMIC_REV Specific --\n" \
                f"First inodes:      {self.s_first_ino} \n" \
                f"Inode size:        {self.s_inode_size} \n\n" \
                f"BLOCK SIZE:        {self.block_size}\n" \
                f"Group count:       {self.group_count}\n\n"
        return str_f


class EXT2DescriptorGroup:
    num_descriptor = 0
    # -- Table discriptor --
    bg_block_bitmap = 0                # 0   4
    bg_inode_bitmap = 0                # 4   4
    bg_inode_table = 0                 # 8   4
    # bg_free_blocks_count = 0           # 12  2
    # bg_free_inodes_count = 0           # 14  2
    # bg_used_dirs_count = 0             # 16  2
    # bg_pad = 0                         # 18  2
    # bg_reserved = 0                    # 20  12

    start_seek = 0
    end_seek = 0

    def __init__(self, num_descriptor):
        self.num_descriptor = num_descriptor

    def __str__(self):
        str_f = f"\n" \
                f"Num descriptor:    {self.num_descriptor}\n" \
                f"Start seek desc:   {self.start_seek}\n" \
                f"End seek desc:     {self.end_seek}\n\n" \
                f"-- Table discriptor --\n" \
                f"Block bitmap:      {self.bg_block_bitmap} \n" \
                f"Inode bitmap:      {self.bg_inode_bitmap} \n" \
                f"Inode table:       {self.bg_inode_table}"
        return str_f


class EXT2Inode:
    FIRST_INDIRECT_BLOCK = 12
    FIRST_SINGLE_INDIRECT_BLOCK = 13
    FIRST_DOUBLE_INDIRECT_BLOCK = 14
    FIRST_TRIPLE_INDIRECT_BLOCK = 15

    i_mode = 0                         # 0	    2
    i_uid = 0                          # 2	    2
    i_size = 0                         # 4	    4
    # i_atime = 0                        # 8	    4
    # i_ctime = 0                        # 12	    4
    # i_mtime = 0                        # 16	    4
    # i_dtime = 0                        # 20	    4
    i_gid = 0                          # 24	    2
    i_links_count = 0                  # 26	    2
    # i_blocks = 0                       # 28	    4
    i_flags = 0                        # 32	    4
    # i_osd1 = 0                         # 36	    4
    i_block = []                       # 40	    15 х 4
    # i_generation = 0                   # 100	4
    # i_file_acl = 0                     # 104	4
    # i_dir_acl = 0                      # 108	4
    # i_faddr = 0                        # 112	4
    # i_osd2 = 0                         # 116   12

    def __init__(self):
        self.i_block = []
