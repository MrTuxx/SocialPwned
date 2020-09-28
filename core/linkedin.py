#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, json, time
from core.colors import colors
from lib.LinkedInAPI import Linkedin
from lib.PwnDB import PwnDB

def getCompanyInformation(api,companyID):

    info = api.get_company(companyID)
    locations = info['confirmedLocations']
    for location in locations:
        country = str(location.get("country"))
        area = str(location.get("geographicArea"))
        city = str(location.get("city"))
        postalCode = str(location.get("postalCode"))
        print(colors.good + " Country: " + colors.W + country + colors.B + " Area: " + colors.W + area + colors.B + " City: " + colors.W + city + colors.B + " Postal Code: " + colors.W + postalCode + colors.end ) 

def getEmployeesFromCurrentCompany(api,companyID):
    return api.search_people(current_company=[str(companyID)])

def getEmployeesFromPastCompany(api,companyID):
    return api.search_people(past_companies=[str(companyID)])

def getEmailsFromUsers(api,employees):

    results = []
    for employee in employees:
        
        employeeID = str(employee.get("public_id"))
        userID = str(employee.get("urn_id"))
        info = getContactInformation(api,employeeID)
        email = str(info.get("email"))
        twitter = str(info.get("twitter"))
        phone = str(info.get("phone"))
        print(colors.good + " User ID: " + colors.W + userID + colors.B + " Public ID of employee: " + colors.W + employeeID + colors.B + " Email: " + colors.W + email + colors.B + " Phone: " + colors.W + phone + colors.B + " Twitter: " + colors.W + twitter + colors.end)

        if email != "Not Found":
            results.append(json.dumps({"user":employeeID,"userID":userID,"email":email}))
    return results

def getCompanyEmployees(api,companies):
    targets = []
    for company in companies:
        nameCompany = company.get("name")
        employees = searchUsersOfCompany(api,nameCompany)
        if employees != [] and employees not in targets:
            targets.append(employees)
    return unionUsers(targets)

def unionUsers(targets):
    results = []
    for target in targets:
        for result in target:
            results.append(result)
    print(colors.info + " " + str(len(results)) + " different users have been found in total ^-^" + colors.end)
    return results

def searchUsers(api,query):
    print(colors.info + " Searching users... :)" + colors.end)
    items = api.search_people(keywords=query)
    
    for item in items:
        user = str(item.get("public_id"))
        userID = str(item.get("urn_id"))
        print(colors.good + " User: " + colors.W + user + colors.B + " userID: " + colors.W + userID + colors.end)
    print(colors.info + " " + str(len(items)) + " users have been found ^-^" + colors.end)
    return items

def searchCompanies(api,query):
    print(colors.info + " Searching companies... :)" + colors.end)
    items = api.search_companies(query)
    
    for item in items:
        nameCompany = str(item.get("name"))
        companyID = str(item.get("urn_id"))
        numberEmployees = str(item.get("subline"))
        print(colors.good + " Name: " + colors.W + nameCompany + colors.B + " company ID: " + colors.W + companyID + colors.B + " Number of employees: " + colors.W + numberEmployees + colors.end)
    print(colors.info + " " + str(len(items)) + " companies have been found ^-^" + colors.end)
    return items

def searchUsersOfCompany(api,nameCompany):
    print(colors.info + " Searching employees of company: " + nameCompany + colors.end)
    employees = api.search_people(keywords=nameCompany)
    print(colors.info + " " + str(len(employees)) + " employees have been found ^-^" + colors.end)
    
    return employees

def getUserInformation(api,publicID):
    results = []
    # profile = api.get_profile(publicID)
    # print(profile)
    info = getContactInformation(api,publicID)
    email = str(info.get("email"))
    twitter = str(info.get("twitter"))
    phone = str(info.get("phone"))
    print(colors.good + " User: " + colors.W + publicID + colors.B + " Email: " + colors.W + email + colors.B + " Phone: " + colors.W + phone + colors.B + " Twitter: " + colors.W + twitter + colors.end)

    if email != "Not Found":
        results.append(json.dumps({"user":publicID,"userID":"Not-Found","email":email}))
    return results


def getContactInformation(api,publicID):

    print(colors.info + " Searching user contact information: " + publicID)
    info = api.get_profile_contact_info(publicID)
    email = ''
    twitter = ''
    phone = ''
    if info.get("email_address") == None:
        email = "Not Found"
    else:
        email = info.get("email_address")

    if info.get("twitter") == []:
        twitter = "Not Found"
    else:
        twitter = str(info.get("twitter")[0].get("name"))
    if info.get("phone_numbers") == []:
        phone = "Not Found"
    else:
        phone = info.get("phone_numbers")[0].get("number")

    return {"email":email,"twitter":twitter,"phone":phone}

def sendContactRequestAListOfUsers(api, users):

    for user in users:
        userID = user.get("urn_id")
        sendContactRequest(api,userID)
    
def sendContactRequest(api, userID):

    response = api.add_connection(userID)
    if response == 201:
        print(colors.good + " Contact request successfully" + colors.end)
    else:
        print(colors.bad + " Contact request unsuccessfully" + colors.end)
    
    return response

def getFollowers(api, userID):
    print(colors.info + " Getting contacts..." + colors.end)
    followers = api.get_profile_connections(userID)
    print(colors.info + " " + str(len(followers)) + " contacts have been found ^-^" + colors.end)
    return followers

def getMyContacts(api):
    print(colors.info + " Getting your contacts..." + colors.end)
    userID = getMyUserID(api)
    followers = getFollowers(api,userID)
    print(colors.info + " " + str(len(followers)) + " contacts have been found ^-^" + colors.end)
    return followers


def getMyUserID(api):
    profile = api.get_current_profile()
    return profile.get("message_id")

def getMyPublicID(api):
    profile = api.get_current_profile()
    return profile.get("publicIdentifier")
