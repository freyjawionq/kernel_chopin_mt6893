import os

# 1. Edit kernel/Kconfig
kconfig_path = 'kernel/Kconfig'
if os.path.exists(kconfig_path):
    with open(kconfig_path, 'r', encoding='utf-8') as f:
        kconfig = f.read().replace('\r\n', '\n')
    if 'KSU_SUSFS' not in kconfig:
        susfs_config = """menu "KernelSU - SUSFS"
config KSU_SUSFS
    bool "KernelSU addon - SUSFS"
    depends on KSU
    depends on THREAD_INFO_IN_TASK
    default y
    help
        Patch and Enable SUSFS to kernel with KernelSU.

config KSU_SUSFS_SUS_PATH
    bool "Enable to hide suspicious path (NOT recommended)"
    depends on KSU_SUSFS
    default y
    help
        - Allow hiding the user-defined path and all its sub-paths from various system calls.
        - Includes temp fix for the leaks of app path in /sdcard/Android/data directory.
        - Effective only on zygote spawned user app process.
        - Use with cautious as it may cause performance loss and will be vulnerable to side channel attacks,
          just disable this feature if it doesn't work for you or you don't need it at all.

config KSU_SUSFS_SUS_MOUNT
    bool "Enable to hide suspicious mounts"
    depends on KSU_SUSFS
    default y
    help
        - Allow hiding the user-defined mount paths from /proc/self/[mounts|mountinfo|mountstat].
        - Effective on all processes for hiding mount entries.
        - mnt_id and mnt_group_id of the sus mount will be assigned to a much bigger number to solve the ssue of id not being contiguous.

config KSU_SUSFS_SUS_KSTAT
    bool "Enable to spoof suspicious kstat"
    depends on KSU_SUSFS
    default y
    help
        - Allow spoofing the kstat of user-defined file/directory.
        - Effective only on zygote spawned user app process.

config KSU_SUSFS_TRY_UMOUNT
	bool "Enable to use ksu's try_umount"
	depends on KSU_SUSFS
	default y
	help
		- Allow using try_umount to umount other user-defined mount paths prior to ksu's default umount paths.
		- Effective only on zygote spawned umounted user app process.

config KSU_SUSFS_SPOOF_UNAME
    bool "Enable to spoof uname"
    depends on KSU_SUSFS
    default y
    help
        - Allow spoofing the string returned by uname syscall to user-defined string.
        - Effective on all processes.

config KSU_SUSFS_ENABLE_LOG
    bool "Enable logging susfs log to kernel"
    depends on KSU_SUSFS
    default y
    help
        - Allow logging susfs log to kernel, uncheck it to completely disable all susfs log.

config KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS
    bool "Enable to automatically hide ksu and susfs symbols from /proc/kallsyms"
    depends on KSU_SUSFS
    default y
    help
        - Automatically hide ksu and susfs symbols from '/proc/kallsyms'.
        - Effective on all processes.

config KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG
    bool "Enable to spoof /proc/bootconfig (gki) or /proc/cmdline (non-gki)"
    depends on KSU_SUSFS
    default y
    help
        - Spoof the output of /proc/bootconfig (gki) or /proc/cmdline (non-gki) with a user-defined file.
        - Effective on all processes.

config KSU_SUSFS_OPEN_REDIRECT
    bool "Enable to redirect a path to be opened with another path (experimental)"
    depends on KSU_SUSFS
    default y
    help
        - Allow redirecting a target path to be opened with another user-defined path.
        - Effective only on processes with uid < 2000.
        - Please be reminded that process with open access to the target and redirected path can be detected.

config KSU_SUSFS_SUS_MAP
    bool "Enable to hide some mmapped real file from different proc maps interfaces"
    depends on KSU_SUSFS
    default y
    help
        - Allow hiding mmapped real file from /proc/<pid>/[maps|smaps|smaps_rollup|map_files|mem|pagemap]
        - It does NOT support hiding for anon memory.
        - It does NOT hide any inline hooks or plt hooks cause by the injected library itself.
        - It may not be able to evade detections by apps that implement a good injection detection.
        - Effective only on zygote spawned umounted user app process.

endmenu

endmenu"""
        idx = kconfig.rfind("endmenu")
        if idx != -1:
            kconfig = kconfig[:idx] + susfs_config + kconfig[idx+7:]
        with open(kconfig_path, 'w', encoding='utf-8') as f:
            f.write(kconfig)

# 2. Edit kernel/Makefile
makefile_path = 'kernel/Makefile'
if os.path.exists(makefile_path):
    with open(makefile_path, 'r', encoding='utf-8') as f:
        makefile = f.read().rstrip()
    if 'SUSFS_VERSION' not in makefile:
        susfs_makefile = """
## For susfs stuff ##
ifeq ($(shell test -e $(srctree)/fs/susfs.c; echo $$?),0)
$(eval SUSFS_VERSION=$(shell cat $(srctree)/include/linux/susfs.h | grep -E '^#define SUSFS_VERSION' | cut -d' ' -f3 | sed 's/"//g'))
$(info )
$(info -- SUSFS_VERSION: $(SUSFS_VERSION))
else
$(info -- You have not integrated susfs in your kernel yet.)
$(info -- Read: https://gitlab.com/simonpunk/susfs4ksu)
endif

# Keep a new line here!! Because someone may append config
"""
        makefile = makefile + '\n\n' + susfs_makefile
        with open(makefile_path, 'w', encoding='utf-8') as f:
            f.write(makefile)

# 3. Edit kernel/ksu.c
ksuc_path = 'kernel/ksu.c'
if os.path.exists(ksuc_path):
    with open(ksuc_path, 'r', encoding='utf-8') as f:
        ksuc = f.read().replace('\r\n', '\n')
    if 'CONFIG_KSU_SUSFS' not in ksuc:
        target_inc = """#ifdef CONFIG_KSU_SUSFS
#include <linux/susfs.h>
#endif // #ifdef CONFIG_KSU_SUSFS

struct cred* ksu_cred;"""
        ksuc = ksuc.replace('struct cred* ksu_cred;', target_inc)
        
        target_init = """ksu_throne_tracker_init();

#ifdef CONFIG_KSU_SUSFS
    susfs_init();
#endif // #ifdef CONFIG_KSU_SUSFS"""
        ksuc = ksuc.replace('ksu_throne_tracker_init();', target_init)
        with open(ksuc_path, 'w', encoding='utf-8') as f:
            f.write(ksuc)

# 4. Edit kernel/hook/setuid_hook.c to fix compiler error: void function should not return a value
setuid_hook_path = 'kernel/hook/setuid_hook.c'
if os.path.exists(setuid_hook_path):
    with open(setuid_hook_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
    if 'return ksu_handle_umount(new, old);' in content:
        content = content.replace('return ksu_handle_umount(new, old);', 'ksu_handle_umount(new, old);\n    return;')
        with open(setuid_hook_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("Patching completed successfully!")
