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

    def create_table(self):
        """ Parse table, format it and return to the user """
        # create matrix from zeros
        teamInfo = [[0 for x in range(self.table_width)] for y in range(self.table_height)]

        # final version of the table to send to the user
        res_table = Texttable()

        # settings for table
        res_table.set_cols_width([2, 15, 4])
        res_table.set_cols_align(['c', 'l', 'c'])   # c - center align (horizontal)
        res_table.set_cols_valign(['m', 'm', 'm'])  # m - middle align (vertical)

        # get team names and corresponding points
        team, pts = scrape_page(self.url)

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
            if x == 0:  res_table.header(['#', date.today(), "Pts"])
            else: res_table.add_row([x, teamInfo[x][0], teamInfo[x][8]])

        return '`' + res_table.draw().replace('-', '—') + '`'
