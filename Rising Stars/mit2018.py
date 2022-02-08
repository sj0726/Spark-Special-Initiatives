from autoscraper import AutoScraper
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
        "https://risingstars18-eecs.mit.edu/participants/"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['Yomna Abdelrahman, University of Stuttgart. “Thermal Imaging in HCI”', 'https://risingstars18-eecs.mit.edu/participant-abdelrahman/'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    # $$ #
    for u in urls:
        result = scraper.get_result_similar(url=u, grouped=True)
        names = list(result.values())[0]
        address = list(result.values())[1]
        basic = list(zip(names, address))
        participants += basic
        # pprint.pprint(participants)
        getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    temp = [ # training models
        (participants[0][1], ["Current Institution:  University of Stuttgart", "Position:  PhD Candidate", "Abstract:  Thermal Imaging in HCI", "Email:  yomna.abdelrahman@vis.uni-stuttgart.de"])
    ]
    # $$ #

    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(len(participants)):
        # getting detailed info from personal page per participants
        # $$ #
        name = participants[i][0].split(",")[0]
        response = requests.get(participants[i][1], timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        print(result)
        data[name] = {
            'institution:': result[0].split("Current Institution:")[1].lstrip(),
            'position': result[1].split("Position:")[1].lstrip(),
            'description': result[2].split("Abstract:")[1].lstrip(),
            'contact': result[3].split("Email:")[1].lstrip(),
            'personal page': participants[i][1]
        }
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()