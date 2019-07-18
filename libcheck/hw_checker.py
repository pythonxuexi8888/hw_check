#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json

sys.path.append(os.path.dirname(sys.path[0]))
from shell_parse.shell_parse import ShellParse 

class Checker(object):
    """A checker object intended to be subclassed for your own use"""
    def __init__(self, cmd_dict):
        self.check_cmd = cmd_dict 
        # run each cmd and tag return with a label
        self.infos    = 
