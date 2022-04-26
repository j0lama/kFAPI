#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "USE: ./run.sh <ID>"
    exit 1
fi

kubectl run shell$1 --rm -i --tty --image j0lama/empty:latest -- bash