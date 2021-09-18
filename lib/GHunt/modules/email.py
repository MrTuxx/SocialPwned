#!/usr/bin/env python3

import json
import sys
import os
from datetime import datetime
from io import BytesIO
from os.path import isfile
from pathlib import Path
from pprint import pprint

import httpx
from PIL import Image
from geopy.geocoders import Nominatim

from lib.GHunt import config
import lib.GHunt.lib.gmaps as gmaps
import lib.GHunt.lib.youtube as ytb
from lib.GHunt.lib.photos import gpics
from lib.GHunt.lib.utils import *
import lib.GHunt.lib.calendar as gcalendar
from core.colors import colors

def email_hunt(email):

    if not email:
        exit(colors.bad + " Please give a valid email.\nExample : larry@google.com" + colors.end)

    if not isfile(config.data_path):
        exit(colors.bad + " Please generate cookies and tokens first, with the check_and_gen.py script." + colors.end)

    hangouts_auth = ""
    hangouts_token = ""
    internal_auth = ""
    internal_token = ""

    cookies = {}

    with open(config.data_path, 'r') as f:
        out = json.loads(f.read())
        hangouts_auth = out["hangouts_auth"]
        hangouts_token = out["keys"]["hangouts"]
        internal_auth = out["internal_auth"]
        internal_token = out["keys"]["internal"]
        cookies = out["cookies"]

    client = httpx.Client(cookies=cookies, headers=config.headers)

    data = is_email_google_account(client, hangouts_auth, cookies, email,
                                   hangouts_token)

    is_within_docker = within_docker()
    geolocator = Nominatim(user_agent="nominatim")
    print(colors.good + f" {len(data['matches'])} account found !" + colors.end)

    for user in data["matches"]:
        print("\n------------------------------\n")

        gaiaID = user["personId"][0]
        email = user["lookupId"]
        infos = data["people"][gaiaID]

        # get name & profile picture
        account = get_account_data(client, gaiaID, internal_auth, internal_token, config)
        name = account["name"]
        
        if name:
            print(colors.info + f" Name : {name}" + colors.end)
        else:
            if "name" not in infos:
                print(colors.info + " Couldn't find name" + colors.end)
            else:
                for i in range(len(infos["name"])):
                    if 'displayName' in infos['name'][i].keys():
                        name = infos["name"][i]["displayName"]
                        print(colors.info + f" Name : {name}" + colors.end)

        # profile picture
        profile_pic_url = account["profile_pic_url"]
        req = client.get(profile_pic_url)

        print(colors.good + f" Profile picture: {profile_pic_url}" + colors.end)

        profile_pic_img = Image.open(BytesIO(req.content))
        profile_pic_hash = image_hash(profile_pic_img)
        is_default_profile_pic = detect_default_profile_pic(profile_pic_hash)

        # last edit
        try:
            timestamp = int(infos["metadata"]["lastUpdateTimeMicros"][:-3])
            last_edit = datetime.utcfromtimestamp(timestamp).strftime("%Y/%m/%d %H:%M:%S (UTC)")
            print(colors.info + f" Last profile edit : {last_edit}" + colors.end)
        except KeyError:
            last_edit = None
            print(colors.info + f" Last profile edit : Not found" + colors.end)
        print(colors.info + f" Email : {email}\n" + colors.info + f" Google ID : {gaiaID}" + colors.end)

        # is bot?
        if "extendedData" in infos:
            isBot = infos["extendedData"]["hangoutsExtendedData"]["isBot"]
            if isBot:
                print(colors.info + " Hangouts Bot : Yes !" + colors.end)
            else:
                print(colors.info + " Hangouts Bot : No" + colors.end)
        else:
            print(colors.info + " Hangouts Bot : Unknown" + colors.end)

        # decide to check YouTube
        ytb_hunt = False
        try:
            services = [x["appType"].lower() if x["appType"].lower() != "babel" else "hangouts" for x in
                        infos["inAppReachability"]]
            if name and (config.ytb_hunt_always or "youtube" in services):
                ytb_hunt = True
            print(colors.good + " Activated Google services :" + colors.end)
            print('\n'.join(["- " + x.capitalize() for x in services]))

        except KeyError:
            ytb_hunt = True
            print(colors.info + " Unable to fetch connected Google services." + colors.end)

        # check YouTube
        if name and ytb_hunt:
            confidence = None
            data = ytb.get_channels(client, name, config.data_path,
                                   config.gdocs_public_doc)
            if not data:
                print(colors.info + " YouTube channel not found." + colors.end)
            else:
                confidence, channels = ytb.get_confidence(data, name, profile_pic_hash)
                
                if confidence:
                    print(colors.good + f" YouTube channel (confidence => {confidence}%) :" + colors.end)
                    for channel in channels:
                        print(f"- [{channel['name']}] {channel['profile_url']}")
                    possible_usernames = ytb.extract_usernames(channels)
                    if possible_usernames:
                        print(colors.good + " Possible usernames found :" + colors.end)
                        for username in possible_usernames:
                            print(f"- {username}")
                else:
                    print(colors.info + " YouTube channel not found." + colors.end)

        # TODO: return gpics function output here
        #gpics(gaiaID, client, cookies, config.headers, config.regexs["albums"], config.regexs["photos"],
        #      config.headless)

        # reviews
        reviews = gmaps.scrape(gaiaID, client, cookies, config, config.headers, config.regexs["review_loc_by_id"], config.headless)

        if reviews:
            confidence, locations = gmaps.get_confidence(geolocator, reviews, config.gmaps_radius)
            print(colors.good + f" Probable location (confidence => {confidence}) :" + colors.end)

            loc_names = []
            for loc in locations:
                loc_names.append(
                    f"- {loc['avg']['town']}, {loc['avg']['country']}"
                )

            loc_names = set(loc_names)  # delete duplicates
            for loc in loc_names:
                print(loc)
        
        
       # Google Calendar
        calendar_response = gcalendar.fetch(email, client, config)
        if calendar_response:
            print(colors.good + " Public Google Calendar found !" + colors.end)
            events = calendar_response["events"]
            if events:
                gcalendar.out(events)
            else:
                print(colors.info + " No recent events found." + colors.end)
        else:
            print(colors.info + " No public Google Calendar." + colors.end)
        