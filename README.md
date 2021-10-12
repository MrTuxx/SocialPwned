# SocialPwned
<p align="right">
  <a href=https://github.com/MrTuxx/SocialPwned/blob/master/docs/LEEME.md>Spanish🗨</a>
</p>

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/SocialPwned.PNG "SocialPwned Welcome")

[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/download/releases/3.0/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/MrTuxx/SocialPwned/blob/master/LICENSE) 

<p align="justify">
  SocialPwned is an OSINT tool that allows to get the emails, from a target, published in social networks like Instagram, Linkedin and Twitter to find the possible credential leaks in PwnDB or Dehashed and obtain Google account information via GHunt.
</p>
<p align="justify">
  The purpose of this tool is to facilitate the search for vulnerable targets during the phase of Footprinting in an Ethical Hacking. It is common for employees of a company to publish their emails in social networks, either professional or personal, so if these emails have their credentials leaked, it is possible that the passwords found have been reused in the environment to be audited. If it’s not the case, at least you would have an idea of the patterns that follow this target to create the passwords and be able to perform other attacks with a higher level of effectiveness.
</p>

SocialPwned uses different modules:

- **Instragram**: Making use of the unofficial [Instagram API](https://github.com/LevPasha/Instagram-API-python) from @LevPasha, different methods were developed to obtain the emails published by users. An Instagram account is required.
- **Linkedin**: Using @tomquirk's unofficial [Linkedin API](https://github.com/tomquirk/linkedin-api), different methods were developed to obtain a company's employees and their contact information (email, twitter or phone). In addition, it is possible to add the employees found to your contacts, so that you can later have access to their network of contacts and information. This module also generates different files with combinations of possible usernames for an organization. A Linkedin account is required.
- **Twint**: Using [Twint](https://github.com/twintproject/twint) from @twintproject you can track all the Tweets published by a user looking for some email. A Twitter account is not necessary.
- **PwnDB**: Inspired by the tool [PwnDB](https://github.com/davidtavarez/pwndb) created by @davidtavarez  a module has been developed that searches for all credential leaks from the emails found. In addition, for each email a POST request is made to [HaveIBeenPwned](https://haveibeenpwned.com/) to find out the source of the leak.
- **Dehashed**: Provides clear passwords and also the hash of passwords that could not be cracked. It is necessary to pay at [Dehashed](https://dehashed.com/) to get an API Key, but it can be a good alternative when PwnDB is slow or does not provide results.
- **GHunt**: Using the tool created by @mxrch, [GHunt](https://github.com/mxrch/GHunt), it is possible to obtain information related to Google mails, e.g. reviews, profile picture, possible location or public calendar events.

## Installation 🛠

### Easy way

```
$ service docker start
$ docker pull mrtuxx/socialpwned
```
>NOTE: You will need to have the docker service correctly installed.

### Manual way

The installation of **Tor** depends on your system. On a Debian:
```
$ sudo apt-get install tor
$ /etc/init.d/tor start
```
Clone the repository using **Git**:
```
$ git clone https://github.com/MrTuxx/SocialPwned.git
$ cd SocialPwned
$ pip3 install -r requirements.txt
```
For the GHunt module to work correctly you must follow these steps:

- [GHunt Manual installation](https://github.com/mxrch/GHunt#manual-installation)

## Usage

To make use of the Instagram and Linkedin features you need to have an account created on each of the social networks. The credentials must be indicated in a JSON file:
```
{
    "instagram":{
        "username":"username",
        "password":"password"
    },
    "linkedin":{
        "email":"email",
        "password":"password"
    },
    "ghunt":{
        "SID":"SID",
        "SSID":"SSID",
        "APISID":"APISID",
        "SAPISID":"SAPISID",
        "HSID":"HSID"
    },
    "dehashed":{
         "email":"email",
         "apikey":"apikey"
    }
}

```
>NOTE: The cookies necessary for the GHunt module to work can be obtained by following the steps explained [here](https://github.com/mxrch/GHunt#where-i-find-these-5-cookies-).
```
usage: socialpwned.py [-h] --credentials CREDENTIALS [--pwndb] [--tor-proxy PROXY] [--instagram] [--info QUERY]
                      [--location LOCATION_ID] [--hashtag-ig QUERY] [--target-ig USERNAME] [--search-users-ig QUERY]
                      [--my-followers] [--my-followings] [--followers-ig] [--followings-ig] [--linkedin]
                      [--company COMPANY_ID] [--search-companies QUERY] [--employees] [--my-contacts]
                      [--user-contacts USER_ID] [--search-users-in QUERY] [--target-in USERNAME] [--add-contacts]
                      [--add-a-contact USER_ID] [--twitter] [--limit LIMIT] [--year YEAR] [--since DATE]
                      [--until DATE] [--profile-full] [--all-tw] [--target-tw USERNAME] [--hashtag-tw USERNAME]
                      [--followers-tw] [--followings-tw] [--ghunt] [--email-gh email@gmail.com] [--dehashed]
                      [--email-dh email@gmail.com]
```

## Output format

Each time SocialPwned is run, a directory with the following format will be generated:

```
output
└── session_year_month_day_time
    ├── dehashed
    │   ├── raw_dehashed.txt
    │   └── socialpwned_dehashed.txt
    ├── emails
    │   └── socialpwned_emails.txt
    ├── instagram
    │   └── socialpwned_instagram.txt
    ├── linkedin_userames
    │   ├── first.last.txt
    │   ├── firstl.txt
    │   ├── first.txt
    │   ├── f.last.txt
    │   ├── flast.txt
    │   ├── lastf.txt
    │   └── rawnames.txt
    ├── pwndb
    │   ├── passwords_pwndb.txt
    │   ├── pwndb.txt
    │   └── socialpwned_pwndb.txt
    ├── socialpwned.json
    └── twitter
        └── socialpwned_twitter.txt
```
- The dehashed directory contains the raw API information in one file and the email-related passwords in another.
- The pwndb directory contains a file with only the passwords, another one with the passwords and related emails and finally a file that adds the sources of the leaks.
- The emails directory contains a file with all the emails obtained.
- The instagram directory contains a file with user accounts and their related email addresses.
- The twitter directory contains a file with user accounts and their related email addresses.
- The linkedin directory contains different files with combinations of user names obtained. Inspired by the [linkedin2usernames](https://github.com/initstring/linkedin2username) tool.
- The socialpwned.json file provides in JSON format all the information obtained by SocialPwned and its different modules. Where the ID of each item is the email, in case you have information about a user but not his email, the ID will be his unique social network identifier.

## Basic Examples and Combos 🚀

Here are some examples:

### Instagram

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/1-3.png "Users with email in Instagram")
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/1-4.png "Leaks Found")
```
python3 socialpwned.py --credentials credentials.json --instagram --info España
```
```
python3 socialpwned.py --credentials credentials.json --instagram --location 832578276
```
```
python3 socialpwned.py --credentials credentials.json --instagram --hashtag-ig someHashtag --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --followers-ig --followings-ig --pwndb
```

### Linkedin

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/2-2.png "Searching employees of a company in Linkedin")
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/2-4.png "Leaks Found")
```
python3 socialpwned.py --credentials credentials.json --linkedin --search-companies "My Target"
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --search-companies "My Target" --employees --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --company 123456789 --employees --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --company 123456789 --employees --add-contacts
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --user-contacts user-id --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --linkedin --user-contacts user-id --add-contacts
```
### Twitter
![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/3-1.png "Searching in Twitter")

```
python3 socialpwned.py --credentials credentials.json --twitter --hashtag-tw someHashtag --pwndb --limit 200
```
```
python3 socialpwned.py --credentials credentials.json --twitter --target-tw username --all-tw --pwndb
```
```
python3 socialpwned.py --credentials credentials.json --twitter --target-tw username --all-tw --followers-tw --followings-tw --pwndb
```

### Combos

```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --followers-ig --followings-ig --linkedin --company 123456789 --employees --twitter --target-tw username --all-tw --pwndb --output results.txt
```
```
python3 socialpwned.py --credentials credentials.json --instagram --target-ig username --linkedin --target-in username --twitter --target-tw username --all-tw --pwndb
```

## References

- [Instagram API](https://github.com/LevPasha/Instagram-API-python). Author: LevPasha
- [Linkedin API](https://github.com/tomquirk/linkedin-api). Author: tomquirk
- [Twint](https://github.com/twintproject/twint). Author: twintproject
- [PwnDB](https://github.com/davidtavarez/pwndb). Author: davidtavarez

## Disclaimer

The usage of SocialPwned to attack targets without prior mutual consent is illegal. In addition, it makes use of different modules that violate Linkedin and Instagram rules, therefore, you will be banned temporarily or permanently.

It is the responsibility of the end user to use SocialPwned. The developers are not responsible and are not liable for any misuse or damage caused.
