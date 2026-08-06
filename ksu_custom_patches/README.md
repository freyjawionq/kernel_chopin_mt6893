# KernelSU Custom Patch Backup & Auto-Apply System

Folder ini berisi seluruh patch custom KernelSU yang telah diuji dan berjalan stabil (termasuk penanganan kompatibilitas manager, signature verification, vmap memory safety, dan ABI compatibility).

## Cara Menggunakan Saat Update KernelSU Ke Versi Terbaru

1. **Update / Timpa Folder KernelSU** dengan kode hulu resmi terbaru di `drivers/kernelsu/`.
2. **Jalankan Pemasangan Patch Otomatis**:
   ```bash
   git am --3way ksu_custom_patches/*.patch
   ```
   Atau jalankan skrip helper:
   ```bash
   bash ksu_custom_patches/apply_patches.sh
   ```
3. Seluruh fitur & perbaikan custom akan terpasang kembali secara otomatis di atas KernelSU terbaru!
