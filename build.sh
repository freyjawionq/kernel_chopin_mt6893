#!/bin/bash

function compile() 
{
    source ~/.bashrc && source ~/.profile
    export LC_ALL=C
    export ARCH=arm64
    export LOCALVERSION='-Ciallo~'

    # Support cleaning build
    if [ "$1" = "-c" ] || [ "$1" = "clean" ]; then
        echo "Cleaning out directory..."
        rm -rf out
    fi

    if ! [ -d "out" ]; then
        echo "Kernel OUT Directory Not Found. Making Again"
        mkdir out
    fi

    make O=out ARCH=arm64 chopin_defconfig

    PATH="${PWD}/clang/bin:${PATH}" \
    make -j$(nproc --all) O=out \
                          ARCH=arm64 \
                          CC="clang" \
                          HOSTCC="gcc" \
                          HOSTLD="ld" \
                          CLANG_TRIPLE=aarch64-linux-gnu- \
                          CROSS_COMPILE="${PWD}/clang/bin/aarch64-linux-gnu-" \
                          CROSS_COMPILE_ARM32="${PWD}/clang/bin/arm-linux-gnueabi-" \
                          LD=ld.lld \
                          STRIP=llvm-strip \
                          AS=llvm-as \
                          AR=llvm-ar \
                          NM=llvm-nm \
                          OBJCOPY=llvm-objcopy \
                          OBJDUMP=llvm-objdump \
                          CONFIG_NO_ERROR_ON_MISMATCH=y 2>&1 | tee error.log 

    if [ -f "out/arch/arm64/boot/Image.gz-dtb" ]; then
        echo -e "\nKernel compiled successfully! Zipping up...\n"
        rm -rf AnyKernel3
        git clone -q --depth=1 https://github.com/froyoandroid/AnyKernel3 AnyKernel3
        cp out/arch/arm64/boot/Image.gz-dtb AnyKernel3/

        # Package ST NFC Fix files
        mkdir -p AnyKernel3/ksu_files
        cp /home/afifnaxxwahana3/com.st.android.nfc_extensions.jar AnyKernel3/ksu_files/
        cp /home/afifnaxxwahana3/com.st.android.nfc_extensions.xml AnyKernel3/ksu_files/

        # Append installer script to anykernel.sh
        cat << 'EOF' >> AnyKernel3/anykernel.sh

# Install ST NFC Library
mount -o rw,remount /system_ext || mount -o rw,remount / || true;
if [ -w /system_ext/framework ]; then
  ui_print "System is writable, installing ST NFC library directly...";
  mkdir -p /system_ext/framework;
  mkdir -p /system_ext/etc/permissions;
  cp $AKHOME/ksu_files/com.st.android.nfc_extensions.jar /system_ext/framework/com.st.android.nfc_extensions.jar;
  cp $AKHOME/ksu_files/com.st.android.nfc_extensions.xml /system_ext/etc/permissions/com.st.android.nfc_extensions.xml;
  chmod 644 /system_ext/framework/com.st.android.nfc_extensions.jar;
  chmod 644 /system_ext/etc/permissions/com.st.android.nfc_extensions.xml;
  ui_print "ST NFC library installed directly!";
else
  mount /data || true;
  if [ -d /data/adb/modules ]; then
    ui_print "Magisk/KernelSU detected, creating ST NFC Fix module...";
    MODDIR="/data/adb/modules/st_nfc_fix";
    mkdir -p $MODDIR/system/system_ext/framework;
    mkdir -p $MODDIR/system/system_ext/etc/permissions;
    
    # Create module.prop
    echo "id=st_nfc_fix" > $MODDIR/module.prop;
    echo "name=ST NFC Extension Fix" >> $MODDIR/module.prop;
    echo "version=v1.0" >> $MODDIR/module.prop;
    echo "versionCode=1" >> $MODDIR/module.prop;
    echo "author=Antigravity" >> $MODDIR/module.prop;
    echo "description=Injects ST NFC extensions library (jar & xml) to system_ext." >> $MODDIR/module.prop;
    
    # Copy files
    cp $AKHOME/ksu_files/com.st.android.nfc_extensions.jar $MODDIR/system/system_ext/framework/com.st.android.nfc_extensions.jar;
    cp $AKHOME/ksu_files/com.st.android.nfc_extensions.xml $MODDIR/system/system_ext/etc/permissions/com.st.android.nfc_extensions.xml;
    
    chmod -R 755 $MODDIR/system/system_ext;
    chmod 644 $MODDIR/module.prop;
    chmod 644 $MODDIR/system/system_ext/framework/com.st.android.nfc_extensions.jar;
    chmod 644 $MODDIR/system/system_ext/etc/permissions/com.st.android.nfc_extensions.xml;
    ui_print "ST NFC Fix module created successfully!";
  else
    ui_print "Warning: System is read-only and no Magisk/KernelSU detected! NFC extensions cannot be installed.";
  fi
fi
EOF

        ZIPNAME="Invincible-Chopin-chopin-KsuBackslashxx-$(date +%Y%m%d-%H%M).zip"
        rm -rf *zip
        (cd AnyKernel3 && zip -r9 "../$ZIPNAME" * -x '*.git*' README.md *placeholder)
        rm -rf AnyKernel3
        echo "Successfully created flashable kernel zip: $ZIPNAME"
    else
        echo "Compilation failed! Check error.log"
        exit 1
    fi
}
compile "$@"
