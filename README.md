# ⚡ ChenXia Kernel — Xiaomi POCO X3 GT / Redmi Note 10 Pro 5G (Chopin)

A high-performance, feature-packed custom Linux 4.14 kernel for **Xiaomi Chopin (MT6893 / Dimensity 1100)**, engineered for peak responsiveness, advanced root management, and complete Play Integrity stealth.

---

## 🌟 Key Features & Highlights

### 🛡️ KernelSU (backslashxx Downstream 4.14 Non-GKI)
- **Ultra-Fast Symbol Scanner**: Integrated `kallsyms_hunt_for_name` linear memory scanner (`_stext` to `_etext`), dropping boot-time symbol lookup from **18s to 0.25s**.
- **Multi-Manager Support**: Concurrently crowns and supports all installed Manager variants:
  - **KernelSU Next Manager** (`com.rifsxd.ksunext`, `com.rifs2000.ksunext`)
  - **ReSukiSU & SukiSU Manager** (`com.resukisu.manager`, `com.sukisu.manager`)
  - **KowSU Manager** (`com.kowx712.supermanager`)
  - **Official KernelSU Manager** (`me.weishu.kernelsu`)
  - **Spoof / Hidden Managers** (V2 Signature matching via `dummy.keystore`).
- **Dynamic Version Auto-Matching**: Seamless `CHANGE_KSUVER` supercall handling so the driver automatically matches the exact version expected by whichever Manager app is opened (e.g. `33227` for Next, `32565` for KowSU/backslashxx, `12000` for ReSukiSU, `11874` for Official).
- **Clean Production Build**: Removed legacy PR signature warning banners for a clean UI experience.
- **Syscall Table Tampering (`CONFIG_KSU_TAMPER_SYSCALL_TABLE=y`)**: Full sucompat fallback protection for legacy 4.14 syscalls without overhead.

---

### 🔒 Advanced Seccomp & SELinux Stealth
- **GKI 2-Style Active SECCOMP Filter**: Android's Seccomp filter remains **100% ENABLED (Mode 2 / Filtered)** across all processes (including KernelSU Manager and daily apps). Supercall evaluation is handled safely in Ring 0 `__secure_computing` without nuking process Seccomp flags or triggering `SIGSYS (Signal 31)` crashes.
- **Dynamic SELinux Rules**: Auto-granted permissions for `proc_filesystems`, `proc_pid_max`, and init domains to eliminate AVC denials while maintaining `Enforcing` mode security.

---

### 🍃 SusFS v2.x Integration (Optional Build Matrix)
- **Sus-Mount**: Hides root mount points from non-root processes.
- **Sus-Path & KStat**: Hides and spoofs file/folder paths associated with root modules.
- **Open-Redirect & Sus-Map**: Hides memory maps and redirects sensitive file accesses seamlessly.

---

## 🛠️ Build Information

- **Kernel Version**: `4.14.357-ChenXia`
- **Compiler**: `ZyCromerZ AOSP Clang 19.0.0 (LTO Enabled)`
- **Target Device**: `Xiaomi Chopin (POCO X3 GT / Redmi Note 10 Pro 5G - MT6893)`
- **CI/CD Workflow**: GitHub Actions Parallel Matrix (`NonSusFS` & `SusFS` variants in ~10 mins).

---

## 📜 Credits & Acknowledgments

- **backslashxx**: For the downstream 4.14 KernelSU non-GKI hooks, `kallsyms_common.h` fast scanner, and sucompat enhancements.
- **tiann & KernelSU Team**: For the original KernelSU root solution.
- **KernelSU Next & ReSukiSU Teams**: For next-gen KernelSU extensions.
- **ZyCromerZ**: For AOSP Clang toolchain builds.
- **Google & Linux Kernel Developers**.

---

⚠️ **Disclaimer**: *Flashing custom kernels carries inherent risks. Make sure to back up your current `boot.img` before flashing.*
