import json

f = open('data/MIT2021.json')
data = json.load(f)

# print(json.dumps(data, sort_keys=True))
new = {'data': []}
for x in data:
    print(data[x])
    temp = {
            'name': x,
            'institution:': data[x]['institution'],
            'position': data[x]['position'],
            'description': data[x]['description'],
            'contact': data[x]['contact'],
            'personal page': data[x]['personal page']
    }
    new['data'].append(temp)

final = json.dumps(new, indent=4)
with open("test.json", "w") as f: 
    f.write(final)
    f.close()