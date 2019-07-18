#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time

# sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


def remove_mine(host_list):
    with open(host_list, 'r') as hosts:
        line = hosts.readline()
        while line:
            rm_sh = "ssh root@{} 'rm -f /root/nvme-cli-1.3-1.el7.x86_64.rpm /root/lshw.tmp.txt'" .format(line.strip())
            # print rm_sh
            ShellParse.shell_parse(rm_sh)
            uninstall_sh = "ssh root@{} 'yum remove -y lshw nvme-cli pciutils'" .format(line.strip())
            # print uninstall_sh
            ShellParse.shell_parse(uninstall_sh)

            line = hosts.readline()


def main():
    host_list = sys.argv[1]
    remove_mine(host_list)


if __name__ == '__main__':
    main()
