#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, json, time, re, os
from core.colors import colors

def linkedin2usernames(users,out_dir):

    out_dir = out_dir + '/linkedin_userames'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    names = []    
    for user in users:
        name = user.get("name")
        names.append(str(name))
    write_files(out_dir,clean_names(names))

def remove_accents(raw_text):
    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ß]", 'ss', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text
        
def clean_names(raw_list):

    clean_list = []
    allowed_chars = re.compile('[^a-zA-Z -]')
    for name in raw_list:
        name = name.lower()
        name = remove_accents(name)
        name = allowed_chars.sub('', name)
        name = re.sub(r'\s+', ' ', name).strip()
        if name and name not in clean_list:
            clean_list.append(name)
    return clean_list

def write_files(out_dir,name_list):

    files = {}
    files['rawnames'] = open(out_dir + '/rawnames.txt', 'w')
    files['f.last'] = open(out_dir + '/f.last.txt', 'w')
    files['flast'] = open(out_dir + '/flast.txt', 'w')
    files['firstl'] = open(out_dir + '/firstl.txt', 'w')
    files['firstlast'] = open(out_dir + '/first.last.txt', 'w')
    files['fonly'] = open(out_dir + '/first.txt', 'w')
    files['lastf'] = open(out_dir + '/lastf.txt', 'w')

    for name in name_list:
        files['rawnames'].write(name + '\n')

        parse = re.split(' |-', name)
        try:
            if len(parse) > 2:
                first, second, third = parse[0], parse[-2], parse[-1]
                files['flast'].write(first[0] + second + '\n')
                files['flast'].write(first[0] + third + '\n')
                files['f.last'].write(first[0] + '.' + second + '\n')
                files['f.last'].write(first[0] + '.' + third + '\n')
                files['lastf'].write(second + first[0] + '\n')
                files['lastf'].write(third + first[0] + '\n')
                files['firstlast'].write(first + '.' + second + '\n')
                files['firstlast'].write(first + '.' + third + '\n')
                files['firstl'].write(first + second[0] + '\n')
                files['firstl'].write(first + third[0] + '\n')
                files['fonly'].write(first + '\n')
            else:
                first, last = parse[0], parse[-1]
                files['flast'].write(first[0] + last + '\n')
                files['f.last'].write(first[0] + '.' + last + '\n')
                files['lastf'].write(last + first[0] + '\n')
                files['firstlast'].write(first + '.' + last + '\n')
                files['firstl'].write(first + last[0] + '\n')
                files['fonly'].write(first + '\n')

        except IndexError:
            print(colors.info + " Struggled with this tricky name: '{}'."
                  .format(name) + colors.end)

    for file_name in files:
        files[file_name].close()

def saveEmails(out_dir,results):

    out_dir = out_dir + '/emails'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    file = out_dir + '/socialpwned_emails.txt'

    print(colors.info + " Writing the file..." + colors.end)
    content = ""
    with open(file, "w") as resultFile:
        for result in results:
            target = json.loads(result)
            resultFile.write(target['email']+"\n")
    resultFile.close()
    print(colors.good + " Correctly saved information...\n" + colors.end)


def saveResultsPwnDB(out_dir,results):

    out_dir = out_dir + '/pwndb'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    file = out_dir + '/socialpwned_pwndb.txt'
    passwords_file = open(out_dir + '/passwords_pwndb.txt', 'w')
    pwndb_file = open(out_dir + '/pwndb.txt', 'w')
    
    with open(file, "w") as resultFile:
        for result in results:
            leak = result.get("leak")
            if len(leak) >= 1:
                print(colors.good + " User: " + colors.V + result.get("user") + colors.B + " Email: " + colors.V + result.get("email") + colors.V + " Have Leaks " + colors.end)
                resultFile.write("User: " + result.get("user") + " Email: " + result.get("email")+"\n")
                for i in range (len(leak)-1):
                    print("\t" + colors.good + " Leaks found in PwnDB: " + colors.V + str(leak[i]) + colors.end)
                    resultFile.write("\t" + "Leaks found in PwnDB: " + str(leak[i]) + "\n")
                    
                    pwndb = json.loads(leak[i])
                    password_pwndb = pwndb.get("password")
                    info_pwndb = pwndb.get("username") + '@' + pwndb.get("domain") + ':' + password_pwndb
                    passwords_file.write(password_pwndb + "\n")
                    pwndb_file.write(info_pwndb + "\n")

                haveIBeenPwnedInfo = leak[-1]
                print("\t\t" + colors.info + " Information found in HaveIBeenPwned from pwned websites" + colors.end)
                for infoPwned  in haveIBeenPwnedInfo:
                    print("\t\t" + colors.good + " " + colors.V + infoPwned + colors.end)
                    resultFile.write("\t\t" + infoPwned + "\n")
            else:
                print(colors.good + " User: " + colors.W + result.get("user") + colors.B + " Email: " + colors.W + result.get("email") + colors.B + " Not Have Leaks in PwnDB" + colors.end)
    resultFile.close()
    passwords_file.close()
    pwndb_file.close()

def saveResultsDehashed(out_dir,results):

    out_dir = out_dir + '/dehashed'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    file = out_dir + '/socialpwned_dehashed.txt'
    raw_file = open(out_dir + '/raw_dehashed.txt', 'w')

    with open(file, "w") as resultFile:
        for result in results:
            for item in result:
                email = item.get("email")
                password = item.get("password")
                if password =='':
                    password = "Not Found"
                hashed_password = item.get("hashed_password")
                if hashed_password == '':
                    hashed_password = "Not Found"
                database_name = item.get("database_name")
                if database_name == '':
                    database_name = "Not Found"
                print(colors.good + " Email: " + colors.V + email + colors.B + " Password: " + colors.V + password + colors.B + " Hashed Password: " + colors.V + hashed_password + colors.B + " Source: " + colors.V + database_name + colors.end)
                resultFile.write(email + ":" + password + ":" + hashed_password + "\n")
            raw_file.write(str(result) + "\n")

    resultFile.close()
    raw_file.close()