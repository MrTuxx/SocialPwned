#!/usr/bin/env python3

import json, logging, sys
from time import time
from os.path import isfile
from pathlib import Path
from ssl import SSLError

import httpx
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException as SE_TimeoutExepction

from lib.GHunt import config
from lib.GHunt.lib.utils import *
from core.colors import colors

#Disable all logs
logging.disable(sys.maxsize)

# We change the current working directory to allow using GHunt from anywhere
#os.chdir(Path(__file__).parents[0])

def get_saved_cookies():
    ''' returns cookie cache if exists '''
    if isfile(config.data_path):
        try:
            with open(config.data_path, 'r') as f:
                out = json.loads(f.read())
                cookies = out["cookies"]
                print(colors.good + " Detected stored cookies, checking it" + colors.end)
                return cookies
        except Exception:
            print(colors.bad + " Stored cookies are corrupted" + colors.end)
            return False
    print(colors.info + " No stored cookies found" + colors.end)
    return False


def get_authorization_source(cookies):
    ''' returns html source of hangouts page if user authorized '''
    req = httpx.get("https://docs.google.com/document/u/0/?usp=direct_url",
                    cookies=cookies, headers=config.headers)

    if req.status_code == 200:
        req2 = httpx.get("https://hangouts.google.com", cookies=cookies,
                         headers=config.headers)
        if "myaccount.google.com" in req2.text:
            return req.text
    return None


def save_tokens(hangouts_auth, gdoc_token, hangouts_token, internal_token, internal_auth, cookies):
    ''' save tokens to file '''
    output = {
        "hangouts_auth": hangouts_auth, "internal_auth": internal_auth,
        "keys": {"gdoc": gdoc_token, "hangouts": hangouts_token, "internal": internal_token},
        "cookies": cookies
    }
    with open(config.data_path, 'w') as f:
        f.write(json.dumps(output))


def get_hangouts_tokens(driver, cookies, tmprinter):
    ''' gets auth and hangouts token '''

    tmprinter.out(colors.info + " Setting cookies..." + colors.end)
    driver.get("https://hangouts.google.com/robots.txt")
    for k, v in cookies.items():
        driver.add_cookie({'name': k, 'value': v})

    tmprinter.out(colors.info + " Fetching Hangouts homepage..." + colors.end)
    driver.get("https://hangouts.google.com")

    tmprinter.out(colors.info + " Waiting for the /v2/people/me/blockedPeople request, it "
                  "can takes a few minutes..." + colors.end)
    try:
        req = driver.wait_for_request('/v2/people/me/blockedPeople', timeout=config.browser_waiting_timeout)
        tmprinter.out(colors.info + " Request found !" + colors.end)
        driver.close()
        tmprinter.out("")
    except SE_TimeoutExepction:
        tmprinter.out("")
        exit(colors.bad + " Selenium TimeoutException has occured. Please check your internet connection, proxies, vpns, et cetera." + colors.end)


    hangouts_auth = req.headers["Authorization"]
    hangouts_token = req.url.split("key=")[1]

    return (hangouts_auth, hangouts_token)

def drive_interceptor(request):
    global internal_auth, internal_token

    if request.url.endswith(('.woff2', '.css', '.png', '.jpeg', '.svg', '.gif')):
        request.abort()
    elif request.path != "/drive/my-drive" and "Accept" in request.headers and \
        any([x in request.headers["Accept"] for x in ["image", "font-woff"]]):
        request.abort()
    if "authorization" in request.headers and "_" in request.headers["authorization"] and \
        request.headers["authorization"]:
        internal_auth = request.headers["authorization"]

def get_internal_tokens(driver, cookies, tmprinter):
    """ Extract the mysterious token used for Internal People API
        and some Drive requests, with the Authorization header"""

    global internal_auth, internal_token

    internal_auth = ""

    tmprinter.out(colors.info + " Setting cookies..." + colors.end)
    driver.get("https://drive.google.com/robots.txt")
    for k, v in cookies.items():
        driver.add_cookie({'name': k, 'value': v})

    start = time()

    tmprinter.out(colors.info + " Fetching Drive homepage..." + colors.end)
    driver.request_interceptor = drive_interceptor
    driver.get("https://drive.google.com/drive/my-drive")

    body = driver.page_source
    internal_token = body.split("appsitemsuggest-pa")[1].split(",")[3].strip('"')

    tmprinter.out(colors.info + f" Waiting for the authorization header, it "
                    "can takes a few minutes..." + colors.end)

    while True:
        if internal_auth and internal_token:
            tmprinter.clear()
            break
        elif time() - start > config.browser_waiting_timeout:
            tmprinter.clear()
            exit(colors.bad + " Timeout while fetching the Internal tokens.\nPlease increase the timeout in config.py or try again." + colors.end)

    del driver.request_interceptor

    return internal_auth, internal_token

def check_and_gen(ghunt_SID,ghunt_SSID,ghunt_APISID,ghunt_SAPISID,ghunt_HSID):

    driverpath = get_driverpath()
    cookies_from_file = get_saved_cookies()

    tmprinter = TMPrinter()

    cookies = {"SID": ghunt_SID, "SSID": ghunt_SSID, "APISID": ghunt_APISID, "SAPISID": ghunt_SAPISID, "HSID": ghunt_HSID, "CONSENT": config.default_consent_cookie, "PREF": config.default_pref_cookie}

    new_cookies_entered = False

    if not cookies_from_file:
        new_cookies_entered = True
        print(colors.good + " Cookies obtained from the json file" + colors.end)
    else:
        # in case user wants to enter new cookies (example: for new account)
        html = get_authorization_source(cookies_from_file)
        valid = False
        if html:
            print(colors.good + " The cookies seems valid !" + colors.end)
            valid = True
        else:
            print(colors.bad + " eems like the cookies are invalid." + colors.end)
            exit(colors.bad + " Please put valid cookies. Exiting... " + colors.end)


    # Validate cookies
    if new_cookies_entered or not cookies_from_file:
        html = get_authorization_source(cookies)
        if html:
            print(colors.good + " The cookies seems valid !" + colors.end)
        else:
            exit(colors.bad + " Seems like the cookies are invalid, try regenerating them." + colors.end)
    
    # Start the extraction process

    # We first initialize the browser driver
    chrome_options = get_chrome_options_args(config.headless)
    options = {
        'connection_timeout': None,
        'verify_ssl': False
    }
    tmprinter.out(colors.info + " Starting browser..." + colors.end)
    driver = webdriver.Chrome(
        executable_path=driverpath, seleniumwire_options=options,
        chrome_options=chrome_options
    )
    driver.header_overrides = config.headers

    print(colors.info + " Extracting the tokens..." + colors.end)
    # Extracting Google Docs token
    trigger = '\"token\":\"'
    if trigger not in html:
        exit(colors.bad +" I can't find the Google Docs token in the source code..." + colors.end)
    else:
        gdoc_token = html.split(trigger)[1][:100].split('"')[0]
        print(colors.info + " Google Docs Token => {}".format(gdoc_token) + colors.end)

    # Extracting Internal People API tokens
    internal_auth, internal_token = get_internal_tokens(driver, cookies, tmprinter)
    print(colors.info + f" Internal APIs Token => {internal_token}" + colors.end)
    print(colors.info + f" Internal APIs Authorization => {internal_auth}" + colors.end)

    # Extracting Hangouts tokens
    auth_token, hangouts_token = get_hangouts_tokens(driver, cookies, tmprinter)
    print(colors.info + f" Hangouts Authorization => {auth_token}" + colors.end)
    print(colors.info + f" Hangouts Token => {hangouts_token}" + colors.end)

    save_tokens(auth_token, gdoc_token, hangouts_token, internal_token, internal_auth, cookies)
