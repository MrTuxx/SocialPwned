#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

socialpwned = []

class SocialPwned:

    def __init__(self,id,name = "",linkedin = {},instagram = {},twitter = {},leaks = {"pwndb":[],"dehashed":[],"ghunt":{}}):
        
        self.id = id
        self.name = name
        self.linkedin = linkedin
        self.instagram = instagram
        self.twitter = twitter
        self.leaks = leaks

        socialpwned.append(self)

    def getTargets():
        return socialpwned

    def getListOfTargets():
        return json.loads(SocialPwned.toJSON())

    def toJSON():
        return json.dumps([ob.__dict__ for ob in socialpwned], default=lambda o: o.__dict__, indent=4)

    def create_json(out_dir):
        socialpwned_json = out_dir + '/socialpwned.json'
        with open(socialpwned_json, "w") as file:
            file.write(SocialPwned.toJSON())

    def checkID(email):

        targets = SocialPwned.getListOfTargets()
        for target in targets:
            if target.get("id") == email:
                return True
        return False

    def updateLinkedin(id,linkedin_list):
        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("linkedin").update(linkedin_list)
                return True
        return False

    def updateInstagram(id,instagram_list):
        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("instagram").update(instagram_list)
                return True
        return False

    def updateTwitter(id,twitter_list):
        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("twitter").update(twitter_list)
                return True
        return False

    def updateLeaksPwnDB(id,pwndb):

        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("leaks")["pwndb"].append(pwndb)
                return True
        return False

    def updateLeaksDehashed(id,dehashed):
        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("leaks")["dehashed"].append(dehashed)
                return True
        return False

    def updateLeaksGhunt(id,ghunt):
        for pwn in socialpwned:
            if pwn.__dict__.get("id") == id:
                pwn.__dict__.get("leaks").get("ghunt").update(ghunt)
                return True
        return False
