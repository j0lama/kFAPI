#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: ./build.sh <image name>"
    exit 1
fi

docker build -t $1 .
docker image tag $1 j0lama/$1:latest
