#!/bin/bash 

tmpfile=$(mktemp)
lshw > $tmpfile || exit 1

cpu_report_file="cpu_report.csv"
[[ -f $cpu_report_file ]] && rm -f $cpu_report_file 
touch $cpu_report_file

OLD_IFS=$IFS

function _append_field(){
    local line_num=$1 
    shift
    local field_content="$@"
    local line_max=$(wc -l < $cpu_report_file)
    if [[ $line_max -lt ${line_num} ]] ;then
        echo "$field_content" >> $cpu_report_file
    else
        sed -i "${line_num}s/$/,$field_content/g" $cpu_report_file 
    fi
}
function _update_info(){
    local info=$@
    IFS="|"
    local nu=1
    for field in $info;do
        IFS="$OLD_IFS"
        _append_field $nu $field 
        nu=$((nu + 1))
    done
    IFS="$OLD_IFS"
}
function _change_delimiter(){
    [[ $# -gt 0 ]] && exec 0<$1
    sed ':label;N;s/\n/|/g;b label' <&0
    # close when no data
    exec 0<&-
}
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

sed -i "1i socket,product_verdor,l1_cache,l2_cache,l3_cach3,cores,threads" $cpu_report_file
rm -f $tmpfile 
