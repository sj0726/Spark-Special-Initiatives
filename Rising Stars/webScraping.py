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
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupA-C.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupD-F.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupG-H.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupI-K.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupL-Q.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupR-V.shtml",
        "https://www2.eecs.berkeley.edu/risingstars/2020/participants/groupW-Z.shtml"
    ]

    response = requests.get(urls[0], timeout=10)
    html_content = response.text
    wanted_list = ['Sarah Aguasvivas Manzano', 'amanzano.shtml'] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    participants = []
    for u in urls:
        result = scraper.get_result_similar(url=u, grouped=True)#, group_by_alias=True)
        names = list(result.values())[0]
        address = list(result.values())[1]
        basic = list(zip(names, address))
        participants += basic
    pprint.pprint(participants)
    # $$ #
    
    getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    link = "https://www2.eecs.berkeley.edu/risingstars/2020/participants/"
    temp = [ # training models
        # (bioLink[0], ["maa343@cornell.edu"]), # default case
        (link + participants[0][1], ["University of Colorado Boulder", "Control and Learning on Edge Devices for Peripheral Robot Intelligence", "https://sarahaguasvivas.github.io/"]), # case when email is too long so it goes over a single line
        (link + participants[1][1], ["Northwestern University", "Re-imagining Wearable Visual Observation", "https://www.rawanalharbi.com/"])
    ]
    # $$ #
    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        res = scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the rules specified from the training model

    data = {}
    for i in range(len(participants)):
        # parsing basic info
        # $$ #
        # info = re.split(", |: ", names[i], 2)
        # name = info[0]
        # institution = info[1]
        # desc = info[2][1:-1]
        # $$ #

        # getting detailed info from personal page
        response = requests.get(link + participants[i][1], timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        print(result)
        if len(result) < 3:
            result.append("N/A")
        data[participants[i][0]] = {'institution:': result[0], 'description': result[1], 'contact': result[2]}
    #     # $$ #
    #     if "Email: " in result[0]:
    #         result[0] = result[0].split()[1]
    #     print(result)
    #     data[name] = {'institution': institution, 'description': desc, 'contact': result[0]}
    #     # $$ #

    final = json.dumps(data, indent=4)
    with open("data/Berkeley2020.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()