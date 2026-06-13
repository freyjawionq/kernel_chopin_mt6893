#!/bin/bash

function compile() 
{

source ~/.bashrc && source ~/.profile
export LC_ALL=C
export ARCH=arm64
export LOCALVERSION='-Ciallo~'

 if ! [ -d "out" ]; then
echo "Kernel OUT Directory Not Found . Making Again"
mkdir out
fi

make O=out ARCH=arm64 chopin_user_defconfig

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
}
compile
