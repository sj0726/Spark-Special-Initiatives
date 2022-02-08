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
    wanted_list = ['Yomna Abdelrahman', 'https://risingstars18-eecs.mit.edu/participant-abdelrahman/'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    # $$ #
    for u in urls:
        result = scraper.get_result_similar(url=u, group_by_alias=True)
        print(result)
        # pprint.pprint(participants)
        # getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    temp = [ # training models
        (participants[1], ["Princeton University", "PhD Candidate"]),
        (participants[3], ["University of Pennsylvania", "PhD Candidate"]),
        (participants[5], ["University of Maryland at College Park", "PhD Candidate"]),
        (participants[7], ["Georgia Institute of Technology", "PhD Candidate"]),
        (participants[9], ["Carnegie Mellon University", "PhD Candidate"]),
    ]
    # $$ #

    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(0, len(participants), 2):
        # getting detailed info from personal page per participants
        # $$ #
        print(participants[i+1])
        response = requests.get(participants[i+1], timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        print(result)
        if len(result) < 1:
            result.append("N/A")
            result.append("N/A")
        elif len(result) == 1:
            result.append("N/A")
        data[participants[i]] = {'institution:': result[0], 'position': result[1], 'description': 'N/A', 'contact': 'N/A', 'personal page': participants[i+1]}
        # $$ #

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()