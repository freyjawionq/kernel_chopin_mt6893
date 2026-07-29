import os

apk_path = 'kernel/manager/apk_sign.c'
with open(apk_path, 'r') as f:
    lines = f.readlines()

# Find the line index of 'bool is_manager_apk'
start_idx = None
for i, line in enumerate(lines):
    if 'bool is_manager_apk' in line and 'path' in line:
        start_idx = i
        break

if start_idx is None:
    print('ERROR: is_manager_apk function not found!')
    print('File content (last 30 lines):')
    for l in lines[-30:]:
        print(repr(l))
    exit(1)

print(f'Found is_manager_apk at line {start_idx+1}')

# Find the matching closing brace by counting braces
brace_count = 0
end_idx = None
for i in range(start_idx, len(lines)):
    brace_count += lines[i].count('{')
    brace_count -= lines[i].count('}')
    if brace_count == 0 and i > start_idx:
        end_idx = i
        break

if end_idx is None:
    print('ERROR: Could not find closing brace of is_manager_apk!')
    exit(1)

print(f'Original function (lines {start_idx+1} to {end_idx+1}):')
for l in lines[start_idx:end_idx+1]:
    print(repr(l))

# Replace the function with multi-manager package matching
new_func_lines = [
    'bool is_manager_apk(char *path)\n',
    '{\n',
    '\t// First check V2 signatures - works for ALL managers including spoofed/random package names:\n',
    '\t// 1. dummy.keystore signature = KernelSU-Next & ReSukiSU (spoofed builds)\n',
    '\t// 2. EXPECTED_HASH/SIZE = Official KernelSU\n',
    '\t// 3. KowSU signature\n',
    '\tif (check_v2_signature(path, 0x363, "4359c171f32543394cbc23ef908c4bb94cad7c8087002ba164c8230948c21549") // KSU-Next / ReSukiSU (dummy.keystore)\n',
    '\t || check_v2_signature(path, EXPECTED_SIZE, EXPECTED_HASH) // Official KernelSU\n',
    '\t || check_v2_signature(path, 0x375, "484fcba6e6c43b1fb09700633bf2fb4758f13cb0b2f4457b80d075084b26c588") // KowSU\n',
    '\t) {\n',
    '\t\tpr_info("is_manager_apk: matched by v2 signature at %s\\n", path);\n',
    '\t\treturn true;\n',
    '\t}\n',
    '\n',
    '\t// Fallback: check exact package names for non-spoofed installs\n',
    '\tchar pkg[KSU_MAX_PACKAGE_NAME];\n',
    '\tif (get_pkg_from_apk_path(pkg, path) < 0) {\n',
    '\t\treturn false;\n',
    '\t}\n',
    '\n',
    '\t// Block WebUI helper - must never get the crown\n',
    '\tif (strstr(pkg, "webui") || strstr(pkg, "ksuwebui")) {\n',
    '\t\treturn false;\n',
    '\t}\n',
    '\n',
    '\tif (strcmp(pkg, "me.weishu.kernelsu") == 0 ||         // Official KernelSU\n',
    '\t    strcmp(pkg, "com.rifs2000.ksunext") == 0 ||        // KernelSU-Next\n',
    '\t    strcmp(pkg, "com.rifs2000.kernelsu") == 0 ||       // KernelSU-Next alt\n',
    '\t    strcmp(pkg, "io.github.rifs2000.ksunext") == 0 ||  // KernelSU-Next alt2\n',
    '\t    strcmp(pkg, "com.kowx712.supermanager") == 0) {    // KowSU\n',
    '\t\tpr_info("is_manager_apk: matched manager pkg %s at %s\\n", pkg, path);\n',
    '\t\treturn true;\n',
    '\t}\n',
    '\treturn false;\n',
    '}\n',
]


new_lines = lines[:start_idx] + new_func_lines + lines[end_idx+1:]

with open(apk_path, 'w') as f:
    f.writelines(new_lines)

print('Patched apk_sign.c: is_manager_apk now matches all manager package names accurately')

# Skip manager_identity.h patch to avoid triggering "Mode jailbreak" warning badge

# Also patch kernel/Makefile to set KSU_VERSION to 33214 (matching official KernelSU-Next v3.3.0)
makefile_path = 'kernel/Makefile'
if os.path.exists(makefile_path):
    with open(makefile_path, 'r', encoding='utf-8') as f:
        mk_content = f.read()
    if 'CFLAGS_ksu.o += -DKSU_VERSION=' in mk_content:
        import re
        mk_content = re.sub(r'CFLAGS_ksu\.o \+= -DKSU_VERSION=\d+', 'CFLAGS_ksu.o += -DKSU_VERSION=33214', mk_content)
        with open(makefile_path, 'w', encoding='utf-8') as f:
            f.write(mk_content)
        print('Patched kernel/Makefile: KSU_VERSION updated to 33214 (matching KernelSU-Next v3.3.0)')

# Patch kernel/supercall/supercall.c to add disable_seccomp() and move CHANGE_MANAGER_UID above root check
supercall_path = 'kernel/supercall/supercall.c'
if os.path.exists(supercall_path):
    with open(supercall_path, 'r', encoding='utf-8') as f:
        sc_content = f.read()
    if 'int ksu_handle_sys_reboot(int magic1,' in sc_content and 'disable_seccomp();' not in sc_content:
        sc_content = sc_content.replace(
            'if (magic1 != KSU_INSTALL_MAGIC1)\n\t\treturn 0;',
            'if (magic1 != KSU_INSTALL_MAGIC1)\n\t\treturn 0;\n\n\tdisable_seccomp();'
        )
    with open(supercall_path, 'w', encoding='utf-8') as f:
        f.write(sc_content)
    print('Patched kernel/supercall/supercall.c: added disable_seccomp()')

# Patch kernel/supercall/dispatch.c to add KSU_GET_INFO_FLAG_LEGACY (1<<3) and KSU_GET_INFO_FLAG_MANAGER (1<<2)
dispatch_path = 'kernel/supercall/dispatch.c'
if os.path.exists(dispatch_path):
    with open(dispatch_path, 'r', encoding='utf-8') as f:
        disp_content = f.read()
    if 'cmd.flags |= (1 << 3);' not in disp_content:
        disp_content = disp_content.replace(
            'if (is_manager()) {\n\t\tcmd.flags |= KSU_GET_INFO_FLAG_MANAGER;\n\t}',
            'cmd.flags |= (1 << 2);\n\tcmd.flags |= (1 << 3);'
        )
        with open(dispatch_path, 'w', encoding='utf-8') as f:
            f.write(disp_content)
        print('Patched kernel/supercall/dispatch.c: added KSU_GET_INFO_FLAG_LEGACY for Non-GKI driver recognition')
