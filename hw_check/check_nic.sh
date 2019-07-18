#!/bin/bash
#This script check network card information"""

tmpfile=$(mktemp)
lshw > $tmpfile || exit 1

report_file="nic_report.csv"
[[ -f $report_file ]] && rm -f $report_file
touch $report_file

# pci bus id
lspci_buses_sh=$(lspci | grep 'Ethernet controller:' | awk '{print $1}')

for lspci_bus in $lspci_buses_sh ;do
    # get nic name
    eth_sh=$(grep -A1 $lspci_bus $tmpfile | grep 'logical name:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
#    # get mac addr
#    mac_sh=$(ip link | grep -A1 "$eth_sh" | grep 'link/ether' | awk '{print $2}')
    # numa node
    numa_node_sh=$(cat /sys/class/net/$eth_sh/device/numa_node)
    # interrupt num
    interrupt_sh=$(cat /proc/interrupts | grep $eth_sh | awk -F: 'NR==1 {print $1}' | sed 's/^[ \t]*//g')
    if [[ -n ${interrupt_sh// /} ]] ;then
        interrupt_str=$(cat /proc/irq/${interrupt_sh// /}/node | awk '{print $1}')
    else
        interrupt_str="--"
    fi
    # vendor info
    vendor_sh=$(grep -B3 $lspci_bus $tmpfile | grep 'vendor:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')
    # product version
    version_sh=$(grep -B3 $lspci_bus $tmpfile | grep 'product:' | awk -F: '{print $2}' | sed 's/^[ \t]*//g')

    # output
    echo "$eth_sh,$numa_node_sh,$interrupt_str,$vendor_sh,$version_sh" >> $report_file
done

sed -i "1i ID,numa_node,interrupt_node,vendor,product_version" $report_file
rm -f $tmpfile

