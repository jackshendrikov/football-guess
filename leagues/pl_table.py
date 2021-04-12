from bs4 import BeautifulSoup
from urllib.request import urlopen


url = "http://www.livescores.com/soccer/england/premier-league/"
page = urlopen(url)
soup = BeautifulSoup(page, "lxml")

team = soup.findAll("div", {"class": "team"})
pts = soup.findAll("div", {"class": "pts"})

# Premier League table params
TABLE_WIDTH, TABLE_HEIGHT = 9, 21

# Create matrix from zeros
teamInfo = [[0 for x in range(TABLE_WIDTH)] for y in range(TABLE_HEIGHT)]


def plTable():
    table = []
    if not team or not pts:
        table.append("%-*s %s" % (5, "Empty Table", "Empty Table"))
    else:
        z = 0
        for x in range(0, 21):
            teamInfo[x][0] = team[x].text
            for y in range(1, 9):
                teamInfo[x][y] = pts[z].text
                z += 1

    for x in range(0, 21):
        table.append("%-*s %s" % (5, teamInfo[x][8], teamInfo[x][0]))

    return '\n'.join(table)


PL_TABLE = plTable()
