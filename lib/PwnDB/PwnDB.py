#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, time, random, sys, scrapy, re
from scrapy.selector import Selector
from core.colors import colors

def haveIBeenPwned(email):
    
    url = 'https://haveibeenpwned.com:443/account/'+str(email)
    payload = ""
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Connection": "close",
        "Host": "haveibeenpwned.com",
        "Accept-Encoding": "gzip, deflate", 
        "Upgrade-Insecure-Requests": "1",
        "Accept-Language": "en-US,en;q=0.5"
        }

    print(colors.info + " Searching information about Leaks found :)" + colors.end)

    try:
        response = requests.request("GET", url, data=payload, headers=headers, verify=False)
        response = Selector(response)
        pwned = response.xpath('//div[@class="pwnedSearchResult pwnedRow panel-collapse in"]/div[@class="container"]/div[@class="row pwnResultBanner"]/div[@class="pwnTitle"]/h2/text()').get()
        no_pwned = response.xpath('//div[@class="pwnedSearchResult panel-collapse in"]/div[@class="container"]/div[@class="row pwnResultBanner"]/div[@class="pwnTitle"]/h2/text()').get()

        infoAboutLeak = []
        if pwned:
            print(colors.info + " Sources Found" + colors.end)
            sources = response.xpath('//div[@id="pwnedSites"]/div/@id').getall()
            descriptions = response.xpath('//div[@id="pwnedSites"]/div[@class="pwnedSearchResult pwnedWebsite panel-collapse in"]/div[@class="container"]/div[@class="row"]/div[@class="col-sm-10"]').xpath('.//p')

            for idx, description in enumerate(descriptions):
                text = description.get()
                if (idx % 2) == 0:
                    index_source = idx // 2
                    text = striphtml(text)
                    infoAboutLeak.append(json.dumps({'Source': sources[index_source], 'Description': text}))      
        else:
            print(colors.info + " Sources not Found" + colors.end)
    except Exception as e:
        print(e)
        infoAboutLeak.append(" Sources not found")
    
    return infoAboutLeak

def striphtml(data):
	data = data.replace('\n',' ')
	data = data.replace('"','')
	pattern = re.compile(r'<.*?>')
	return pattern.sub('', data)

def parsePwndbResponse(mail,text):
    if "Array" not in text:
        return None

    leaks = text.split("Array")[1:]
    emails = []
    foundLeak = False

    for leak in leaks:
        leaked_email = ''
        domain = ''
        password = ''
        try :
            leaked_email = leak.split("[luser] =>")[1].split("[")[0].strip()
            domain = leak.split("[domain] =>")[1].split("[")[0].strip()
            password = leak.split("[password] =>")[1].split(")")[0].strip()
        except:
            pass
        if leaked_email != "donate" and domain != "btc.thx" and password != "12cC7BdkBbru6JGsWvTx4PPM5LjLX8g":
            foundLeak = True
            emails.append(json.dumps({'username': leaked_email, 'domain': domain, 'password': password}))
    
    if foundLeak:
        emails.append(haveIBeenPwned(mail))

    return emails

def findLeak(emails,tor_proxy):
    
    session = requests.session()
    session.proxies = {'http': 'socks5h://{}'.format(tor_proxy), 'https': 'socks5h://{}'.format(tor_proxy)}

    url = "http://pwndb2am4tzkvold.onion/"
    leaks = []
    
    print(colors.info + " Searching Leaks :)" + colors.end)
    for email in emails:

        item = json.loads(email)
        mail = item.get("email")
        poc = mail.replace("(","")
        mail = poc.replace(")","")
        user = item.get("user")
        userID = item.get("userID")
        username = mail.split("@")[0]
        domain = mail.split("@")[1]
        request_data = {'luser': username, 'domain': domain, 'luseropr': 1, 'domainopr': 1, 'submitform': 'em'}
        time.sleep(1)
        try:
            response = session.post(url, data=request_data)
        except Exception as e:
            print(colors.bad + " Can't connect to service! restart tor service and try again." + colors.end)
            print(e)
            sys.exit()
        print(colors.info + " Searching: " + mail + colors.end)
        if response.status_code == 200:
            target = {'user': user, 'userID': userID, 'email': mail, 'leak': parsePwndbResponse(mail,response.text)}
            leaks.append(target)
            print(colors.good + " The request was successful" + colors.end)
        else:
            print(response.status_code)
            print(response.text)
            print(colors.bad + " The request was not successful for the user: " + colors.W + user + colors.R + " and email: " + colors.W + mail + colors.R + ". Maybe you should increase the delay" + colors.end)

    return leaks

def saveResultsPwnDB(results):
    with open("PwnDBResults.txt", "a") as resultFile:
        for result in results:
            leak = result.get("leak")
            if len(leak) >= 1:
                print(colors.good + " User: " + colors.V + result.get("user") + colors.B + " Email: " + colors.V + result.get("email") + colors.V + " Have Leaks " + colors.end)
                resultFile.write("User: " + result.get("user") + " Email: " + result.get("email")+"\n")
                for i in range (len(leak)-1):
                    print("\t" + colors.good + " Leaks found in PwnDB: " + colors.V + str(leak[i]) + colors.end)
                    resultFile.write("\t" + "Leaks found in PwnDB: " + str(leak[i]) + "\n")

                haveIBeenPwnedInfo = leak[-1]
                print("\t\t" + colors.info + " Information found in HaveIBeenPwned from pwned websites" + colors.end)
                for infoPwned  in haveIBeenPwnedInfo:
                    print("\t\t" + colors.good + " " + colors.V + infoPwned + colors.end)
                    resultFile.write("\t\t" + infoPwned + "\n")
            else:
                print(colors.good + " User: " + colors.W + result.get("user") + colors.B + " Email: " + colors.W + result.get("email") + colors.B + " Not Have Leaks in PwnDB" + colors.end)
    resultFile.close()



