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

    CLANG_DIR="/home/afifnaxxwahana3/toolchains/aosp-clang"
    GCC_DIR="/home/afifnaxxwahana3/toolchains/arm-gnu"

    PATH="${CLANG_DIR}/bin:${GCC_DIR}/bin:${PATH}" \
    make -j$(nproc --all) O=out \
                          ARCH=arm64 \
                          CC="clang" \
                          HOSTCC="gcc" \
                          HOSTLD="ld" \
                          CLANG_TRIPLE=aarch64-none-linux-gnu- \
                          CROSS_COMPILE="aarch64-none-linux-gnu-" \
                          CROSS_COMPILE_ARM32="arm-linux-gnueabi-" \
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
