import pandas as pd
import csv
import json
import model

# url = 'https://httpbin.org/cookies'

# requestsJar = requests.cookies.RequestsCookieJar()
# requestsJar.set('username', 'Anna', domain='httpbin.org', path='/cookies')
# requestsJar.set('username', 'Bella', domain='httpbin.org', path='/Bella')
# r3 = requests.get(url, cookies=requestsJar)
# print(r3.text)

# with open('chat_records.json', 'r') as f:
#         data = json.load(f)
#         print(data['chat_records'][0]['user'])

salt = model.salt_generator()
pwd_info = model.hash_calculator('test1', salt)
print(pwd_info)

pwd_info = model.hash_calculator('test1', salt)
print(pwd_info)
