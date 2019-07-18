#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import re
import json

def print_json(result_json_file):
    result_json = open(result_json_file, 'r')
    result_dict = json.load(result_json)
    result_json.close()
    items = result_dict.keys()
    out_list = []

    if 'CPU' in items:
        cpu_info = result_dict['CPU']

        out_list.append('------------------------------ CPU ------------------------------')
        fmt = '{:10s}{:50s}{:10s}{:10s}{:10s}{:10s}{:10s}'
        head = fmt .format('ID', 'version', 'l1_cache', 'l2_cache','l3_cache', 'cores', 'threads')
        out_list.append(head)
        for item in cpu_info:
            output = fmt .format(item['ID'], item['version'], item['l1_cache'], item['l2_cache'],
                                 item['l3_cache'], item['cores'], item['threads'])
            out_list.append(output)
    if 'Memory' in items:
        memory_info = result_dict['Memory']

        out_list.append('------------------------------ 内存 ------------------------------')
        fmt = '{:10s}{:10s}{:20s}{:30s}{:30s}{:20s}'
        head = fmt .format('size', 'speed', 'slot', 'channel', 'vendor', 'version')
        out_list.append(head)
        for item in memory_info:
            output = fmt .format(item['size'], item['speed'], item['slot'], item['channel'],
                                 item['vendor'], item['version'])
            out_list.append(output)
    if 'Network' in items:
        network_info = result_dict['Network']

        out_list.append('------------------------------ 网卡 ------------------------------')
        fmt = "{:10s}{:10s}{:20s}{:35s}{:50s}"
        head = fmt .format('ID', 'numa_node', 'interrupt_node', 'vendor', 'version')
        out_list.append(head)
        for item in network_info:
            output = fmt .format(item['ID'], item['numa_node'], item['interrupt_node'],
                                 item['vendor'], item['version'])
            out_list.append(output)
    if 'HDD' in items:
        hdd_info = result_dict['HDD']

        out_list.append('------------------------------ 机械硬盘 ------------------------------')
        fmt = "{:10s}{:20s}{:10s}{:15s}"
        head = fmt .format('device', 'size', 'vendor', 'version')
        out_list.append(head)
        for item in hdd_info:
            output = fmt .format(item['device'], item['size'], item['vendor'], item['version'])
            out_list.append(output)
    if 'NVMe' in items:
        nvme_info = result_dict['NVMe']

        out_list.append('------------------------------ NVMe硬盘 ------------------------------')
        fmt = "{:15s}{:10s}{:25s}{:75s}{:10s}{:15s}{:15s}"
        head = fmt .format('device', 'size', 'model_number', 'product', 'life', 'numa_node', 'interrupt_node')
        out_list.append(head)
        for item in nvme_info:
            output = fmt .format(item['device'], item['size'], item['model_number'], item['product'],
                                 item['life'], item['numa_node'], item['interrupt_node'])
            out_list.append(output)
    if 'RAID' in items:
        raid_info = result_dict['RAID']

        out_list.append('------------------------------ RAID卡 ------------------------------')
        fmt = "{:40s}{:40s}"
        head = fmt .format('vendor', 'product')
        out_list.append(head)
        for item in raid_info:
            output = fmt .format(item['vendor'], item['product'])
            out_list.append(output)
    for item in out_list:
        print item

def usage():
    usage_info = '''
    Usage:
    python print_json_to_txt.py <result_json_file>
    Example:
    python print_json_to_txt.py ../results_hw/10.216.0.76.json
    '''
    print usage_info


def main():
    if len(sys.argv) != 2:
        usage()
    else:
        print_json(sys.argv[1])


if __name__ == '__main__':
    main()
