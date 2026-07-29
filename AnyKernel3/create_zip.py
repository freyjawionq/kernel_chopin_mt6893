import zipfile
import os

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == "create_zip.py" or ".git" in root or file.endswith(".zip") or file == "README.md":
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, path)
            ziph.write(file_path, arcname)

if __name__ == "__main__":
    zipf = zipfile.ZipFile('KernelSU-Next-chopin-v7-slim.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
    print("KernelSU-Next-chopin-v7-slim.zip created successfully.")
