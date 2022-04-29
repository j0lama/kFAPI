#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "USE: sudo ./run_proxy.sh <Number of UEs> <eNB IP> <UE IP>"
    exit 1
fi

./build/proxy $1 $2 $(ifconfig eth0 | grep 'inet' | awk '{ print $2}') $3