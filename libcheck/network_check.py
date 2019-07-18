#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


class NetworkCheck(object):
    """This script check network card information"""

    def network_check(self):
        eths = list()
        eth_macs = list()
        numa_nodes = list()  # numa node of network card
        interrupt_nodes = list()  # interrupt node of network card
        vendors = list()  # network card vendors
        versions = list()  # network card versions
        lspci_buses_sh = "lspci | grep 'Ethernet controller:' | awk '{print $1}'"
        lspci_buses = ShellParse.shell_parse(lspci_buses_sh)
        # print "Network device numbers: ", len(lspci_buses)
        for lspci_bus in lspci_buses:
            eth_sh = ("grep -A1 %s lshw.tmp.txt | grep 'logical name:' | awk -F: '{print $2}' | "
                      "sed 's/^[ \t]*//g'" % lspci_bus)
            eth = ShellParse.shell_parse(eth_sh)
            eths.append(eth)
            mac_sh = ("ip link | grep -A1 '%s:' | grep 'link/ether' | awk '{print $2}'" % eth)
            mac = ShellParse.shell_parse(mac_sh)
            eth_macs.append(mac)
            numa_node_sh = "cat /sys/class/net/%s/device/numa_node" % eth
            numa_node = ShellParse.shell_parse(numa_node_sh)
            numa_nodes.append(numa_node)

            interrupt_sh = ("cat /proc/interrupts | grep %s | awk -F: 'NR==1 {print $1}' |"
                            " sed 's/^[ \t]*//g'" % eth)
            interrupt = ShellParse.shell_parse(interrupt_sh)
            if interrupt.strip():
                shell = "cat /proc/irq/%s/node | awk '{print $1}'" % interrupt
                interrupt_nodes.append(ShellParse.shell_parse(shell))
            else:
                interrupt_nodes.append("--")

            vendor_sh = ("grep -B3 %s lshw.tmp.txt | grep 'vendor:' | awk -F: '{print $2}' |"
                         " sed 's/^[ \t]*//g'" % lspci_bus)
            vendor = ShellParse.shell_parse(vendor_sh)
            vendors.append(vendor)

            version_sh = ("grep -B3 %s lshw.tmp.txt | grep 'product:' | awk -F: '{print $2}' |"
                          " sed 's/^[ \t]*//g'" % lspci_bus)
            version = ShellParse.shell_parse(version_sh)
            versions.append(version)

        sorted_eths = sorted(eths)
        indexs = []
        for sorted_eth in sorted_eths:
            indexs.append(eths.index(sorted_eth))

        result_dict = {'Network': []}
        for index in indexs:
            network_info = {}
            network_info['ID'] = eths[index]
            network_info['numa_node'] = numa_nodes[index]
            network_info['interrupt_node'] = interrupt_nodes[index]
            network_info['vendor'] = vendors[index]
            network_info['version'] = versions[index]
            result_dict['Network'].append(network_info)
        return result_dict


def main():
    os.popen("lshw > lshw.tmp.txt")
    check = NetworkCheck()
    results = check.network_check()
    print json.dumps(results, indent=2, sort_keys=True)
    os.remove("lshw.tmp.txt")


if __name__ == "__main__":
    main()
