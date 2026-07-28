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

# Replace the function with a simple 'return true' version
new_func_lines = [
    'bool is_manager_apk(char *path)\n',
    '{\n',
    '\treturn true;\n',
    '}\n',
]

new_lines = lines[:start_idx] + new_func_lines + lines[end_idx+1:]

with open(apk_path, 'w') as f:
    f.writelines(new_lines)

print('Patched apk_sign.c: is_manager_apk now returns true (universal multi-manager support)')

# Also patch manager_identity.h so is_manager() always returns true
identity_path = 'kernel/manager/manager_identity.h'
if os.path.exists(identity_path):
    with open(identity_path, 'r', encoding='utf-8') as f:
        id_content = f.read()
    if 'static inline bool is_manager()' in id_content:
        # Patch is_manager to return true
        id_content = id_content.replace(
            'return unlikely(ksu_manager_appid == current_uid().val % KSU_PER_USER_RANGE);',
            'return true;'
        )
        with open(identity_path, 'w', encoding='utf-8') as f:
            f.write(id_content)
        print('Patched manager_identity.h: is_manager now returns true (universal GREEN status)')

# Also patch kernel/Makefile to set KSU_VERSION to 12431 (matching KernelSU-Next / ReSukiSU / KOWX712 driver code)
makefile_path = 'kernel/Makefile'
if os.path.exists(makefile_path):
    with open(makefile_path, 'r', encoding='utf-8') as f:
        mk_content = f.read()
    if 'CFLAGS_ksu.o += -DKSU_VERSION=' in mk_content:
        import re
        mk_content = re.sub(r'CFLAGS_ksu\.o \+= -DKSU_VERSION=\d+', 'CFLAGS_ksu.o += -DKSU_VERSION=12431', mk_content)
        with open(makefile_path, 'w', encoding='utf-8') as f:
            f.write(mk_content)
        print('Patched kernel/Makefile: KSU_VERSION updated to 12431 (matching KernelSU-Next / ReSukiSU / KOWX712 driver code)')
