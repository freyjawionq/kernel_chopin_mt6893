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

// Input hook stubs for SusFS / KSU
#ifdef CONFIG_KSU
DEFINE_STATIC_KEY_FALSE(ksu_is_input_hook_enabled);
EXPORT_SYMBOL(ksu_is_input_hook_enabled);

int ksu_handle_input_handle_event(unsigned int *type, unsigned int *code, int *value) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_input_handle_event);
#endif

// Fallback stubs when CONFIG_KSU_TAMPER_SYSCALL_TABLE is active and manual hooks are disabled
#if defined(CONFIG_KSU_TAMPER_SYSCALL_TABLE)
bool ksu_su_compat_enabled = true;
EXPORT_SYMBOL(ksu_su_compat_enabled);

int ksu_handle_faccessat(int *dfd, const char __user **filename_user, int *mode, int *__unused_flags) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_faccessat);

int ksu_handle_stat(int *dfd, const char __user **filename_user, int *flags) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_stat);

int ksu_handle_vfs_fstat(int *fd, void *statbuf) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_vfs_fstat);

int ksu_handle_execveat(int *fd, void *filename_ptr, void *argv, void *envp, int *flags) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_execveat);

int ksu_handle_execveat_sucompat(int *fd, void *filename_ptr, void *argv, void *envp, int *flags) {
    return 0;
}
EXPORT_SYMBOL(ksu_handle_execveat_sucompat);

void ksu_handle_setresuid(void *new, void *old) {}
EXPORT_SYMBOL(ksu_handle_setresuid);
#endif
