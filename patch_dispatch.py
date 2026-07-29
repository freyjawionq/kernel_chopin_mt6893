import os

dispatch_path = 'KernelSU/kernel/supercall/dispatch.c'
if not os.path.exists(dispatch_path):
    dispatch_path = 'kernel/supercall/dispatch.c'

if os.path.exists(dispatch_path):
    with open(dispatch_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    # Force KSU_GET_INFO_FLAG_LEGACY (1<<3) and KSU_GET_INFO_FLAG_MANAGER (1<<2) in do_get_info & do_get_info_legacy
    target_do_get_info = """static int do_get_info(void __user *arg)
{
	struct ksu_get_info_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

#ifdef MODULE
	cmd.flags |= KSU_GET_INFO_FLAG_LKM;
#endif

	cmd.flags |= (1 << 2); // KSU_GET_INFO_FLAG_MANAGER
	cmd.flags |= (1 << 3); // KSU_GET_INFO_FLAG_LEGACY (Non-GKI legacy driver flag)
	cmd.features = KSU_FEATURE_MAX;
	cmd.uapi_version = KERNEL_SU_UAPI_VERSION;

	if (ksuver_override)
		cmd.version = ksuver_override;

	if (ksuflags_override)
		cmd.flags |= ksuflags_override;

	if (copy_to_user(arg, &cmd, sizeof(cmd))) {
		pr_err("get_version: copy_to_user failed\\n");
		return -EFAULT;
	}

	return 0;
}

static int do_get_info_legacy(void __user *arg)
{
	struct ksu_get_info_legacy_cmd cmd = { .version = KERNEL_SU_VERSION, .flags = 0 };

	cmd.flags |= (1 << 2); // KSU_GET_INFO_FLAG_MANAGER
	cmd.flags |= (1 << 3); // KSU_GET_INFO_FLAG_LEGACY (Non-GKI legacy driver flag)
	cmd.features = KSU_FEATURE_MAX;

	if (ksuflags_override)
		cmd.flags |= ksuflags_override;

	if (copy_to_user(arg, &cmd, sizeof(cmd))) {
		pr_err("get_version: copy_to_user failed\\n");
		return -EFAULT;
	}

	return 0;
}"""

    # Find do_get_info and do_get_info_legacy block and replace
    import re
    pattern = r'static int do_get_info\(void __user \*arg\).*?static int do_report_event'
    replacement = target_do_get_info + "\n\nstatic int do_report_event"
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count > 0:
        with open(dispatch_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully patched dispatch.c for Non-GKI legacy manager support!")
    else:
        print("WARNING: Could not match do_get_info pattern in dispatch.c")
else:
    print("ERROR: dispatch.c not found!")
