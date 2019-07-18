#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import shutil

# sys.path.append(os.path.dirname(sys.path[0]))

from shell_parse.shell_parse import ShellParse
# import compare_result


def deploy_code(host_list):
    with open(host_list, 'r') as hosts:
        line = hosts.readline()
        while line:
            make_dir_sh = "ssh root@{} 'mkdir /tmp/base_check/' > /dev/null 2>&1" .format(line.strip())
            # print make_dir_sh
            ShellParse.shell_parse(make_dir_sh)
            deploy_sh = "scp -r . root@{}:/tmp/base_check/ > /dev/null 2>&1 &" .format(line.strip())
            # print deploy_sh
            ShellParse.shell_parse(deploy_sh)

            line = hosts.readline()


def run_code(host_list, result_dir, config):
    with open(host_list, 'r') as hosts:
        line = hosts.readline()
        while line:
            check_deploy_sh = "ps -ef | grep 'scp -r . root@{}:/root/' | grep -v grep | wc -l"
            while True:
                time.sleep(0.1)
                check_deploy = int(ShellParse.shell_parse(check_deploy_sh))
                if check_deploy == 0:
                    break
            run_code_sh = ("ssh root@{} 'python /tmp/base_check/base_check.py /tmp/base_check/{}' "
                           "> {}/{}.json 2>/dev/null &" .format(line.strip(),
                                                                config,
                                                                result_dir,
                                                                line.strip()))
            # print run_code_sh
            ShellParse.shell_parse(run_code_sh)
            line = hosts.readline()


def wait_code_finished():
    check_code_finished_sh = ("ps -ef | grep 'ssh root@' | grep base_check.py | "
                              "grep -v grep | wc -l")
    while True:
        time.sleep(0.1)
        check_code_finished = int(ShellParse.shell_parse(check_code_finished_sh))
        if check_code_finished == 0:
            break


def rm_remote_code(host_list):
    with open(host_list, 'r') as hosts:
        line = hosts.readline()
        while line:
            make_dir_sh = "ssh root@{} 'rm -rf /tmp/base_check/' > /dev/null 2>&1" .format(line.strip())
            ShellParse.shell_parse(make_dir_sh)
            line = hosts.readline()


def usage():
    usage_info = '''
        Usage:
        python deploy_code.py <host_list> <config>
        Example:
        python deploy_code.py host_list config
        '''
    print usage_info


def main():
    if len(sys.argv) != 3:
        usage()
    else:
        host_list = sys.argv[1]
        result_dir = "../{}" .format(host_list)
        config = sys.argv[2]
        if os.path.isdir(result_dir):
            shutil.rmtree(result_dir)
        os.mkdir(result_dir)
        deploy_code(host_list)
        run_code(host_list, result_dir, config)
        wait_code_finished()
        rm_remote_code(host_list)


if __name__ == '__main__':
    main()
