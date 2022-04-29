#!/bin/bash

cd ../../../
source oaienv
cd cmake_targets/ran_build/build/

# Modify the configuration file
ENB_IP_ADDR=$(ifconfig eth0 | grep 'inet' | awk '{ print $2}')
sed -i "s/enb_addr/$ENB_IP_ADDR/g" enb.conf

./lte-softmodem -O enb.conf --emulate-l1 --nsa --log_config.global_log_options level,nocolor,time,thread_id | tee eNB.log 2>&1