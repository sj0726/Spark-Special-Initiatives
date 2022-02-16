from selectors import PollSelector
from attr import attrs
from autoscraper import AutoScraper
from bs4 import BeautifulSoup
from matplotlib.pyplot import text
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
        "https://risingstars15-eecs.mit.edu/participants/"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['https://risingstars15-eecs.mit.edu/henny-admoni/'] # initial scraping models to get participants' names & personal pages
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
        ("https://risingstars15-eecs.mit.edu/henny-admoni/", ['Position: PhD Candidate'])
    ]
    # # $$ #

    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(len(participants)):
        url = participants[i]
        if url == "https://risingstars15-eecs.mit.edu/deblina-sarkar/":
            continue
        print(url)
        response = requests.get(url, timeout=10)
        # html_content = response.text
        # result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact content is different, the scraper object will know that the object in the same position is the one to fetch
        # print(result)
        # if len(result) > 0:
        #     if "Position:" in result[0]:
        #         position = result[0].split("Position:")[1].lstrip()
        #     else:
        #         position = "N/A"
        # else:
        #     position = "N/A"


        soup = BeautifulSoup(response.content, 'html.parser')
        # # getting detailed info from personal page per participants
        # # $$ #

        title = soup.find("h2").getText()
        name = title.split(", ")[0]
        [institution, desc] = title.split(", ")[1].split(". ")
        basicInfo = soup.find(class_="fusion-column-wrapper").find_all("p")[1:]
        email = basicInfo[0].find("a")['href']
        pos = soup.find_all(class_="fusion-column-wrapper")[1]
        position = pos.find("p")
        if position.b != None:
            position.b.decompose()
        if position.u != None:
            position.u.decompose()
        position = position.text
                            # position = pos # point to the same reference
                            # pos.b.decompose()
                            # position = position.text
                            # detail = basicInfo.find(class_="fusion-column-wrapper").find_all("b")
                            # email = detail[0].find("a")["href"]
        if len(basicInfo) > 1:
            website = basicInfo[1].find("a")
            if website != None:
                personalPage = website["href"]
            else:
                personalPage = url
        else:
            personalPage = url
        print(name, institution, position, desc, email, personalPage)
        # with open("test.html", "w") as f:
        #     f.write(str(position))
        #     f.close()
        # break
        # response = requests.get(participants[i], timeout=10)
        # html_content = response.text
        # result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        # print(result)
        data[name] = {
            'institution': institution,
            'position': position,
            'description': desc,
            'contact': email,
            'personal page': personalPage
        }
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()