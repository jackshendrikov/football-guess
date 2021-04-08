from bs4 import BeautifulSoup

url = 'example.html'

players = open('players.txt', 'a')

soup = BeautifulSoup(open(url), 'html.parser')
table_wiki = soup.find('table', {'id': 'playerTopList'})

for td in table_wiki.find_all('td', {'class': 'name'}):
    players.write("_".join(td.text.replace('\n', '').split(' ')) + '\n')

players.close()
