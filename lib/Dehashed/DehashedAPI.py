#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json
from core.colors import colors


def dehashedRequest(dehashed_email,dehashed_apikey,emails):

    results = []

    for email in emails:
        item = json.loads(email)
        mail = item.get("email")
        user = item.get("user")
        print(colors.info + " Searching: " + mail + colors.end)

        result = dehashedSearch(dehashed_email,dehashed_apikey,email=mail)
        if result != False and result != None:
            results.append(result)

    return results

def dehashedSearch(dehashed_email,dehashed_apikey,email=None,phone=None,username=None,name=None):

    headers = {
    'Accept': 'application/json',
    }

    params = (
        ('query', 'email:' + email +'&size=100'),
    )
    response = requests.get('https://api.dehashed.com/search', headers=headers, params=params, auth=(dehashed_email, dehashed_apikey))
    result = json.loads(response.text)
    if response.status_code != 200:
        print(colors.bad + " The request was not successful for the email: " + colors.W + email + colors.end)
        print(colors.info + " " + result.get("message") + colors.end)
        return False
    return result.get("entries")