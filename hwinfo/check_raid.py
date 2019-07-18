#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import commands

# check raid type (different vendor different name) 
# lshw -C storage

raid_type = 'aacraid'
raid_report_file = sys.path[0] + '/raid_report.csv'

def shell_run(cmd):
    ret, out = commands.getstatusoutput(cmd)
    if ret == 0 :
        return out
    else:
        return False


cmd = 'lshw -C storage -json |sed -e "1i {\\n\\"storage\\":\\[" -e "$ a \]}" -e "s/[ ]\+//g" -e "s/}{/},{/g" -e "/^$/d"'

storage_dev_dict = json.loads(shell_run(cmd))['storage']
#raid_dev_list = filter(lambda x : x['configuration']['driver']== raid_type, storage_dev_dict)
raid_dev_list = filter(lambda x : 'raid' in x['configuration']['driver'], storage_dev_dict)

result = 'logical_name,product_version,vendor,discription\n'

for raid_dev_info in raid_dev_list:
    name = raid_dev_info['logicalname']
    product = raid_dev_info['product']
    vendor = raid_dev_info['vendor']
    description = raid_dev_info['description']
    if name:
        result += ','.join([name,product,vendor,description]) + '\n'
    else:
        result += 'not found\n'

f = open(raid_report_file, 'w')
f.write(result)
f.close()

#num_of_raid_sh = "lspci | grep -i 'raid bus controller' | wc -l"
#pci_buses_sh = "lspci | grep -i 'raid bus controller' | awk '{print $1}'"
#
#vendor_sh = ("grep -B4 %s lshw.tmp.txt | grep vendor | awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % pci_bus)
#product_sh = ("grep -B4 %s lshw.tmp.txt | grep product | awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % pci_bus)
#
#raid_info['vendor'] = vendors[index]
#raid_info['product'] = products[index]
#result_dict['RAID'].append(raid_info)
