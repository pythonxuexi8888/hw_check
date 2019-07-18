#!/bin/bash 

tmpfile=$(mktemp)
lshw > $tmpfile || exit 1

cpu_report_file="cpu_report.csv"
touch $cpu_report_file 

function _update_report_by_column(){
    local column_content=${@}
    local row_num=1
    local line_max=$(wc -l < $cpu_report_file)
    for column in $column_content ;do
        if [[ $line_max -lt ${row_num} ]] ;then
            echo "$column" >> $cpu_report_file
        else
            sed -i "${i}s/$/,$column_content/g" $cpu_report_file 
        fi
        row_num=$((row_num + 1))
    done
}

# CPU numbers int 
#total_physical_cpu=$(cat $tmpfile | grep -i 'description: CPU' | wc -l)

# CPU slot IDs
cpu_socket_id=$(cat $tmpfile | grep -A9 'description: CPU' | grep 'slot:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
echo $cpu_socket_id && sleep 5
_update_report_by_column $cpu_socket_id 

# CPU product versions 
cpu_product_version=$(cat $tmpfile | grep -A9 'description: CPU' | grep 'version:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
_update_report_by_column $cpu_product_version 

# CPU L1 cache
l1_cache=$(cat $tmpfile | grep -A4 'L1 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
_update_report_by_column $l1_cache

# CPU L2 cache
l2_cache=$(cat $tmpfile | grep -A4 'L2 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
_update_report_by_column $l2_cache

# CPU L3 cache
l3_cache=$(cat $tmpfile | grep -A4 'L3 cache' | grep 'capacity:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
_update_report_by_column $l3_cache

# CPU cores
cores_on_chip=$(cat $tmpfile | grep -A14 'description: CPU' | grep 'configuration:' | awk '{print $2}' | awk -F= '{print $2}')
_update_report_by_column $cores_on_chip

# CPU threads
threads_on_chip=$(cat $tmpfile | grep -A14 'description: CPU' | grep 'configuration:' | awk '{print $4}' | awk -F= '{print $2}')
_update_report_by_column $threads_on_chip

rm -f $tmpfile 
