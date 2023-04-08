import pandas as pd
import csv
import json
import requests

url = 'https://httpbin.org/cookies'

requestsJar = requests.cookies.RequestsCookieJar()
requestsJar.set('username', 'Anna', domain='httpbin.org', path='/cookies')
requestsJar.set('username', 'Bella', domain='httpbin.org', path='/Bella')
r3 = requests.get(url, cookies=requestsJar)
print(r3.text)

