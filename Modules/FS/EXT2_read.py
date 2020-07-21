class EXT2Data:
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
    # s_state = 0                      # 58  2
    # s_errors = 0                     # 60  2
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

    bg_block_bitmap = 0                # 0   4
    bg_inode_bitmap = 0                # 4   4
    bg_inode_table = 0                 # 8   4
    # bg_free_blocks_count = 0           # 12  2
    # bg_free_inodes_count = 0           # 14  2
    # bg_used_dirs_count = 0             # 16  2
    # bg_pad = 0                         # 18  2
    # bg_reserved = 0                    # 20  12


class EXT2Reader:
    error = ""

    def __init__(self, data: EXT2Data):
        print(dir(data))

    def superblockc_read(self, data: EXT2Data, file):
        file.seek(1024)
        superblock = file.read(1024).hex()
        self.super_block_initilaiz(data, superblock)
        if data.s_magic != "EF53":
            self.error = "Файловая система не является EXT2"
            exit()

    def table_descriptor_block(self, file):
        table_descriptor = file.read(32)

    def table_descriptor_block_init(self):
        bg_block_bitmap = 0  # 0   4
        bg_inode_bitmap = 0  # 4   4
        bg_inode_table = 0  # 8   4

    def super_block_initilaiz(self, data: EXT2Data, superblock: str):
        data.s_inodes_count = superblock[0:8]  # 0   4
        data.s_blocks_count = superblock[8:16]  # 4   4
        data.s_free_blocks_count = superblock[24:32]  # 12  4
        data.s_free_inodes_count = superblock[32:40]  # 16  4
        data.s_first_data_block = superblock[40:48]  # 20  4
        data.s_log_block_size = superblock[48:56]  # 24  4
        data.s_blocks_per_group = superblock[64:72]  # 32  4
        data.s_inodes_per_group = superblock[80:88]  # 40  4

        data.s_magic = superblock[112:116]  # 56  2
        data.s_first_ino = superblock[168:176]  # 84  4
        data.s_inode_size = superblock[176:180]  # 88  2


if __name__ == '__main__':
    data = EXT2Data()
    p = EXT2Reader(data)