Linux kernel release 4.x <http://kernel.org/>
===========================================

These are the release notes for the Linux kernel source code for Xiaomi Chopin (POCO X3 GT / Redmi Note 10 Pro 5G - MT6893).

WHAT IS THE LINUX KERNEL?
-------------------------

The Linux kernel is an open-source Unix-like operating system kernel originally created by Linus Torvalds in 1991.

DOCUMENTATION
-------------

The Documentation/ directory contains extensive documentation for the Linux kernel.

COMPILING THE KERNEL
--------------------

To compile the kernel for Xiaomi Chopin:

  export ARCH=arm64
  export SUBARCH=arm64
  make chopin_defconfig
  make -j$(nproc)

TARGET SPECIFICATIONS
---------------------

  Device: Xiaomi POCO X3 GT / Redmi Note 10 Pro 5G (chopin / MT6893)
  Kernel Version: 4.14.357
  Architecture: ARM64 (aarch64)
