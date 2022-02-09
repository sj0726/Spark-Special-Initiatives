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
        "https://publish.illinois.edu/rising-stars/participants/"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['https://publish.illinois.edu/rising-stars/ayten-ozge-akmandor/', 'https://publish.illinois.edu/rising-stars/andrea-alexandru/', 'https://publish.illinois.edu/rising-stars/naama-ben-david/'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    # $$ #
    for u in urls:
        result = scraper.get_result_similar(url=u, grouped=True)
        # print(result)
        x = list(result.values())
        for i in x:
            participants += i
        # pprint.pprint(participants)
        getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    # temp = [ # training models
    #     (participants[0], ["Ayten Ozge Akmandor", "Princeton University", "PhD Candidate", "Research Abstract:  Semantically Enhanced Classification of Real-world Tasks"]),
    #     # (participants[3], ["University of Pennsylvania", "PhD Candidate"]),
    #     # (participants[5], ["University of Maryland at College Park", "PhD Candidate"]),
    #     # (participants[7], ["Georgia Institute of Technology", "PhD Candidate"]),
    #     # (participants[9], ["Carnegie Mellon University", "PhD Candidate"]),
    # ]
    # $$ #

    # scraper = AutoScraper()
    # for url, wanted_list in temp:
    #     response = requests.get(url, timeout=100)
    #     html_content = response.text
    #     scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(len(participants)):
        # getting detailed info from personal page per participants
        # $$ #
        ban = [
            "https://publish.illinois.edu/rising-stars/heba-aly/",
            "https://publish.illinois.edu/rising-stars/hana-habib",
            "https://publish.illinois.edu/rising-stars/huda-ibeid",
            "https://publish.illinois.edu/rising-stars/guyue-liu"
            ]
        if participants[i] in ban:
            continue
        print(participants[i])
        response = requests.get(participants[i], timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find(class_="wp-block-media-text__content")
        name = body.find("h2")
        if name == None:
            continue
        else:
            name = name.text
        institution = body.find("h3")
        if institution == None:
            institution = "N/A"
        else:
            institution = institution.text
        bold = body.find_all("strong")
        position = bold[0].text
        desc = bold[1].text
        if ":" in desc:
            desc = desc.split(":", maxsplit=1)
            if len(desc) < 2:
                desc = "N/A"
            else:
                desc = desc[1].lstrip()
        else:
            desc = desc.split("Abstract", maxsplit=1)
            if len(desc) < 2:
                desc = "N/A"
            else:
                desc = desc[1].lstrip()
        personalPage = body.find("h2").find("a")
        if personalPage == None:
            personalPage = "N/A"
        else:
            personalPage = personalPage['href']

        # with open("test.html", "w") as f:
        #     f.write(str(body))
        #     f.write("\n")
        #     f.write(str(personalPage))
        #     f.close()
        # break

        data[name] = {
            'institution': institution,
            'position': position,
            'description': desc,
            'contact': "N/A",
            'personal page': personalPage
        }
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()