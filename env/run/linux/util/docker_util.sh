#!/bin/bash

container="dewfall"

runDocker() {
    local dockerfile=$1
    local pyScript=$2
    local pyArgs=("${@:3}")

    # Remove container if it already exists
    if [ "$(sudo docker ps -a -q -f name=^${container})" ]; then
        sudo docker rm -f "$container"
    fi

    # Build image
    sudo docker build -f "$dockerfile" -t "$container:latest" .

    # Run container
    sudo docker run --name "$container" "$container:latest" "$pyScript" "${pyArgs[@]}"
}

copyDocker() {
    local dockerPath=$1
    local outPath=$2

    # Delete $outPath if it exists locally
    if [ -d "$outPath" ]; then
        sudo rm -r "$outPath"
    fi

    # Copy from container to local
    sudo docker cp "$container:/$dockerPath" "./$outPath"

    # Make current user own $outPath
    sudo chown -R $(whoami):$(whoami) "./$outPath"
}