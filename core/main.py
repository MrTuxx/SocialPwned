#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import argparse
import json
import re
import os
import time
import random
from lib.InstagramAPI import InstagramAPI

### Delay in seconds ###
min_delay = 1
max_delay = 5

G, B, R, W, M, C, end = '\033[92m', '\033[94m', '\033[91m', '\x1b[37m', '\x1b[35m', '\x1b[36m', '\033[0m'
info = end + W + "[-]" + W
good = end + G + "[+]" + C
bad = end + R + "[" + W + "!" + R + "]"


def run(args):
    
    api = InstagramAPI(args.user,args.password)
    print(args)
    if (api.login()):
        print(good + "Login Success!")
    else:
        print(bad + "Can't Login!")