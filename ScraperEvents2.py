# Python Event Scraper for BSC24
# James Kincell May 2024


import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import csv
import datetime

PaidTextList = []
PaidLinkList = []
FreeTextList = []
FreeLinkList = []

print("Processing links from main page... ", end="")

#Get the main event page source
from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth('JamesDummy', '#PasswordRemoved#')
page = requests.get('https://www.outdoorlads.com/events/BSC24', auth=basic)

#Load into BS HTML Parser to find main content
soup = BeautifulSoup(page.content, "html.parser")
eventContent = soup.find("div", class_="field field-description")

#Convert to a string ready for stripping
eventContentString = str(eventContent)

#Search for the content in the Paid Activities Section
PaidActivitiesStart = eventContentString.find("Paid Activities")
PaidActivitiesEnd = eventContentString.find("Free Activities")

#Save to a string
PaidActivities = eventContentString[PaidActivitiesStart:PaidActivitiesEnd]

#Search for the content in the Free Activities Section
FreeActivitiesStart = eventContentString.find("Free Activities")
FreeActivitiesEnd = eventContentString.find("On-site Activities")

#Save to a string
FreeActivities = eventContentString[FreeActivitiesStart:FreeActivitiesEnd]

#Load Paid Activities chunk into BS
soup = BeautifulSoup(PaidActivities, "html.parser")

#Find the links and their text
PaidLinks = soup.find_all("a")
#print(PaidLinks)

#Put the links into a list
for link in PaidLinks:
    #print("Link:", link.get("href"), "Text:", link.string)
    #PaidTextList.append(link.string)
    PaidLinkList.append(link.get("href"))

#Load Free Activities chunk into BS
soup = BeautifulSoup(FreeActivities, "html.parser")

#Find the links and their text
FreeLinks = soup.find_all("a")

#Put the links into a list
for link in FreeLinks:
    #print("Link:", link.get("href"), "Text:", link.string)
    FreeLinkList.append(link.get("href"))

#Get the list lengths
PaidLength = len(PaidLinkList)
FreeLength = len(FreeLinkList)

print("Done.")

print("Writing Saturday Paid Events... ", end="")

#Write the Sat Paid Events to a csv
with open('PaidEventsSat.csv', mode='w', newline='') as PaidEventsSat_file:
    PaidEventsSat_writer = csv.writer(PaidEventsSat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    PaidEventsSat_writer.writerow(["Event Name", "# Attending", "#Spaces"])
    for x in range(PaidLength):
        page = requests.get(PaidLinkList[x], auth=basic)
        soup = BeautifulSoup(page.content, "html.parser")
        eventName = soup.find("div", class_="field title")
        attending = soup.find("div", class_="event__attending")
        attending2 = [int(s) for s in re.findall(r'\b\d+\b', str(attending))]
        if "Sat" in eventName.string:
            PaidEventsSat_writer.writerow([eventName.string, attending2[0], attending2[1]])
    now = datetime.datetime.now()
    updateText = 'Last Updated: ' + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    PaidEventsSat_writer.writerow([updateText])
print("Done.")

print("Writing Sunday Paid Events...", end="")

with open('PaidEventsSun.csv', mode='w', newline='') as PaidEventsSun_file:
    PaidEventsSun_writer = csv.writer(PaidEventsSun_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    PaidEventsSun_writer.writerow(["Event Name", "# Attending", "#Spaces"])
    for x in range(PaidLength):
        page = requests.get(PaidLinkList[x], auth=basic)
        soup = BeautifulSoup(page.content, "html.parser")
        eventName = soup.find("div", class_="field title")
        attending = soup.find("div", class_="event__attending")
        attending2 = [int(s) for s in re.findall(r'\b\d+\b', str(attending))]
        if "Sun" in eventName.string:
            PaidEventsSun_writer.writerow([eventName.string, attending2[0], attending2[1]])
    now = datetime.datetime.now()
    updateText = 'Last Updated: ' + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    PaidEventsSun_writer.writerow([updateText])
print("Done.")

print("Writing Saturday Free Events... ", end="")

#write the Free Events to a csv
with open('FreeEventsSat.csv', mode='w', newline='') as FreeEventsSat_file:
    FreeEventsSat_writer = csv.writer(FreeEventsSat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    FreeEventsSat_writer.writerow(["Event Name", "# Attending", "#Spaces"])
    for x in range(FreeLength):
        page = requests.get(FreeLinkList[x], auth=basic)
        soup = BeautifulSoup(page.content, "html.parser")
        eventName = soup.find("div", class_="field title")
        attending = soup.find("div", class_="event__attending")
        attending2 = [int(s) for s in re.findall(r'\b\d+\b', str(attending))]
        if "Sat" in eventName.string:
            FreeEventsSat_writer.writerow([eventName.string, attending2[0], attending2[1]])
    now = datetime.datetime.now()
    updateText = 'Last Updated: ' + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    FreeEventsSat_writer.writerow([updateText])
print("Done.")

print("Writing Sunday Free Events...", end="")
with open('FreeEventsSun.csv', mode='w', newline='') as FreeEventsSun_file:
    FreeEventsSun_writer = csv.writer(FreeEventsSun_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    FreeEventsSun_writer.writerow(["Event Name", "# Attending", "#Spaces"])
    for x in range(PaidLength):
        page = requests.get(FreeLinkList[x], auth=basic)
        soup = BeautifulSoup(page.content, "html.parser")
        eventName = soup.find("div", class_="field title")
        attending = soup.find("div", class_="event__attending")
        attending2 = [int(s) for s in re.findall(r'\b\d+\b', str(attending))]
        if "Sun" in eventName.string:
            FreeEventsSun_writer.writerow([eventName.string, attending2[0], attending2[1]])
    now = datetime.datetime.now()
    updateText = 'Last Updated: ' + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    FreeEventsSun_writer.writerow([updateText])
print("Done.")

print("Script Finished.")

