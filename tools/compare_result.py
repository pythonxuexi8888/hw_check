#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import re
import json
import shutil


def compare(result_dir, error_dir, file_name1, file_name2):
    out_list = []
    # out_list.append('---- {} <----> {} ----\n' .format(file_name1, file_name2))
    file1 = open('{}/{}' .format(result_dir, file_name1), 'r')
    file2 = open('{}/{}' .format(result_dir, file_name2), 'r')
    hw_dict1 = json.load(file1) #符合要求的模板
    hw_dict2 = json.load(file2) #带比较的机器信息
    file1.close()
    file2.close()
    items = hw_dict1.keys()
    if 'CPU' in items:
        cpu_info1 = hw_dict1['CPU']
        cpu_info2 = hw_dict2['CPU']
        cpu_diff1 = [item for item in cpu_info1 if item not in cpu_info2] #本应有却没有的项
        cpu_diff2 = [item for item in cpu_info2 if item not in cpu_info1] #本不应有却有的项

        if len(cpu_diff1) != 0 or len(cpu_diff2) != 0:
            out_list.append('------------------------------ CPU ------------------------------\n')
            fmt = '{:10s}{:50s}{:10s}{:10s}{:10s}{:10s}{:10s}\n'
            head = fmt .format('ID', 'version', 'l1_cache', 'l2_cache','l3_cache', 'cores', 'threads')
            out_list.append(head)
            out_list.append('正确的CPU信息\n')
            for item in cpu_diff1:
                output = fmt .format(item['ID'], item['version'], item['l1_cache'], item['l2_cache'],
                                     item['l3_cache'], item['cores'], item['threads'])
                out_list.append(output)
            out_list.append('错误的CPU信息\n')
            for item in cpu_diff2:
                output = fmt .format(item['ID'], item['version'], item['l1_cache'], item['l2_cache'],
                                     item['l3_cache'], item['cores'], item['threads'])
                out_list.append(output)
    if 'Memory' in items:
        memory_info1 = hw_dict1['Memory']
        memory_info2 = hw_dict2['Memory']
        memory_diff1 = [item for item in memory_info1 if item not in memory_info2] #本应有却没有的项
        memory_diff2 = [item for item in memory_info2 if item not in memory_info1] #本不应有却有的项

        if len(memory_diff1) != 0 or len(memory_diff2) != 0:
            out_list.append('------------------------------ 内存 ------------------------------\n')
            fmt = '{:10s}{:10s}{:20s}{:30s}{:30s}{:20s}\n'
            head = fmt .format('size', 'speed', 'slot', 'channel', 'vendor', 'version')
            out_list.append(head)
            out_list.append('正确的内存信息\n')
            for item in memory_diff1:
                output = fmt .format(item['size'], item['speed'], item['slot'], item['channel'],
                                     item['vendor'], item['version'])
                out_list.append(output)
            out_list.append('错误的内存信息\n')
            for item in memory_diff2:
                output = fmt .format(item['size'], item['speed'], item['slot'], item['channel'],
                                     item['vendor'], item['version'])
                out_list.append(output)
    if 'Network' in items:
        network_info1 = hw_dict1['Network']
        network_info2 = hw_dict2['Network']
        network_diff1 = [item for item in network_info1 if item not in network_info2] #本应有却没有的项
        network_diff2 = [item for item in network_info2 if item not in network_info1] #本不应有却有的项
        
        if len(network_diff1) != 0 or len(network_diff2) != 0:
            out_list.append('------------------------------ 网卡 ------------------------------\n')
            fmt = "{:10s}{:10s}{:20s}{:35s}{:50s}\n"
            head = fmt .format('ID', 'numa_node', 'interrupt_node', 'vendor', 'version')
            out_list.append(head)
            out_list.append('正确的网卡信息\n')
            for item in network_diff1:
                output = fmt .format(item['ID'], item['numa_node'], item['interrupt_node'],
                                     item['vendor'], item['version'])
                out_list.append(output)
            out_list.append('错误的网卡信息\n')
            for item in network_diff2:
                output = fmt .format(item['ID'], item['numa_node'], item['interrupt_node'],
                                     item['vendor'], item['version'])
                out_list.append(output)
    if 'HDD' in items:
        hdd_info1 = hw_dict1['HDD']
        hdd_info2 = hw_dict2['HDD']
        hdd_diff1 = [item for item in hdd_info1 if item not in hdd_info2] #本应有却没有的项
        hdd_diff2 = [item for item in hdd_info2 if item not in hdd_info1] #本不应有却有的项

        if len(hdd_diff1) != 0 or len(hdd_diff2) != 0:
            out_list.append('------------------------------ 机械硬盘 ------------------------------\n')
            fmt = "{:10s}{:20s}{:10s}{:15s}\n"
            head = fmt .format('device', 'size', 'vendor', 'version')
            out_list.append(head)
            out_list.append('正确的机械硬盘信息\n')
            for item in hdd_diff1:
                output = fmt .format(item['device'], item['size'], item['vendor'], item['version'])
                out_list.append(output)
            out_list.append('错误的机械硬盘信息\n')
            for item in hdd_diff2:
                output = fmt .format(item['device'], item['size'], item['vendor'], item['version'])
                out_list.append(output)
    if 'NVMe' in items:
        nvme_info1 = hw_dict1['NVMe']
        nvme_info2 = hw_dict2['NVMe']
        nvme_diff1 = [item for item in nvme_info1 if item not in nvme_info2] #本应有却没有的项
        nvme_diff2 = [item for item in nvme_info2 if item not in nvme_info1] #本不应有却有的项

        if len(nvme_diff1) != 0 or len(nvme_diff2) != 0:
            out_list.append('------------------------------ NVMe硬盘 ------------------------------\n')
            fmt = "{:15s}{:10s}{:25s}{:75s}{:10s}{:15s}{:15s}\n"
            head = fmt .format('device', 'size', 'model_number', 'product', 'life', 'numa_node', 'interrupt_node')
            out_list.append(head)
            out_list.append('正确的NVMe硬盘信息\n')
            for item in nvme_diff1:
                output = fmt .format(item['device'], item['size'], item['model_number'], item['product'],
                                     item['life'], item['numa_node'], item['interrupt_node'])
                out_list.append(output)
            out_list.append('错误的NVMe硬盘信息\n')
            for item in nvme_diff2:
                output = fmt .format(item['device'], item['size'], item['model_number'], item['product'],
                                     item['life'], item['numa_node'], item['interrupt_node'])
                out_list.append(output)
    if 'RAID' in items:
        raid_info1 = hw_dict1['RAID']
        raid_info2 = hw_dict2['RAID']
        raid_diff1 = [item for item in raid_info1 if item not in raid_info2] #本应有却没有的项
        raid_diff2 = [item for item in raid_info2 if item not in raid_info1] #本不应有却有的项

        if len(raid_diff1) != 0 or len(raid_diff2) != 0:
            out_list.append('------------------------------ RAID卡 ------------------------------\n')
            fmt = "{:40s}{:40s}\n"
            head = fmt .format('vendor', 'product')
            out_list.append(head)
            out_list.append('正确的RAID卡信息\n')
            for item in raid_diff1:
                output = fmt .format(item['vendor'], item['product'])
                out_list.append(output)
            out_list.append('错误的RAID卡信息\n')
            for item in raid_diff1:
                output = fmt .format(item['vendor'], item['product'])
                out_list.append(output)
    
    if len(out_list) != 0:
        result_log = '{}/{}.{}' .format(error_dir, file_name2[:-5], 'log')
        result_log_file = open(result_log, 'w')
        result_log_file.writelines(out_list)
        result_log_file.close()


def usage():
    usage_info = '''
    Usage:
    python compare_result.py <host_list> <the_right_machine>
    Example:
    python compare_result.py host_list 10.216.0.75
    '''
    print usage_info


def main():
    if len(sys.argv) != 3:
        usage()
    else:
        host_list = sys.argv[1]
        result_dir = "../{}" .format(host_list)
        if not os.path.isdir(result_dir):
            print "The result directory doesn't exist!"
        else:
            error_dir = "../error-{}" .format(host_list)
            right_machine = "{}.json" .format(sys.argv[2])
            if os.path.isdir(error_dir):
                shutil.rmtree(error_dir)
            os.mkdir(error_dir)
            file_list = os.listdir(result_dir)
            file_list.sort()
            # file_name1 = file_list[0]
            # file_list.remove(file_name1)
            for f in file_list:
                compare(result_dir, error_dir, right_machine, f)


if __name__ == '__main__':
    main()
