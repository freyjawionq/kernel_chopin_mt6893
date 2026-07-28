import re

apk_path = 'kernel/manager/apk_sign.c'
with open(apk_path, 'r') as f:
    content = f.read()

# Replace the entire is_manager_apk function body with 'return true'
new_func = 'bool is_manager_apk(char *path)\n{\n\treturn true;\n}'
content = re.sub(
    r'bool is_manager_apk\(char \*path\)\s*\{[^}]*\}',
    new_func,
    content,
    flags=re.DOTALL
)

with open(apk_path, 'w') as f:
    f.write(content)

print('Patched apk_sign.c: is_manager_apk now returns true')
