# SocialPwned
<p align="right">
  <a href=https://github.com/MrTuxx/SocialPwned/blob/master/docs/LEEME.md>Spanish🗨</a>
</p>

![SocialPwned](https://github.com/MrTuxx/SocialPwned/blob/master/docs/images/SocialPwned.PNG "SocialPwned Welcome")

[![Python 3.6|3.7|3.8](https://img.shields.io/badge/Python-3.6%2F3.7%2F3.8-blue.svg)](https://www.python.org/download/releases/3.0/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/MrTuxx/SocialPwned/blob/master/LICENSE) 

<p align="justify">
  SocialPwned is an OSINT tool that allows to get the emails, from a target, published in social networks like Instagram, Linkedin and Twitter to find the possible credential leaks in PwnDB.
</p>
<p align="justify">
  The purpose of this tool is to facilitate the search for vulnerable targets during the phase of Footprinting in an Ethical Hacking. It is common for employees of a company to publish their emails in social networks, either professional or personal, so if these emails have their credentials leaked, it is possible that the passwords found have been reused in the environment to be audited. If it’s not the case, at least you would have an idea of the patterns that follow this target to create the passwords and be able to perform other attacks with a higher level of effectiveness.
</p>

SocialPwned uses different modules:

- **Instragram**: Making use of the unofficial [Instagram API](https://github.com/LevPasha/Instagram-API-python) from @LevPasha , different methods were developed to obtain the emails published by users. An Instagram account is required.
- **Linkedin**: Using @tomquirk's unofficial [Linkedin API](https://github.com/tomquirk/linkedin-api), different methods were developed to obtain a company's employees and their contact information (email, twitter or phone). In addition, it is possible to add the employees found to your contacts, so that you can later have access to their network of contacts and information. A Linkedin account is required.
- **Twint**: Using [Twint](https://github.com/twintproject/twint) from @twintproject you can track all the Tweets published by a user looking for some email. A Twitter account is not necessary.
- **PwnDB**: Inspired by the tool [PwnDB](https://github.com/davidtavarez/pwndb) created by @davidtavarez  a module has been developed that searches for all credential leaks from the emails found. In addition, for each email a POST request is made to [HaveIBeenPwned](https://haveibeenpwned.com/) to find out the source of the leak.

## Installation 🛠

The installation of **Tor** depends on your system. On a Debian:
```
sudo apt-get install tor
/etc/init.d/tor start
```
>NOTE: tor service must be up and running to be connected to port 9050

Clone the repository using **Git**:
```
git clone https://github.com/MrTuxx/SocialPwned.git
cd SocialPwned
pip3 install -r requirements.txt
```
