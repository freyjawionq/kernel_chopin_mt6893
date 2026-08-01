# NOTE: unity build. single unit.

obj-$(CONFIG_KSU) := ksu.o

CFLAGS_ksu.o += -I$(srctree)/security/selinux -I$(srctree)/security/selinux/include
CFLAGS_ksu.o += -I$(objtree)/security/selinux

KDIR := $(KDIR)
MDIR := $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

$(info -- KDIR: $(KDIR))
$(info -- MDIR: $(MDIR))

# driver version matches backslashxx KernelSU baseline (32579)
CFLAGS_ksu.o += -DKSU_VERSION=32579
CFLAGS_ksu.o += -DKSU_COMPAT_USE_SELINUX_STATE=1
CFLAGS_ksu.o += -Wno-error -Wno-strict-prototypes -Wno-old-style-definition -Wno-incompatible-pointer-types

ifndef KSU_EXPECTED_SIZE
KSU_EXPECTED_SIZE := 0x033b
endif

ifndef KSU_EXPECTED_HASH
KSU_EXPECTED_HASH := c371061b19d8c7d7d6133c6a9bafe198fa944e50c1b31c9d8daa8d7f1fc2d2d6
endif

ifdef KSU_MANAGER_PACKAGE
CFLAGS_ksu.o += -DKSU_MANAGER_PACKAGE=\"$(KSU_MANAGER_PACKAGE)\"
$(info -- KernelSU Manager package name: $(KSU_MANAGER_PACKAGE))
endif

$(info -- KernelSU Manager signature size: $(KSU_EXPECTED_SIZE))
$(info -- KernelSU Manager signature hash: $(KSU_EXPECTED_HASH))

CFLAGS_ksu.o += -DEXPECTED_SIZE=$(KSU_EXPECTED_SIZE)
CFLAGS_ksu.o += -DEXPECTED_HASH=\"$(KSU_EXPECTED_HASH)\"

# uncommon, but wont hurt, check for 3-arg security_add_hooks
ifeq ($(shell grep -A1 "void security_add_hooks" $(srctree)/include/linux/lsm_hooks.h 2>/dev/null | grep -q lsm 2>/dev/null; echo $$?),0)
$(info -- KernelSU/compat: security_add_hooks v2 found!)
CFLAGS_ksu.o += -DKSU_COMPAT_SECURITY_ADD_HOOKS_V2
endif
