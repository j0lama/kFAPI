#!/bin/bash

if [ ! -f core-configured ]; then
    echo "Configuring core..."
    # Configure the network
    sysctl -w net.ipv4.ip_forward=1
    iptables -t nat -A POSTROUTING -s 1.1.0.0/16 ! -o srsTUN -j MASQUERADE
    CORE_IP_ADDR=$(ifconfig eth0 | grep 'inet' | awk '{ print $2}')
    sed -i "s/core_addr/$CORE_IP_ADDR/g" core.conf
    touch core-configured
    echo "Configuration done!"
fi

srsepc core.conf