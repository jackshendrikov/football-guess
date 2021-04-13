from bs4 import BeautifulSoup
from urllib.request import urlopen


def parse_url(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    team = soup.findAll("div", {"class": "team"})
    pts = soup.findAll("div", {"class": "pts"})

    return team, pts


class ChampionshipTable:

    def __init__(self, url, table_width, table_height):
        self.url = url
        self.table_width = table_width
        self.table_height = table_height

    def create_table(self):
        # create matrix from zeros
        teamInfo = [[0 for x in range(self.table_width)] for y in range(self.table_height)]

        # final version of the table to send to the user
        res_table = []

        # get team names and corresponding points
        team, pts = parse_url(self.url)

        if not team or not pts:
            res_table.append("%-*s %s" % (5, "Empty Table", "Empty Table"))
        else:
            z = 0
            for x in range(0, self.table_height):
                teamInfo[x][0] = team[x].text
                for y in range(1, self.table_width):
                    teamInfo[x][y] = pts[z].text
                    z += 1

        for x in range(0, self.table_height):
            res_table.append("%-*s %s" % (5, teamInfo[x][8], teamInfo[x][0]))

        return '\n'.join(res_table)
