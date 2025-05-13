#!/bin/bash

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Error: '$1' is not installed. Please install it manually for your system."
        echo "Official Website: $2"
        exit 1
    fi
}

require python3 https://www.python.org
require clang++ https://clang.llvm.org

python3 --version
clang++ --version | head -n 1