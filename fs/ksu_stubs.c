#include <linux/jump_label.h>
#include <linux/fs.h>
#include <linux/tracepoint.h>

#ifdef CONFIG_KSU
DEFINE_STATIC_KEY_TRUE(ksu_is_init_rc_hook_enabled);
EXPORT_SYMBOL(ksu_is_init_rc_hook_enabled);

int ksu_handle_sys_read(unsigned int fd) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_sys_read);
#endif

#ifdef CONFIG_KSU
int ksu_handle_devpts(struct inode *inode) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_devpts);
#endif

// MediaTek PPM / SWPM tracepoint stubs to satisfy LTO linker
struct tracepoint __tracepoint_ppm_user_setting;
EXPORT_SYMBOL(__tracepoint_ppm_user_setting);

struct tracepoint __tracepoint_swpm_power;
EXPORT_SYMBOL(__tracepoint_swpm_power);

// susfs_try_umount and susfs_add_try_umount are referenced from setuid_hook.c
// but not implemented in fs/susfs.c in this tree — provide stubs always.
#ifndef CONFIG_KSU_SUSFS_TRY_UMOUNT
void susfs_try_umount(uid_t uid) {}
EXPORT_SYMBOL(susfs_try_umount);

int susfs_add_try_umount(const char *target_path, u32 flags, u8 mode) { return 0; }
EXPORT_SYMBOL(susfs_add_try_umount);
#endif

