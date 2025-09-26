#!/bin/bash
cd "$(realpath -m "$0/../../../../")"
source "env/run/linux/util/docker_util.sh"
runDocker "env/Dockerfile.linux" "env/src/build.py"