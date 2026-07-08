#!/bin/bash

function compile() 
{
    source ~/.bashrc && source ~/.profile
    export LC_ALL=C
    export ARCH=arm64
    export TZ="Asia/Jakarta"
    export KBUILD_BUILD_USER="ChenXia"
    export KBUILD_BUILD_HOST="ChenXia"
    export KBUILD_BUILD_TIMESTAMP="$(TZ='Asia/Jakarta' date)"

    # Read and increment build version
    VERSION_FILE="/home/afifnaxxwahana3/kernel_source/build_version.txt"
    if [ ! -f "$VERSION_FILE" ]; then
        echo "1" > "$VERSION_FILE"
    fi
    VERSION=$(cat "$VERSION_FILE")
    VERSION_STR=$(printf "%04d" "$VERSION")
    DATE_STR=$(date '+%Y%m%d')
    
    export LOCALVERSION="-ChenXia"

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

    CLANG_DIR="/home/afifnaxxwahana3/toolchains/clang-r563880c"
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
        sed -i 's/kernel.string=.*/kernel.string=Kernel by Chen Xia/g' AnyKernel3/anykernel.sh
        cp out/arch/arm64/boot/Image.gz-dtb AnyKernel3/

        # Increment build version for next run
        echo $((VERSION + 1)) > "$VERSION_FILE"

        ZIPNAME="ChenXia-kernel-v1-${DATE_STR}-${VERSION_STR}.zip"
        rm -rf *zip
        (cd AnyKernel3 && zip -r9 "../$ZIPNAME" * -x '*.git*' README.md *placeholder)
        rm -rf AnyKernel3
        echo "Successfully created flashable kernel zip: $ZIPNAME"

        # ── Auto-generate CI-style build info post ──
        CLANG_RAW=$(${CLANG_DIR}/bin/clang --version 2>/dev/null | head -1)
        # Extract only the FIRST parenthetical group (build ID + flags), stop at first closing paren
        CLANG_BUILD_INFO=$(echo "$CLANG_RAW" | sed 's/Android (\([^)]*\)).*/\1/')
        CLANG_VER=$(echo "$CLANG_RAW" | grep -oP 'clang version \K[0-9.]+')
        COMPILER_STR="Android (${CLANG_BUILD_INFO}) clang ${CLANG_VER}"
        KV=$(grep -m1 "^VERSION" Makefile | awk '{print $3}')
        KPL=$(grep -m1 "^PATCHLEVEL" Makefile | awk '{print $3}')
        KSL=$(grep -m1 "^SUBLEVEL" Makefile | awk '{print $3}')
        KERNEL_VER="${KV}.${KPL}.${KSL}"
        COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
        TIMESTAMP="${DATE_STR}-$(TZ='Asia/Jakarta' date '+%H%M')"
        FILE_MD5=$(md5sum "$ZIPNAME" | awk '{print $1}')

        POST_FILE="build_info_${VERSION_STR}.txt"
        printf "Build info:\nDevice: POCO X3 GT [chopin]\nKernel Version: %s\nCompiler: %s\nBuild host: ChenXia\nCommit / Branch: (%s) / %s\nBuild variant: KSUNext / Stable (clean)\nTimestamp: %s\nMD5: %s\n" \
            "$KERNEL_VER" "$COMPILER_STR" "$COMMIT_HASH" "$BRANCH" "$TIMESTAMP" "$FILE_MD5" > "$POST_FILE"

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cat "$POST_FILE"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Build info saved to: $POST_FILE"

        # ── Auto-upload to Telegram ──
        TG_TOKEN="8923896004:AAGCPhMh0ltOgkfgw4PW0T4p9EzfKCkSi4g"
        TG_CHAT_ID="-1003976388872"
        CAPTION="<pre>$(cat "$POST_FILE")</pre>"

        echo "Uploading $ZIPNAME to Telegram..."
        curl -s -F chat_id="${TG_CHAT_ID}" \
             -F document=@"${ZIPNAME}" \
             --form-string "caption=${CAPTION}" \
             -F parse_mode="HTML" \
             https://api.telegram.org/bot${TG_TOKEN}/sendDocument > /dev/null

        if [ $? -eq 0 ]; then
            echo "Telegram upload successful!"
        else
            echo "Telegram upload failed!"
        fi
    else
        echo "Compilation failed! Check error.log"
        exit 1
    fi
}
compile "$@"
