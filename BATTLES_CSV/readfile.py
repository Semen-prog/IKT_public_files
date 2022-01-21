import json

d = json.load(open("translation.json"))

for tab in d["resources"]:
    s = tab["path"].split('/')[-1][:-4]
    print('!!!', s, '!!!', '<br>', '<br>')
    for field in tab["schema"]["fields"]:
        print(field["id"], ": ", sep = '', end = '')
        if "description" in field:
            print(field["description"], end = '')
        print('<br>')
    print('<br>')
    print('<br>')
