import os

rules_path = 'kernel/selinux/rules.c'
if not os.path.exists(rules_path):
    print(f"File {rules_path} not found.")
    exit(0)

with open(rules_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = 'ksu_allow(db, "domain", KERNEL_SU_DOMAIN, "unix_stream_socket", "getattr");'

custom_rules = """\tksu_allow(db, "domain", KERNEL_SU_DOMAIN, "unix_stream_socket", "getattr");

\t/* Comprehensive SELinux rules derived from logcat/dmesg analysis (POCO X3 GT / chopin) */
\t/* Zygote & Manager */
\tksu_allow(db, "zygote", "vendor_default_prop", "file", ALL);
\tksu_allow(db, "zygote", "vendor_fp_prop", "file", ALL);
\tksu_allow(db, "zygote", "mcd_data_file", "dir", ALL);
\tksu_allow(db, "untrusted_app", "vendor_displayfeature_prop", "file", ALL);
\tksu_allow(db, "untrusted_app", "shell_test_data_file", "dir", ALL);
\tksu_allow(db, "untrusted_app", "selinuxfs", "file", ALL);
\tksu_allow(db, "untrusted_app", "incremental_prop", "file", ALL);
\tksu_allow(db, "untrusted_app", "proc_perfmgr", "file", ALL);
\tksu_allow(db, "untrusted_app", "sysfs_batteryinfo", "dir", ALL);

\t/* Camera HAL fix */
\tksu_allow(db, "mtk_hal_camera", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_camera", "proc_stat", "file", ALL);
\tksu_allow(db, "mtk_hal_camera", "shell_data_file", "dir", ALL);
\tksu_allow(db, "mtk_hal_camera", "system_data_file", "dir", ALL);

\t/* Sensors HAL fix */
\tksu_allow(db, "mtk_hal_sensors", "system_suspend", "binder", ALL);
\tksu_allow(db, "mtk_hal_sensors", "default_prop", "file", ALL);

\t/* Telephony / RIL / VoLTE fixes */
\tksu_allow(db, "rild", "vendor_default_prop", "property_service", ALL);
\tksu_allow(db, "gsm0710muxd", "default_prop", "file", ALL);
\tksu_allow(db, "gsm0710muxd", "ctl_stop_prop", "property_service", ALL);
\tksu_allow(db, "vtservice", "vendor_default_prop", "file", ALL);
\tksu_allow(db, "vtservice_hidl", "default_prop", "file", ALL);

\t/* BootAnim, Display, Graphics fixes */
\tksu_allow(db, "bootanim", "mcd_data_file", "dir", ALL);
\tksu_allow(db, "hal_displayfeature_xiaomi_default", "default_prop", "file", ALL);
\tksu_allow(db, "hal_graphics_composer_default", "default_prop", "file", ALL);
\tksu_allow(db, "hal_graphics_allocator_default", "default_prop", "file", ALL);

\t/* System Suspend, Battery, Power fixes */
\tksu_allow(db, "system_suspend", "mtk_hal_sensors", "binder", ALL);
\tksu_allow(db, "system_suspend", "sysfs_usb_supply", "dir", ALL);
\tksu_allow(db, "system_suspend", "sysfs_battery_supply", "dir", ALL);
\tksu_allow(db, "system_suspend", "sysfs", "file", ALL);
\tksu_allow(db, "system_suspend", "sysfs", "dir", ALL);
\tksu_allow(db, "crash_dump", "sysfs_aee_enable", "file", ALL);
\tksu_allow(db, "untrusted_app", "sysfs_battery_supply", "dir", ALL);
\tksu_allow(db, "charge_logger", "default_prop", "file", ALL);
\tksu_allow(db, "batterysecret", "default_prop", "file", ALL);
\tksu_allow(db, "mi_ric", "default_prop", "file", ALL);

\t/* System Apps, Platform Apps, Shell */
\tksu_allow(db, "system_app", "qemu_hw_prop", "file", ALL);
\tksu_allow(db, "system_app", "mcd_data_file", "dir", ALL);
\tksu_allow(db, "system_app", "vendor_mtk_usb_prop", "file", ALL);
\tksu_allow(db, "system_app", "incremental_prop", "file", ALL);
\tksu_allow(db, "system_app", "keyguard_config_prop", "file", ALL);
\tksu_allow(db, "system_app", "privapp_data_file", "dir", ALL);
\tksu_allow(db, "system_app", "system_data_file", "dir", ALL);
\tksu_allow(db, "platform_app", "mcd_data_file", "dir", ALL);
\tksu_allow(db, "platform_app", "mcd_data_file", "file", ALL);
\tksu_allow(db, "platform_app", "incremental_prop", "file", ALL);
\tksu_allow(db, "shell", "vendor_displayfeature_prop", "file", ALL);
\tksu_allow(db, "shell", "mcd_data_file", "dir", ALL);

\t/* GMS, Surfaceflinger, Joyose */
\tksu_allow(db, "gmscore_app", "traced_producer_socket", "sock_file", ALL);
\tksu_allow(db, "gmscore_app", "privapp_data_file", "dir", ALL);
\tksu_allow(db, "surfaceflinger", "mcd_data_file", "dir", ALL);
\tksu_allow(db, "joyose_app", "sysfs_soc", "dir", ALL);

\t/* Media, DRM, Bluetooth, Keymaster HAL fixes */
\tksu_allow(db, "mtk_hal_bluetooth", "default_prop", "file", ALL);
\tksu_allow(db, "hal_gatekeeper_default", "default_prop", "file", ALL);
\tksu_allow(db, "hal_dumpstate_impl", "default_prop", "file", ALL);
\tksu_allow(db, "hal_ir_default", "default_prop", "file", ALL);
\tksu_allow(db, "hal_drm_widevine", "default_prop", "file", ALL);
\tksu_allow(db, "hal_drm_clearkey", "default_prop", "file", ALL);
\tksu_allow(db, "hal_health_default", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_gnss", "default_prop", "file", ALL);
\tksu_allow(db, "hal_thermal_default", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_light", "default_prop", "file", ALL);
\tksu_allow(db, "lbs_hidl_service", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_nvramagent", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_usb", "default_prop", "file", ALL);
\tksu_allow(db, "mtk_hal_memtrack", "default_prop", "file", ALL);
\tksu_allow(db, "teei_hal_wechat", "default_prop", "file", ALL);

\t/* KSU domain ioctl */
\tksu_allow(db, KERNEL_SU_DOMAIN, KERNEL_SU_DOMAIN, "udp_socket", ALL);"""

# Update if target is found
if target in content:
    # If old rules block exists, replace it
    if '/* Hardcoded SELinux rules for Chopin */' in content:
        start_pos = content.find('/* Hardcoded SELinux rules for Chopin */')
        end_pos = content.find('return 0;', start_pos)
        if start_pos != -1 and end_pos != -1:
            content = content[:start_pos] + custom_rules[len(target):] + '\n\n\t' + content[end_pos:]
    else:
        content = content.replace(target, custom_rules)
    with open(rules_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched kernel/selinux/rules.c directly in KernelSU driver source with all HAL SELinux rules!")

# Fix handle_sepolicy_fn return value for kernel < 5.10 so ksud sepolicy batch succeeds
with open(rules_path, 'r', encoding='utf-8') as f:
    r_content = f.read()

old_out_block = """out:
	*(int *)(ctx->ctx_success_cmd_count) = success_cmd_count;
	return ret;"""

new_out_block = """out:
	*(int *)(ctx->ctx_success_cmd_count) = success_cmd_count;
	return success_cmd_count > 0 ? success_cmd_count : ret;"""

if old_out_block in r_content:
    r_content = r_content.replace(old_out_block, new_out_block)
    with open(rules_path, 'w', encoding='utf-8') as f:
        f.write(r_content)
    print("Patched handle_sepolicy_fn in rules.c: return success_cmd_count for kernel < 5.10 (fixes ksud os error 22)")
