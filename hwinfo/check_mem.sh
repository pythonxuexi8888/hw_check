#!/bin/bash
. $(dirname $0)/functions

report_file="$(dirname $0)/mem_report.csv"
_refresh_report_file

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

sed -i "1i size,speed,slot,channel,vendor,product_version" $report_file
rm -f $tmpfile
