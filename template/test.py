import pandas as pd
import csv
import json
  

# with open('credentials.csv', 'a') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Iris', '888'])

with open('info.json') as f:
    data = json.load(f)
    for i in data['user_info']:
        print(i['friends'])
