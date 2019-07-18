#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


class RAIDCheck(object):
    """This script check cpu information"""

    def raid_check(self):
        num_of_raid_sh = "lspci | grep -i 'raid bus controller' | wc -l"
        num_of_raid = int(ShellParse.shell_parse(num_of_raid_sh))
        # print "RAID bus controller numbers: ", num_of_raid

        pci_buses_sh = "lspci | grep -i 'raid bus controller' | awk '{print $1}'"
        pci_buses = ShellParse.shell_parse(pci_buses_sh)

        vendors = []
        products = []
        aList = []
        if num_of_raid == 1:
            aList.append(pci_buses)
        else:
            aList = pci_buses
        for pci_bus in aList:
            vendor_sh = ("grep -B4 %s lshw.tmp.txt | grep vendor | "
                         "awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % pci_bus)
            vendor = ShellParse.shell_parse(vendor_sh)
            vendors.append(vendor)
            product_sh = ("grep -B4 %s lshw.tmp.txt | grep product | "
                          "awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % pci_bus)
            product = ShellParse.shell_parse(product_sh)
            products.append(product)

        result_dict = {'RAID': []}
        for index in xrange(num_of_raid):
            raid_info = {}
            raid_info['vendor'] = vendors[index]
            raid_info['product'] = products[index]
            result_dict['RAID'].append(raid_info)
        return result_dict


def main():
    os.popen("lshw > lshw.tmp.txt")
    check = RAIDCheck()
    results = check.raid_check()
    print json.dumps(results, indent=2, sort_keys=True)
    os.remove("lshw.tmp.txt")

if __name__ == "__main__":
    main()
