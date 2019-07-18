#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


class NVMeCheck(object):
    """This script check nvme ssd information"""

    def nvme_check(self):

        # nvme devices
        nvmes_sh = "nvme list | grep nvme | awk '{print $1}' | sort"
        nvmes = ShellParse.shell_parse(nvmes_sh)
        if isinstance(nvmes, str):
            tmp = []
            tmp.append(nvmes)
            nvmes = tmp
        # print nvmes
        # print "NVMe SSD numbers: ", len(nvmes)

        # nvme numa nodes
        nvme_nodes_sh = "ls /sys/class/nvme/ | sort"
        nvme_nodes = ShellParse.shell_parse(nvme_nodes_sh)
        if isinstance(nvme_nodes, str):
            tmp = []
            tmp.append(nvme_nodes)
            nvme_nodes = tmp
        # print nvme_nodes

        products = dict() # product description
        model_numbers = dict()  # nvme model_number
        devices_json_file = open('devices_json.tmp.txt', 'r')
        devices = json.load(devices_json_file)
        devices_json_file.close()
        for device in devices['Devices']:
            products[device['DevicePath']] = device['ProductName']
            model_numbers[device['DevicePath']] = device['ModelNumber']
        length_of_model = len(device['ModelNumber'].split())
        sizes = list()  # nvme size
        lifes = list()  # nvme lifes
        numa_nodes = list()  # numa nodes
        interrupts = list()  # interrupt numa nodes
        for i in xrange(len(nvmes)):
            size_sh = "nvme list | grep %s | awk '{print $%d $%d}'" % (nvmes[i], 4+length_of_model,
                                                                       5+length_of_model)
            size = ShellParse.shell_parse(size_sh)
            sizes.append(size)

            """ model_number_sh = "nvme list | grep %s | awk '{print $3 $4}'" % nvmes[i]
            model_number = ShellParse.shell_parse(model_number_sh)
            model_numbers.append(model_number) """

            life_sh = "nvme smart-log %s | grep percentage_used | awk '{print $3}'" % nvmes[i]
            life = ShellParse.shell_parse(life_sh)
            lifes.append(life)

            numa_node_sh = "cat /sys/class/nvme/%s/device/numa_node | awk '{print $1}'" % nvme_nodes[i]
            numa_node = ShellParse.shell_parse(numa_node_sh)
            numa_nodes.append(numa_node)

            irqs_sh = ("cat /proc/interrupts | grep %s | awk -F: "
                       "'NR==1 {print $1}' | sed 's/^[ \t]*//g'"  % nvme_nodes[i])
            irq = ShellParse.shell_parse(irqs_sh)
            interrupt_sh = "cat /proc/irq/%s/node" % irq
            interrupt = ShellParse.shell_parse(interrupt_sh)
            interrupts.append(interrupt)

        result_dict = {'NVMe': []}
        for index in xrange(len(nvmes)):
            nvme_info = {}
            nvme_info['device'] = nvmes[index]
            nvme_info['size'] = sizes[index]
            nvme_info['model_number'] = model_numbers[nvmes[index]]
            nvme_info['product'] = products[nvmes[index]]
            nvme_info['life'] = lifes[index]
            nvme_info['numa_node'] = numa_nodes[index]
            nvme_info['interrupt_node'] = interrupts[index]
            result_dict['NVMe'].append(nvme_info)
        return result_dict


def main():
    os.popen("nvme list -o json > devices_json.tmp.txt")
    check = NVMeCheck()
    results = check.nvme_check()
    print json.dumps(results, indent=2, sort_keys=True)
    os.remove("devices_json.tmp.txt")

if __name__ == "__main__":
    main()
