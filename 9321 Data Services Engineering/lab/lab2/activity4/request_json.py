import requests

url = 'https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json'

'''
params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)
'''
r = requests.get(url)
data = r.json()
#print(data)