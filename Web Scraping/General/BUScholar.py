import json
from pprint import pprint

f = open("googleScholar.json", "r")
data = json.load(f)
keywords = ['comput', 'data', 'machine learning', 'aritificial intelligence', 'computer vision',
            'human computer interaction', 'natural language process', 'robotics', 'neural networks']
exactMatch = ['ai']
keywords = [x.casefold() for x in keywords]
result = {"profiles": []}

for profile in data["profiles"]:
    if 'email' in profile and 'interests' in profile:
        if profile['email'] == 'Verified email at bu.edu':
            interestMatch = False
            for interest in profile['interests']:
                for keyword in keywords:
                    if keyword in interest['title'].casefold():
                        print(profile['name'])
                        result["profiles"].append(profile)
                        interestMatch = True
                        # print(interest['title'], "matched with", keyword)
                        break
                if interestMatch:
                    break

                for exact in exactMatch:
                    temp = interest['title'].casefold().split()
                    if exact in temp:
                        print(profile['name'])
                        result["profiles"].append(profile)
                        interestMatch = True
                        # print(interest['title'], "matched with", exact)
                        break
                if interestMatch:
                    break

pprint(result)

with open("BUScholar.json", "w") as f:
    f.write(str(json.dumps(result)))