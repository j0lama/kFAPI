#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: ./push.sh <image name>"
    exit 1
fi

docker image push j0lama/$1
