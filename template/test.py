import pandas as pd
import csv
import json
import requests

# url = 'https://httpbin.org/cookies'

# requestsJar = requests.cookies.RequestsCookieJar()
# requestsJar.set('username', 'Anna', domain='httpbin.org', path='/cookies')
# requestsJar.set('username', 'Bella', domain='httpbin.org', path='/Bella')
# r3 = requests.get(url, cookies=requestsJar)
# print(r3.text)

# with open('chat_records.json', 'r') as f:
#         data = json.load(f)
#         print(data['chat_records'][0]['user'])

with open('pwd.txt', 'r') as f:
    data = f.read()
    print(data)
