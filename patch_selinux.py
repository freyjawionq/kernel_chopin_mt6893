import os

rules_path = 'kernel/selinux/rules.c'
if not os.path.exists(rules_path):
    print(f"File {rules_path} not found.")
    exit(0)

with open(rules_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'ksu_allow(db, "domain", KERNEL_SU_DOMAIN, "unix_stream_socket", "getattr");'

if target in content and '/* Hardcoded SELinux rules for Chopin */' not in content:
    custom_rules = """\tksu_allow(db, "domain", KERNEL_SU_DOMAIN, "unix_stream_socket", "getattr");

\t/* Hardcoded SELinux rules for Chopin */
\tksu_allow(db, "zygote", "vendor_default_prop", "file", ALL);
\tksu_allow(db, "zygote", "vendor_fp_prop", "file", ALL);
\tksu_allow(db, "zygote", "mcd_data_file", "dir", "search");
\tksu_allow(db, "untrusted_app", "vendor_displayfeature_prop", "file", ALL);
\tksu_allow(db, "untrusted_app", "shell_test_data_file", "dir", "search");
\tksu_allow(db, "untrusted_app", "selinuxfs", "file", ALL);
\tksu_allow(db, "untrusted_app", "incremental_prop", "file", ALL);
\tksu_allow(db, "untrusted_app", "proc_perfmgr", "file", "ioctl");
\tksu_allow(db, "untrusted_app", "sysfs_batteryinfo", "dir", ALL);
\tksu_allow(db, "system_app", "qemu_hw_prop", "file", ALL);
\tksu_allow(db, "system_app", "mcd_data_file", "dir", "search");
\tksu_allow(db, "system_app", "vendor_mtk_usb_prop", "file", ALL);
\tksu_allow(db, "system_app", "incremental_prop", "file", ALL);
\tksu_allow(db, "system_app", "keyguard_config_prop", "file", ALL);
\tksu_allow(db, "system_app", "privapp_data_file", "dir", "search");
\tksu_allow(db, "system_app", "system_data_file", "dir", ALL);
\tksu_allow(db, "platform_app", "mcd_data_file", "dir", "search");
\tksu_allow(db, "shell", "vendor_displayfeature_prop", "file", ALL);
\tksu_allow(db, "shell", "mcd_data_file", "dir", "search");
\tksu_allow(db, "gmscore_app", "traced_producer_socket", "sock_file", "write");
\tksu_allow(db, "gmscore_app", "privapp_data_file", "dir", "search");
\tksu_allow(db, "surfaceflinger", "mcd_data_file", "dir", "search");
\tksu_allow(db, "system_suspend", "sysfs", "dir", ALL);
\tksu_allow(db, "joyose_app", "sysfs_soc", "dir", ALL);
\tksu_allow(db, KERNEL_SU_DOMAIN, KERNEL_SU_DOMAIN, "udp_socket", "ioctl");"""

    content = content.replace(target, custom_rules)
    with open(rules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched kernel/selinux/rules.c directly in KernelSU driver source!")
