#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.colors import colors
import os
def banner():

    picture =  """
############################
############################
## ########      ######## ##
## #####            ##### ##
## ###                ### ##
## #                    # ##
## ## #####      ##### ## ##
## ###   ####  ###    ### ##
## #       ##  ##       # ##
## # #      #  #      # # ##
##   # ####      #### #   ##
##   # #### #  # #### #   ##
##    #     #  #     #    ##
##          #  #          ##
##   #     #    #     #   ##
##  ##     #    #     ##  ##
## ###   ####  ####   ### ##
## ###################### ##
##  ####################  ##
## #  ################  # ##
## ##     #########    ## ##
## ##      ######      ## ##
## ###                ### ##
## ####              #### ##
## #####            ##### ##
############################
############################
Author: @MrTuxx
DISCLAIMER: This is only for testing purposes and can only be used where strict consent has been given. Don't be a fucking stalker.
"""

    pic = picture.split("\n")
    for line in pic:
        centered = line.center(os.get_terminal_size().columns)
        print(colors.BOLD + centered + colors.end)
