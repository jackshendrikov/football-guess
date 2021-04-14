""" This module defines all of work with current tables of specific league """

import requests

from bs4 import BeautifulSoup
from leagues.utils import shorten_name
from texttable import Texttable
from datetime import date


def scrape_page(url):
    """ Scrape certain web-page, find and retrieve the necessary tags """
    print("Trying to retrieve web page...")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    team = soup.findAll("div", {"class": "team"})
    pts = soup.findAll("div", {"class": "pts"})

    print("Retrieve successful!")

    return team, pts


# Teams Quota. Example: [(2, 1), (1, 1), 3]
#   (2, 1) ->
#       2 - teams in Champions League,
#       1 - teams in Champions League Qualification
#   (1, 1) ->
#       1 - teams in Europa League
#       1 - teams in Europa League Qualification
#   3 -> Relegation
country_quota = dict([("spain", [(4, 0), (1, 1), 3]), ("germany", [(4, 0), (1, 1), 3]),
                      ("italy", [(4, 0), (1, 1), 3]), ("france", [(2, 1), (1, 1), 3]),
                      ("ukraine", [(1, 1), (0, 2), 1]), ("england", [(4, 0), (1, 0), 3])])


class ChampionshipTable:
    """ Class representing current Table of commands of specific League.
           url (String) - url for parse table.
           table_width (Int) - width of the table (include params like points, name of commands, goals, etc.).
           table_height (Int) - height of the table (number of commands on league).
    """

    def __init__(self, url, table_width, table_height):
        """ Initialize type """
        self.url = url
        self.table_width = table_width
        self.table_height = table_height
        self.champions_league = []
        self.europa_league = []
        self.relegation = []

    def team_detail(self, country, teams_num, team, position):
        quotas = country_quota[country]

        team = '_' + team + '_'

        start_cl, start_el = quotas[0][0], quotas[0][0] + quotas[0][1] + quotas[1][0]
        end_cl, end_el = start_cl + quotas[0][1], start_el + quotas[1][1]

        # Champions League
        if position in range(start_cl):
            self.champions_league.append(team)
        elif position in range(start_cl, end_cl):
            self.champions_league.append(team + " (qualification)")

        # Europa League
        elif position in range(start_el):
            self.europa_league.append(team)
        elif position in range(start_el, end_el):
            self.europa_league.append(team + " (qualification)")

        # Relegation
        elif position in range(teams_num - quotas[2], teams_num):
            self.relegation.append(team)

    def create_table(self):
        """ Parse table, format it and return to the user """
        # create matrix from zeros
        teamInfo = [[0 for x in range(self.table_width)] for y in range(self.table_height)]

        # final version of the table to send to the user
        res_table = Texttable()

        # settings for table
        res_table.set_cols_width([2, 15, 4])
        res_table.set_cols_align(['c', 'l', 'c'])  # c - center align (horizontal)
        res_table.set_cols_valign(['m', 'm', 'm'])  # m - middle align (vertical)
        res_table.set_chars(['—', '|', '+', '='])  # replace dash with em dash

        # get team names and corresponding points
        team, pts = scrape_page(self.url)

        # current country
        country = self.url.split('/')[-3]

        if not team or not pts:
            res_table.add_row(["?", "Empty Table", "?"])
        else:
            z = 0
            for x in range(0, self.table_height):
                teamInfo[x][0] = shorten_name(team[x].text)
                for y in range(1, self.table_width):
                    teamInfo[x][y] = pts[z].text
                    z += 1

        for x in range(0, self.table_height):
            if x == 0:
                res_table.header(['#', date.today(), "Pts"])
            else:
                self.team_detail(country, teams_num=self.table_height-1, team=teamInfo[x][0], position=x-1)
                res_table.add_row([x, teamInfo[x][0], teamInfo[x][8]])

        return '`' + res_table.draw() + '`' + \
               "\n\n🏆 *Champions League zone*: " + ", ".join(self.champions_league) + \
               "\n\n🇪🇺 *Europa League zone*: " + ", ".join(self.europa_league) + \
               "\n\n⏬ *Relegation zone*: " + ", ".join(self.relegation)
