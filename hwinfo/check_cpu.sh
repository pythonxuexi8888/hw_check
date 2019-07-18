#!/bin/bash 
. $(dirname $0)/functions

report_file="$(dirname $0)/cpu_report.csv"
_refresh_report_file 

# CPU numbers int 
#total_physical_cpu=$(cat $tmpfile | grep -i 'description: CPU' | _change_delimiter )

# CPU slot IDs
cpu_socket_id=$(cat $tmpfile | grep -A9 'description: CPU' | grep 'slot:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter )
_update_info $cpu_socket_id 

# CPU product versions 
cpu_product_version=$(cat $tmpfile | grep -A9 'description: CPU' | grep 'version:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter ) 
_update_info $cpu_product_version 

# CPU L1 cache
l1_cache=$(cat $tmpfile | grep -A4 'L1 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter )
_update_info $l1_cache

# CPU L2 cache
l2_cache=$(cat $tmpfile | grep -A4 'L2 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter )
_update_info $l2_cache

# CPU L3 cache
l3_cache=$(cat $tmpfile | grep -A4 'L3 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter )
_update_info $l3_cache

# CPU cores
cores_on_chip=$(cat $tmpfile | grep -A14 'description: CPU' | grep 'configuration:' | awk '{print $2}' | awk -F= '{print $2}' | _change_delimiter )
_update_info $cores_on_chip

# CPU threads
threads_on_chip=$(cat $tmpfile | grep -A14 'description: CPU' | grep 'configuration:' | awk '{print $4}' | awk -F= '{print $2}' | _change_delimiter )
_update_info $threads_on_chip

sed -i "1i socket,product_verdor,l1_cache,l2_cache,l3_cach3,cores,threads" $report_file
rm -f $tmpfile
