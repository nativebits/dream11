import json
import sys
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
'''
driver = webdriver.Chrome("C:\\Nativebits\\WebScrap\\chromedriver.exe")
driver.get("https://www.fancode.com")
print(driver.find_element_by_id("app").__getattribute__("OUTERHTML"))

markup = requests.get("https://www.fancode.com")
print(markup)
soup = BeautifulSoup("https://www.fancode.com/cricket/schedule/today")
print(soup.prettify())
'''

driver = webdriver.Chrome("C:\\Nativebits\\WebScrap\\chromedriver.exe")
driver.maximize_window()
res =driver.get("https://www.fancode.com/cricket/schedule/today")

#print(driver.page_source)
markup = driver.page_source
sleep(10)
soup = BeautifulSoup(markup,features="html.parser")
soup.prettify()
count = 0
divs = []
for elem in soup.find_all("a"):
    if "data-analytics" in  elem.attrs:
        res = json.loads(elem.attrs['data-analytics'])
        if "name" in res and res['name'] == "MatchCardClicked":
            if res["params"]["matchStatus"] == "LIVE":  
                print(elem.attrs['data-analytics'])
                count = count+1
                print(count)
                div = {
                    "name" : res["params"]["matchName"],
                    "link" : "https://www.fancode.com" + elem.attrs["href"]
                }
                divs.append(div)
TeamA = []
TeamB = []
def checkName(txt):
    #txt = ""
    if txt.endswith("WK"):
        return txt[:-2]
    elif txt.endswith("BAT"):
        return txt[:-3]
    elif txt.endswith("BOWL"):
        return txt[:-4]
    elif txt.endswith("AR"):
        return txt[:-2]
    return ""

def checkRole(txt):
    #txt = ""
    if txt.endswith("WK"):
        return "WK"
    elif txt.endswith("BAT"):
        return "BAT"
    elif txt.endswith("BOWL"):
        return "BOWL"
    elif txt.endswith("AR"):
        return "AR"
    return ""
for div in divs:
    if "ENG" in div['name']:
        driver.get(div['link'].replace("live-match-info","squad"))
        markup2 = driver.page_source
        sleep(10)
        soup2 = BeautifulSoup(markup2,features="html.parser")
        soup2.prettify()
        for elem in soup2.find_all("div"):
            if "data-e2e" in elem.attrs and elem.attrs["data-e2e"] == "squad_players":
                for child in elem.children:
                    aTags =  child.find_all("a")
                     
                    if len(aTags) == 2:
                        TeamA.append({
                            "name" : checkName(aTags[0].text),
                            "role" : checkRole(aTags[0].text)
                        })
                        TeamB.append({
                            "name" : checkName(aTags[1].text),
                            "role" : checkRole(aTags[1].text)
                        })

                    if len(aTags) == 1 and child.next_element.name == "a":
                       TeamA.append({
                            "name" : checkName(aTags[0].text),
                            "role" : checkRole(aTags[0].text)
                        })
                    elif len(aTags) == 1:
                        TeamB.append({
                            "name" : checkName(aTags[0].text),
                            "role" : checkRole(aTags[0].text)
                        })

                    print(child)
    
#print(soup.prettify())
s = soup.find("a")["data-analytics"]
print(s.count())