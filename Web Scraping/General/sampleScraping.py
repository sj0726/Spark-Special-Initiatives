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
    # urls =  [ # link to participants lists
    #     "https://ww3.aauw.org/aauw_check/fellowships_directory/#fldComputer%20and%20information%20sciences&"
    # ]

    # response = requests.get(urls[0], timeout=10)
    # html_content = response.text
    # wanted_list = ['Kirsten Boehner', 'Cornell University', "#rid2013"] # initial scraping models to get participants' names & personal pages
    # $$ #

    # init. autoscraper
    # scraper = AutoScraper()
    # scraper.build(html=html_content, wanted_list=wanted_list)
    # $$ #
    data = {'data': []}
    for x in range(1, 18):
        print("page", x)
        url = "https://www.pdsoros.org/meet-the-fellows?Fellowship%20Year%5B0%5D=2021&Fellowship%20Year%5B1%5D=2020&Fellowship%20Year%5B2%5D=2019&Fellowship%20Year%5B3%5D=2018&Fellowship%20Year%5B4%5D=2017&Fellowship%20Year%5B5%5D=2016&Fellowship%20Year%5B6%5D=2015&Fellowship%20Year%5B7%5D=2014&Fellowship%20Year%5B8%5D=2013&Fellowship%20Year%5B9%5D=2012&Fellowship%20Year%5B10%5D=2011&Fellowship%20Year%5B11%5D=2010&Fellowship%20Year%5B12%5D=2009&Fellowship%20Year%5B13%5D=2008&Fellowship%20Year%5B14%5D=2007&Fellowship%20Year%5B15%5D=2006&Fellowship%20Year%5B16%5D=2005&Fellowship%20Year%5B17%5D=2004&Fellowship%20Year%5B18%5D=2003&Fellowship%20Year%5B19%5D=2002&Fellowship%20Year%5B20%5D=2001&Fellowship%20Year%5B21%5D=2000&Fellowship%20Year%5B22%5D=1999&Fellowship%20Year%5B23%5D=1998&Professional%20Fields%5B0%5D=science%2C%20engineering%2C%20and%20technology&page={}&append=1".format(x)
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all("div", class_="pd-person pd-row pd-person--full")
        for entry in table:
            content = entry.find("div", class_="pd-person-content")
            field = content.find("p", class_="pd-person-rationale").text
            # print(field)
            if re.search("comput", field, re.IGNORECASE):
                name = content.find("h4").text.split(",")[0]
                info = content.find_all("p")
                position = info[0].text.split(",")[0].strip()
                institution = info[0].text.split(",")[1].strip()
                personalPage = content.find("a")['href']
            else:
                continue
            print(name, position, institution, personalPage)
            temp = {
            'name': name,
            'institution': institution,
            'position': position,
            'description': "N/A",
            'contact': "N/A",
            'personal page': personalPage
            }
            data['data'].append(temp)
    
    final = json.dumps(data, indent=4)
    with open("PhD.json", "w") as f: 
        f.write(final)
        # pprint.pprint(result)
        # break
        # names = list(result.values())[0]
        # address = list(result.values())[1]
        # basic = list(zip(names, address))
        # participants += basic
    # pprint.pprint(participants)
    # getDetails(participants) # get detailed information from personal pages (if applicable)
    # $$ #

def getDetails(participants):
    # scraper initialization / training
    # $$
    link = "https://www2.eecs.berkeley.edu/risingstars/2020/participants/"
    temp = [ # training models
        (link + participants[0][1], ["University of Colorado Boulder", "Control and Learning on Edge Devices for Peripheral Robot Intelligence", "https://sarahaguasvivas.github.io/"]), # case when email is too long so it goes over a single line
        (link + participants[1][1], ["Northwestern University", "Re-imagining Wearable Visual Observation", "https://www.rawanalharbi.com/"])
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
        response = requests.get(link + participants[i][1], timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact content is different, the scraper object will know that the object in the same position is the one to fetch
        print(result)
        if len(result) < 3:
            result.append("N/A") # in case there is no information listed (happens for some participants)
        data[participants[i][0]] = {'institution:': result[0], 'description': result[1], 'contact': result[2]}
        # $$ #

    final = json.dumps(data, indent=4)
    with open("data/Berkeley2020.json", "w") as f: 
        f.write(final)

if __name__ == "__main__":
    data = getNames()