#!/usr/bin/env python
# coding=utf-8

import getopt, sys
import commands, json

# command line arguments
help_info = '''
    -c  cpu check on
    -m  mem check on
    -s  ssh check on
    -h  hdd check on (not help!)
    -n  nvme check on
    -r  raid check on
    -a  all options above
'''

if len(sys.argv) < 2 :
    print(help_info)
    sys.exit(1)
else:
    try:
        opt_list = getopt.getopt(sys.argv[1:], 'cmshnrax:')[0]
    except:
        print(help_info)
        sys.exit(1)
#print(opt_list)


class hwCheck(object):
    """This object checks different type of hardware and return its info"""

    def run_check(self, hw_type_list):
        cmd = "lshw -json"
        ret, out = commands.getstatusoutput(cmd)
        try:
            lshw_dict = json.loads(out)
        except:
            pass
        hw_info = dict()
        cpu_info = [x for x in lshw_dict['children'][0]['children'] if x['class'] == 'processor' ]
        hw_info['CPU']= (cpu_info)
        mem_info = [x for x in lshw_dict['children'][0]['children'] if x['class'] == 'memory' ]
        hw_info['MEM']= [x for x in mem_info if x['id'] == 'memory' ]
        return hw_info

# [u'bridge', u'generic', u'communication', u'system', u'memory', u'processor']
def main():
    opt_dict = {
        '-c':'processor',
        '-m':'memory',
        '-s':'ssh',
        '-h':'hdd',
        '-n':'nvme',
        '-r':'raid',
    }
    hw_type_list = list()
    for i in opt_list:
        opt = i[0]
        if opt == '-a' :
            hw_type_list += opt_dict.values()
            break 
        elif opt_dict.has_key(opt):
            hw_type_list.append(opt_dict[opt])
        else:
            print(help_info)
            sys.exit(1)
    print(hw_type_list)
    hwc = hwCheck()
    print(hwc.run_check(hw_type_list))

if __name__ == "__main__":
    main()
