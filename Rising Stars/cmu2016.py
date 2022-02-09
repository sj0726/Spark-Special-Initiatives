from selectors import PollSelector
from attr import attrs
from autoscraper import AutoScraper
from bs4 import BeautifulSoup
import requests
import re
import json
import pprint
##############################################################################################################
########      Disclaimer: codes in-between comments with "$$" sign should be changed per website      ########
##############################################################################################################

def getNames():
    # initial setups
    # $$ #
    urls =  [ # link to participants lists
        "http://risingstars.ece.cmu.edu/participants/"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['http://risingstars.ece.cmu.edu/mehrnaz-afshang/'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    # $$ #
    for u in urls:
        result = scraper.get_result_similar(url=u, grouped=True)
        # pprint.pprint(result)
        # names = list(result.values())[0]
        # address = list(result.values())[2]
        # basic = list(zip(names, address))
        participants += list(result.values())[0]
        # pprint.pprint(participants)
        getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    temp = [ # training models
        ("http://risingstars.ece.cmu.edu/mehrnaz-afshang/", ["Position: Postdoctoral Fellow"])
    ]
    # $$ #

    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(len(participants)):
        url = participants[i]
        print(url)
        response = requests.get(url, timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact content is different, the scraper object will know that the object in the same position is the one to fetch
        if len(result) > 0:
            if "Position:" in result[0]:
                position = result[0].split("Position:")[1].lstrip()
        else:
            position = "N/A"


        soup = BeautifulSoup(response.content, 'html.parser')
        # getting detailed info from personal page per participants
        # $$ #

        title = soup.find("h2").getText().split(",")
        name = title[0]
        institution = title[0].lstrip()
        basicInfo = soup.find(class_="post-content")
        # pos = basicInfo.find(text=re.compile("^.*Position:.*$")).parent.parent
        # position = pos # point to the same reference
        # pos.b.decompose()
        # position = position.text
        detail = basicInfo.find(class_="fusion-column-wrapper").find_all("b")
        email = detail[0].find("a")["href"]
        if len(detail) > 1:
            website = detail[1].find("a")
            if website != None:
                personalPage = website["href"]
            else:
                personalPage = url
        else:
            personalPage = url
        print(name, institution, position, email, personalPage)
        # with open("test.html", "w") as f:
        #     f.write(str(basicInfo))
        #     f.write(str(position))
        #     f.close()
        # break
        # response = requests.get(participants[i], timeout=10)
        # html_content = response.text
        # result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        # print(result)
        data[name] = {
            'institution:': institution,
            'position': position,
            'description': "N/A",
            'contact': email,
            'personal page': personalPage
        }
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()