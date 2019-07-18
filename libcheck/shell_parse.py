# -*- coding:utf-8 -*-

import os


class ShellParse(object):

    @staticmethod
    def shell_parse(shells):
        items = list()
        for line in os.popen(shells).readlines():
            line = line.strip('\n')
            items.append(line)
        if len(items) == 1:
            return items[0]
        elif len(items) == 0:
            return ""
        else:
            return items

