#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

# sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse


def install_deps(host_list):
    with open(host_list, 'r') as hosts:
        line = hosts.readline()
        while line:
            nvme_sh = "scp /home/dongrui/nvme-cli-1.3-1.el7.x86_64.rpm root@{}:~/" .format(line.strip())
            # print nvme_sh
            ShellParse.shell_parse(nvme_sh)
            install_nvme_sh = "ssh root@{} 'yum localinstall nvme-cli-1.3-1.el7.x86_64.rpm -y' > /dev/null 2>&1 &" .format(line.strip())
            # print install_nvme_sh
            ShellParse.shell_parse(install_nvme_sh)
            install_sh = "ssh root@{} 'yum install lshw pciutils -y' > /dev/null 2>&1 &" .format(line.strip())
            # print install_sh
            res = ShellParse.shell_parse(install_sh)
            # print res
            line = hosts.readline()


def usage():
    usage_info = '''
        Usage:
        python install_deps.py <host_list>
        Example:
        python install_deps.py host_list.txt
        '''
    print usage_info


def main():
    if len(sys.argv) != 2:
        usage()
    else:
        install_deps(sys.argv[1])

if __name__ == '__main__':
    main()
