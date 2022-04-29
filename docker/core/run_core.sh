#!/bin/bash


srsepc_if_masq.sh eth0

CORE_IP_ADDR=$(ifconfig eth0 | grep 'inet' | awk '{ print $2}')
sed -i "s/enb_addr/$CORE_IP_ADDR/g" core.conf

srsepc epc.conf