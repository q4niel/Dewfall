#!/bin/bash
cd "$(realpath -m "$0/../../../../")"
source "env/run/linux/util/docker_util.sh"
runDocker "env/Dockerfile.linux" "env/src/fetch_libraries.py"
copyDocker "Dewfall/3rd" "3rd"