""" This module defines all of work with scores of commands of specific league for the last week """
import re

import requests

from bs4 import BeautifulSoup
from texttable import Texttable
from leagues.utils import shorten_name


def scrape_page(url):
    """ Scrape certain web-page, find and retrieve the necessary tags """
    print("Trying to retrieve web page...")

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    games = soup.findAll("div", {"class": "row-gray"})

    scores = []

    for element in games:
        match_name_element = element.find(attrs={"class": "scorelink"})

        if match_name_element is not None:
            home_team = shorten_name(' '.join(element.find("div", "tright").get_text().strip().split(" ")))
            away_team = shorten_name(' '.join(element.find(attrs={"class": "ply name"}).get_text().strip().split(" ")))

            home_scores = element.find("div", "sco").get_text().split("-")[0].strip()
            away_scores = element.find("div", "sco").get_text().split("-")[1].strip()

            scores.append([home_team, home_scores + "-" + away_scores, away_team])

    print("Retrieve successful!")

    return scores


class ChampionshipLatest:
    """ Class representing current scores of commands of specific for the last week.
            url (String) - url for parse scores.
    """

    def __init__(self, url):
        """ Initialize type """
        self.url = url

    def parse_latest(self):
        """ Parse necessary data, format it and return to the user """
        # final version of the table to send to the user
        scores = Texttable()

        # settings for table
        scores.set_cols_width([9, 3, 9])
        scores.set_cols_align(['l', 'c', 'r'])  # c - center align (horizontal), l - left, r - right
        scores.set_cols_valign(['m', 'm', 'm'])  # m - middle align (vertical)
        scores.set_chars(['—', '|', '+', '='])  # replace dash with em dash

        scores.add_rows([["Home Team", "", "Away Team"]] + scrape_page(self.url))

        return '`' + scores.draw() + '`'
