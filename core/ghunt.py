#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from pathlib import Path

from lib.GHunt.lib.utils import *
from lib.GHunt.modules.doc import doc_hunt
from lib.GHunt.modules.email import email_hunt
from lib.GHunt.modules.gaia import gaia_hunt
from lib.GHunt.modules.youtube import youtube_hunt
from lib.GHunt.check_and_gen import check_and_gen
from core.colors import colors

def checkAndGen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID):
    check_and_gen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID)


def emailHunt(email):
    email_hunt(email)