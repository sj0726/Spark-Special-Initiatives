from autoscraper import AutoScraper
import requests
import re
import json

def getNames():
    # initial setups
    url = "https://risingstars21-eecs.mit.edu/participants/" # link to participants lists
    response = requests.get(url, timeout=10)
    html_content = response.text
    wanted_list = ['Maria Antoniak, Cornell University: “Modeling Personal Experiences Shared in Online Communities”', 'https://risingstars21-eecs.mit.edu/antoniak/'] # initial scraping models to get participants' names & personal pages
    
    # init. autoscraper
    scraper = AutoScraper()
    scraper.build(html=html_content, wanted_list=wanted_list)
    result = scraper.get_result_similar(html=html_content, grouped=True)#, group_by_alias=True)
    names = list(result.values())[0] # list of names
    bioLink = list(result.values())[1] # list of personal pages
    getDetails(names, bioLink) # get detailed information from personal pages (if applicable)

def getDetails(names, bioLink):
    # scraper initialization / training
    temp = [ # training models
        # (bioLink[0], ["maa343@cornell.edu"]), # default case
        ("https://risingstars21-eecs.mit.edu/ippolito/", ["daphnei@seas.upenn.edu", "Position: PhD Candidate"]) # case when email is too long so it goes over a single line
    ]
    scraper = AutoScraper()
    for url, wanted_list in temp:
        response = requests.get(url, timeout=100)
        html_content = response.text
        scraper.build(html=html_content, wanted_list=wanted_list, update=True) # this creates a scraper object with the same rule of getting the inital "maa343@cornell.edu" email
    
    data = {}
    for i in range(len(names)):
        # parsing names
        info = re.split(", |: ", names[i], 2)
        name = info[0]
        institution = info[1]
        desc = info[2][1:-1]

        # getting detailed info from personal page
        url = bioLink[i]
        response = requests.get(url, timeout=10)
        html_content = response.text
        result = scraper.get_result_similar(html=html_content) # by using get_result_similar, even though the exact email address is different, the scraper object will know that the object in the same position is the one to fetch
        if "Email: " in result[0]:
            result[0] = result[0].split()[1]
        if "Position: " in result[1]:
            result[1] = result[1].split(maxsplit=1)[1]
        print(result)
        data[name] = {'institution': institution, 'description': desc, 'position': result[1], 'contact': result[0], 'personal page': bioLink[i]}
        # print("\nname:", name, "\ninstitution:", institution, "\ndesc:", desc, "\nemail:", result[0])

    final = json.dumps(data, indent=4)
    with open("test.json", "w") as f:
        f.write(final)

if __name__ == "__main__":
    data = getNames()