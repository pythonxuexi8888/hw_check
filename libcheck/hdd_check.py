#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


class HDDCheck(object):
    """This script check hdd information"""

    def hdd_check(self):

        devices_sh = "lsblk | grep disk | grep sd | awk '{print $1}'"
        devices = ShellParse.shell_parse(devices_sh)
        # print devices

        sizes = list()  # disk size
        vendors = list()  # disk vendor
        versions = list()  # disk version

        if isinstance(devices, str):
            tmp = []
            tmp.append(devices)
            devices = tmp
        # print "HDD numbers:", len(devices)
        for device in devices:
            size_sh = ("grep -A3 '/dev/%s$' lshw.tmp.txt | grep 'size:' | "
                       "awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % device)
            size = ShellParse.shell_parse(size_sh)
            sizes.append(size)

            vendor_sh = ("grep -B4 '/dev/%s$' lshw.tmp.txt | grep vendor | "
                         "awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % device)
            vendor = ShellParse.shell_parse(vendor_sh)
            vendors.append(vendor)

            version_sh = ("grep -B4 '/dev/%s$' lshw.tmp.txt | grep product | "
                          "awk -F: '{print $2}' | sed 's/^[ \t]*//g'" % device)
            version = ShellParse.shell_parse(version_sh)
            versions.append(version)

        result_dict = {'HDD': []}
        for index in xrange(len(devices)):
            hdd_info = {}
            hdd_info['device'] = devices[index]
            hdd_info['size'] = sizes[index]
            hdd_info['vendor'] = vendors[index]
            hdd_info['version'] = versions[index]
            result_dict['HDD'].append(hdd_info)
        return result_dict


def main():
    os.popen("lshw > lshw.tmp.txt")
    check = HDDCheck()
    results = check.hdd_check()
    print json.dumps(results, indent=2, sort_keys=True)
    os.remove("lshw.tmp.txt")


if __name__ == "__main__":
    main()
