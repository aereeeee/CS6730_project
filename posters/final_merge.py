import json

u = {}
uu = {}

with open('1_125_f.json', 'r') as fp:
    u = json.load(fp)

with open('movies_data_f.json', 'r') as fp:
    uu = json.load(fp)

f = []
for obj in uu:
    if obj['id'] not in u.keys():
        continue
    perc = u[obj['id']]
    f.append({**obj, **perc})

with open('movies_data_f.json', 'w+') as fp:
    fp.write(json.dumps(f, indent = 2))