from html.entities import html5
from autoscraper import AutoScraper
import requests
import re
import json
import pprint
from bs4 import BeautifulSoup
##############################################################################################################
########      Disclaimer: codes in-between comments with "$$" sign should be changed per website      ########
##############################################################################################################

def getNames():
    # initial setups
    # $$ #
    urls =  [ # link to participants lists
        'https://www.directory.wimlworkshop.org/list/'
    ]

    response = requests.get(urls[0], timeout=10)
    f = open('test.html', 'r')
    table = f.read()
    soup = BeautifulSoup(table, 'html.parser')
    table = soup.find_all(class_="btn pill-btn btn-outline-primary w-75 m-2")
    # print(table)
    # html_content = response.text
    # wanted_list = ['/list/261/'] # initial scraping models to get participants' names & personal pages
    # # $$ #

    # # init. autoscraper
    # scraper = AutoScraper()
    # scraper.build(html=table, wanted_list=wanted_list)
    # $$ #
    participants = []
    for x in table:
    #     result = scraper.get_result_similar(url=u, grouped=True)#, group_by_alias=True)
    #     print(result)
    #     names = list(result.values())[0]
    #     address = list(result.values())[1]
    #     basic = list(zip(names, address))
        participants += ['https://www.directory.wimlworkshop.org' + x['href']]
    # print(participants)
    getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    # link = "https://www2.eecs.berkeley.edu/risingstars/2020/participants/"
    # temp = [ # training models
    #     (participants[0], ["Weiwei Zong"])#, " Research scientist/engineer", " University of Michigan", "mailto:mandyzong@gmail.com", "https://www.linkedin.com/in/weiwei-zongwang-ph-d-b8029940/"]), # case when email is too long so it goes over a single line
    #     # (link + participants[1][1], ["Northwestern University", "Re-imagining Wearable Visual Observation", "https://www.rawanalharbi.com/"])
    # ]
    # $$ #
    
    # scraper = AutoScraper()
    # for url, wanted_list in temp:
    #     response = requests.get(url, timeout=100)
    #     html_content = response.text
    #     scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {'data': []}
    for i in range(len(participants)):
        # getting detailed info from personal page per participants
        # $$ #
        print(participants[i])
        response = requests.get(participants[i], timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("div", id="content")
        name = table.find("h2").text
        basicInfo = table.find_all("p")
        position = basicInfo[0].text.lstrip()
        institution = basicInfo[1].text.lstrip()
        contactInfo = table.find(class_="d-flex flex-column").find_all("a", href=True)
        email = contactInfo[0]["href"]
        personalPage = contactInfo[1]["href"]
        print(name, position, institution, email, personalPage)
        temp = {
            'name': name,
            'institution': institution,
            'position': position,
            'description': "N/A",
            'contact': email,
            'personal page': personalPage
        }
        data['data'].append(temp)
        # for x in basicInfo:
        #     print(x.text.lstrip())
        # for x in contactInfo:
        #     print(x["href"])
        # html_content = response.text
        # result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact content is different, the scraper object will know that the object in the same position is the one to fetch
        # with open("result.html", "w") as f:
        #     f.write(str(basicInfo))
        #     f.close()
        # break
        # if len(result) < 3:
        #     result.append("N/A") # in case there is no information listed (happens for some participants)
        # data[participants[i][0]] = {'institution': result[0], 'description': result[1], 'contact': result[2]}
        # $$ #

    final = json.dumps(data, indent=4)
    with open("WiML.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()