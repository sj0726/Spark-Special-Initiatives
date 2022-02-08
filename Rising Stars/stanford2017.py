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
        "https://risingstars2017.stanford.edu/speaker-category/participants/"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['Yousra Aafer', 'https://risingstars2017.stanford.edu/organizing-committee/yousra-aafer/'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    # $$ #
    for u in urls:
        result = scraper.get_result_similar(url=u, grouped=True)
        names = list(result.values())[0]
        address = list(result.values())[2]
        basic = list(zip(names, address))
        participants += basic
        # pprint.pprint(participants)
        getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    temp = [ # training models
        # ("https://risingstars2017.stanford.edu/organizing-committee/yousra-aafer/", ["Yousra Aafer", "Postdoctoral Researcher", "Purdue University"]),
        ("https://risingstars2017.stanford.edu/organizing-committee/bilge-acun/", ["Bilge Acun", "PhD Candidate", "acun2@illinois.edu", "Mitigating Variability in HPC Systems and Applications for Performance and Power Efficiency"])
        # ("https://risingstars2017.stanford.edu/organizing-committee/shaizeen-aga/", ["Shaizeen Aga", "PhD Candidate, University of Michigan, Ann Arbor", "Compute Caches", "shaizeen@umich.edu"])
    ]
    # $$ #

    # scraper = AutoScraper()
    # for url, wanted_list in temp:
    #     response = requests.get(url, timeout=100)
    #     html_content = response.text
    #     scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(1, len(participants)):
        # getting detailed info from personal page per participants
        # $$ #

        url = participants[i][1]
        print(url)
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        result = soup.find(class_="columns small-12 medium-9 large-9").find_all("p")
        name = soup.find(class_="columns small-12 medium-3 large-3").find(class_="name").getText()
        basicInfo = result[0].getText()
        institution = re.split(",|\n", basicInfo)[1].lstrip()
        position = re.split(",|\n", basicInfo)[0]
        email = result[0].find("a")["href"]
        abstract = result[1].getText().split("\n")[1]

        # name = participants[i][0].split(",")[0]
        # response = requests.get(participants[i][1], timeout=10)
        # html_content = response.text
        # result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        # print(result)
        data[name] = {
            'institution:': institution,
            'position': position,
            'description': abstract,
            'contact': email,
            'personal page': url
        }
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()