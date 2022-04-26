#!/bin/bash

if [ ! -f /local/repository/core-setup-complete ]; then
    echo "The Core setup has not finished. Please wait"
    exit 0
fi

cd /local/repository/config/

sudo srsepc core.conf