#!/usr/bin/env python
# -*- coding: utf-8 -*-

class colors:
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    G, Y, R, W, V, B, end = '\033[92m', '\033[93m', '\033[91m', '\x1b[37m', '\033[95m', '\033[94m', '\033[0m'
    info = end + W + "[-]" + W
    good = end + G + "[+]" + B
    bad = end + R + "[" + W + "!" + R + "]"