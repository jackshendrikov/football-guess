""" This module defines all of work with current scores of commands of specific league """

import requests

from bs4 import BeautifulSoup
from texttable import Texttable
from leagues.utils import shorten_name


class ChampionshipScores:
    """ Class representing current scores of commands of specific League.
           url (String) - url for parse scores.
    """

    def __init__(self, url):
        """ Initialize type """
        self.url = url

    def scrape_score(self):
        """ Scrape web page, retrieve necessary data, format it and return to the user """
        page = requests.get(self.url)
        parsed_markup = BeautifulSoup(page.text, "html.parser")

        # final version of the table to send to the user
        scores = Texttable()

        # settings for table
        scores.set_cols_width([10, 1, 10])
        scores.set_cols_align(['l', 'c', 'r'])  # c - center align (horizontal), l - left, r - right
        scores.set_cols_valign(['m', 'm', 'm'])  # m - middle align (vertical)
        scores.set_chars(['—', '|', '+', '='])  # replace dash with em dash
        scores.header(["Home Team", "", "Away Team"])

        # scrape needed data from the parsed markup
        for element in parsed_markup.find_all("div", "row-gray"):

            match_name_element = element.find(attrs={"class": "scorelink"})

            if match_name_element is not None and element.find("div", "sco").get_text().split("-")[0].strip() == "?":
                home_team = shorten_name(' '.join(element.find("div", "tright").get_text().strip().split(" ")))
                away_team = shorten_name(' '.join(element.find(attrs={"class": "ply name"}).get_text().strip().split(" ")))

                scores.add_row([home_team, "-", away_team])

        return '`' + scores.draw() + '`'
