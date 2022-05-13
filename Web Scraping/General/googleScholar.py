from time import sleep
import requests
import json
import pprint

type = "json"
engine = "google_scholar_profiles"
mauthors = "Boston Universtiy"
hl = "en"
api_key = "" # replace with proper key
init = "https://serpapi.com/search.{}?engine={}&mauthors={}&hl={}&api_key={}".format(type, engine, mauthors, hl, api_key)

response = requests.get(init)
initData = response.json()

profiles = initData["profiles"]
# print(isinstance(profiles, list))
after_author = initData["pagination"]["next_page_token"]
result = {"profiles" : []}
result["profiles"] += profiles
count = 1

while after_author != None:
    url = "https://serpapi.com/search.{}?after_author={}&engine={}&mauthors={}&hl={}&api_key={}".format(type, after_author, engine, mauthors, hl, api_key)
    response = requests.get(url)
    print(response.status_code)
    if (response.status_code != 200):
        print(response.text)
        break
    data = response.json()
    count += 1
    print("details: {0}\nlink: {1}\ncount:{2}\n".format(data["search_parameters"], data["search_metadata"]["google_scholar_profiles_url"], count))

    profiles = data["profiles"]
    if "pagination" in data:
        if "next_page_token" in data["pagination"]:
            after_author = data["pagination"]["next_page_token"]
        else:
            print("last page!")
            break
    else:
        print("no pagination!")
        break

    result["profiles"] += profiles
    sleep(2)
    # break
# pprint.pprint(result)
print("Requests made:", count)

with open("googleScholar.json", "w") as f:
    f.write(str(json.dumps(result)))