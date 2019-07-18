#! /usr/bin/python
# -*- coding: utf-8 -*-
#from __future__ import print_function

# storage device info (lshw)
# lshw -C storage -json |sed -e "1i {\n\"storage\":\[" -e "$ a \]}" -e "s/[ ]\+//g" -e "s/}{/},{/g" -e "/^$/d" >3.json

# nvme list (nvme-cli)
# nvme list -o json

import json
import commands

def shell_run(cmd):
    ret, out = commands.getstatusoutput(cmd)
    if ret == 0 :
        return out
    else:
        return False

nvme_report_file = './nvme_report.csv'
cmd = "ls /sys/class/nvme/"
nvme_devs = shell_run(cmd).split()

result = 'device,product_version,size,vendor,life,numa_node,interrupt_node\n'

for nvme_dev in nvme_devs:

    # name, model number, size
    cmd1 = "nvme list |awk '/^\/dev\/%s/{print $1\",\"$3\",\"$8,$9}'" % nvme_dev
    basic_info = shell_run(cmd1)
    nvme_dev_name = basic_info.split(',')[0]

    # product 
    cmd2 = "nvme list -o json"
    _tmp_json = json.loads(shell_run(cmd2))['Devices']

    _dev_info = filter(lambda x : x['DevicePath'] == nvme_dev_name, _tmp_json)[0]
    product_name = _dev_info['ProductName']

    # life
    cmd3 = "nvme smart-log %s | grep percentage_used | awk '{print $3}'" % nvme_dev_name
    life = shell_run(cmd3)

    # numa node
    cmd4 = "cat /sys/class/nvme/%s/device/numa_node | awk '{print $1}'" % nvme_dev
    numa_node = shell_run(cmd4)

    # interrupt node
    cmd5 = "cat /proc/interrupts | grep %s | awk -F: 'NR==1 {print $1}' | sed 's/^[ \t]*//g'"  % nvme_dev
    irq_num = shell_run(cmd5)
    # 
    cmd6 = "cat /proc/irq/%s/node" % irq_num
    interrupt_node = shell_run(cmd6)

    #print(basic_info,product_name,life,numa_node,interrupt_node, sep=',')
    result += ','.join([basic_info,product_name,life,numa_node,interrupt_node]) + '\n'

f = open(nvme_report_file, 'w')
f.write(result)
f.close()
