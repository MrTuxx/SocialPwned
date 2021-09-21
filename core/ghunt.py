#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json
from pathlib import Path

from lib.GHunt.lib.utils import *
from lib.GHunt.modules.email import email_hunt
from lib.GHunt.check_and_gen import check_and_gen
from core.colors import colors

def checkAndGen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID):
    check_and_gen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID)

def emailHunt(email):
    print(colors.info + " Extracting information from email: " + email + colors.end)
    email_hunt(email)

def emailsListHunt(emails):

    for email in emails:
        item = json.loads(email)
        mail = item.get("email")
        emailHunt(mail)