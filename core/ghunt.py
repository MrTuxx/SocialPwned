#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from pathlib import Path

from lib.GHunt.lib.utils import *
from lib.GHunt.modules.doc import doc_hunt
from lib.GHunt.modules.email import email_hunt
from lib.GHunt.modules.gaia import gaia_hunt
from lib.GHunt.modules.youtube import youtube_hunt


def emailHunt(email):
    print(email)