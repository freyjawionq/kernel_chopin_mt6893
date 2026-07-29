### AnyKernel3 Ramdisk Mod Script
## osm0sis @ xda-developers

### AnyKernel setup
# global properties
properties() { '
kernel.string=deadfvck
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=chopin
device.name2=
device.name3=
device.name4=
device.name5=
supported.versions=
supported.patchlevels=
'; } # end properties

### AnyKernel install
# boot shell variables
BLOCK=/dev/block/by-name/boot;
IS_SLOT_DEVICE=1;
RAMDISK_COMPRESSION=auto;
PATCH_VBMETA_FLAG=auto;

# import functions/variables and setup patching - see for reference (DO NOT REMOVE)
. tools/ak3-core.sh;

# boot install
split_boot; # skip ramdisk unpack
flash_boot; # skip ramdisk repack
## end boot install
