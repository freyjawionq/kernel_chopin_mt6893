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
