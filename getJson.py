import json

import requests

subjectJson = {'subject': []}

url1 = 'https://api.eol.cn/web/api/?keyword=&level1=1&level2=&page='
url2 = '&size=30&sort=&uri=apidata/api/gkv3/special/lists&signsafe=111cd45f1f73e18c6d5cf51e3bcdf3d2'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

d = {'keyword': '',
     'level1': 1,
     'level2': '',
     'page': 26,
     'signsafe': 'f6a12f70ae234d735d2e19e1642c4724',
     'size': 30,
     'sort': '',
     'uri': 'apidata/api/gkv3/special/lists'
     }

for i in range(26):
    url = url1 + str(i + 1) + url2
    result = requests.post(url, data=d, headers=header).json()['data']['item']
    for j in result:
        print(j['name'])
        subject = {
            'name': j['name'],
            'id': j['special_id'],
            'classify': j['level3_name'],
            'degree': j['degree']
        }
        subjectJson['subject'].append(subject)

file = open('init.json', 'w+')
file.write(json.dumps(subjectJson, indent=4, ensure_ascii=False))
file.close()
