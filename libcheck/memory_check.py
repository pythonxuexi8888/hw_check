#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


class MemoryCheck(object):
    """This script check memory information"""

    def memory_check(self):

        # memory numbers
        num_of_memory_sh = "dmidecode -t 17 | grep Size | grep -v 'No Module Installed' | wc -l"
        num_of_memory = ShellParse.shell_parse(num_of_memory_sh)

        # memory size
        sizes_sh = ("dmidecode -t 17 | grep Size | grep -v 'No Module Installed' | "
                    "awk -F: '{print $2}' | sed 's/[ \t]*//g'")
        sizes = ShellParse.shell_parse(sizes_sh)

        # memory speed
        speeds_sh = ("dmidecode -t 17 | grep Speed | grep -v -E 'Unknown|Clock' | "
                     "awk -F: '{print $2}' | sed 's/[ \t]*//g'")
        speeds = ShellParse.shell_parse(speeds_sh)

        # memory slot
        slots_sh = ("dmidecode -t 17 | grep -A3 Size | grep -v 'No Module Installed' | "
                    "grep -E 'Size:|Locator:' | sed -n '/Size:/,+1p' | grep 'Locator:' | awk -F: '{print $2}'"
                    " | sed 's/^[ \t]*//g'")
        slots = ShellParse.shell_parse(slots_sh)

        # memory channel
        channels_sh = ("dmidecode -t 17 | grep -A4 Size | grep -v 'No Module Installed' | "
                       "grep -E 'Size:|Bank Locator:' | sed -n '/Size:/,+1p' | grep 'Bank Locator:' | "
                       "awk -F: '{print $2}' | sed 's/^[ \t]*//g'")
        channels = ShellParse.shell_parse(channels_sh)

        # memory vendor
        vendors = list()
        for slot in slots:
            vendor_sh = ("grep -B4 'slot: %s$' lshw.tmp.txt | grep 'vendor:' | awk -F: '{print $2}' | "
                         "sed 's/^[ \t]*//g'" % slot)
            vendor = ShellParse.shell_parse(vendor_sh)
            vendors.append(vendor)

        # memory version
        versions = list()
        for slot in slots:
            version_sh = ("grep -B4 'slot: %s$' lshw.tmp.txt | grep 'product:' | awk -F: '{print $2}' | "
                          "sed 's/^[ \t]*//g'" % slot)
            version = ShellParse.shell_parse(version_sh)
            versions.append(version)

        result_dict = {'Memory': []}
        for index in xrange(len(sizes)):
            memory_info = {}
            memory_info['size'] = sizes[index]
            memory_info['speed'] = speeds[index]
            memory_info['slot'] = slots[index]
            memory_info['channel'] = channels[index]
            memory_info['vendor'] = vendors[index]
            memory_info['version'] = versions[index]
            result_dict['Memory'].append(memory_info)
        return result_dict

        # numa node number
        #num_of_numa_sh = "lscpu | grep 'NUMA node(s)' | awk -F: '{print $2}' | sed 's/[ \t]*//g'"
        #num_of_numa = int(ShellParse.shell_parse(num_of_numa_sh))
        # memmory channel number
        #num_of_channel_sh = ("dmidecode -t 17 | grep -A4 Size | grep -v 'No Module Installed' | "
                             #"grep -E 'Size|Locator' | sed -n '/Size:/,+1p' | grep 'Locator' | "
                             #"awk '{print $3}' | sort -u | wc -l")
        #num_of_channel = int(ShellParse.shell_parse(num_of_channel_sh))
        # memory number of each channel
        #num_of_mems = list()
        #for node in xrange(num_of_numa):
            #for channel in xrange(num_of_channel):
         #   num_of_mem_sh = ("dmidecode -t 17 | grep -A4 Size | grep -v 'No Module Installed'"
         #                    " | grep -E 'Size|Locator' | sed -n '/Size:/,+1p' | grep 'Locator' | "
         #                    "awk '$2==" + str(node+1) + " {print $2 $3 $4 $5}' |"
         #                    " wc -l") # " && $6==" + str(channel) +
          #  num_of_mem = int(ShellParse.shell_parse(num_of_mem_sh))
           # num_of_mems.append(num_of_mem)
            #print "NUMA node %d has %d memory(s)" % (node+1, num_of_mem)
        #num_of_mems.sort()
        #if num_of_mems[0] == num_of_mems[-1]:
        #    print "It's OK!"
        #else:
        #    print "It's invalid!"


def main():
    os.popen("lshw > lshw.tmp.txt")
    check = MemoryCheck()
    results = check.memory_check()
    print json.dumps(results, indent=2, sort_keys=True)
    os.remove("lshw.tmp.txt")

if __name__ == "__main__":
    main()
