import requests
from bs4 import BeautifulSoup




word = input()
url="https://en.wikipedia.org/wiki/{}".format(word)
subject_page = requests.get(url)
soup = BeautifulSoup(subject_page.text,'lxml')
result = soup.select('.mw-parser-output p')
print(result[1].text)


