#!/bin/bash

tmpfile=$(mktemp)
lshw > $tmpfile || exit 1

mem_report_file="mem_report.csv"
[[ -f $mem_report_file ]] && rm -f $mem_report_file
touch $mem_report_file

OLD_IFS=$IFS

function _append_field(){
    local line_num=$1
    shift
    local field_content="$@"
    local line_max=$(wc -l < $mem_report_file)
    if [[ $line_max -lt ${line_num} ]] ;then
        echo "$field_content" >> $mem_report_file
    else
        sed -i "${line_num}s/$/,$field_content/g" $mem_report_file
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


# memory size
sizes_sh=$(dmidecode -t 17 | grep Size | grep -v 'No Module Installed' | awk -F: '{print $2}' | sed 's/[ \t]*//g' | _change_delimiter)
_update_info $sizes_sh


# memory speed
speeds_sh=$(dmidecode -t 17 | grep Speed | grep -v -E 'Unknown|Clock' | awk -F: '{print $2}' | sed 's/[ \t]*//g' | _change_delimiter)
_update_info $speeds_sh
# memory slot


slots_sh=$(dmidecode -t 17 | grep -A3 Size | grep -v 'No Module Installed' | grep -E 'Size:|Locator:' | sed -n '/Size:/,+1p' | grep 'Locator:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter)
_update_info $slots_sh

# memory channel
channels_sh=$(dmidecode -t 17 | grep -A4 Size | grep -v 'No Module Installed' | grep -E 'Size:|Bank Locator:' | sed -n '/Size:/,+1p' | grep 'Bank Locator:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g' | _change_delimiter)
_update_info $channels_sh

# memory vendor
IFS="|"
for slot in $slots_sh;do
    IFS="$OLD_IFS"
    vendor_partial=$(grep -B4 "slot: $slot" $tmpfile | grep 'vendor:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
    vendor_string+="$vendor_partial|" 
    IFS="|"
done
_update_info $vendor_string

# memory version
IFS="|"
for slot in $slots_sh;do
    IFS="$OLD_IFS"
    version_partial=$(grep -B4 "slot: $slot" $tmpfile | grep 'product:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
    version_string+="$version_partial|"
    IFS="|"
done
_update_info $version_string

sed -i "1i size,speed,slot,channel,vendor,product_version" $mem_report_file

rm -f $tmpfile
