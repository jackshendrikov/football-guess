""" This module defines all of work with scores of commands of specific league for the last week """

import requests

from bs4 import BeautifulSoup
from leagues.utils import shorten_name


def scrape_page(url):
    """ Scrape certain web-page, find and retrieve the necessary tags """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")

    games = soup.findAll("div", {"class": "row-gray"})

    return games


class ChampionshipLatest:
    """ Class representing current scores of commands of specific for the last week.
            url (String) - url for parse scores.
    """

    def __init__(self, url, width):
        """ Initialize type """
        self.url = url
        self.width = width

    def parse_latest(self):
        """ Parse necessary data, format it and return to the user """
        games = scrape_page(self.url)
        scores = [shorten_name(game.text) for game in games]

        if len(scores) == 0:
            return "I cann't find any score at {0}".format(self.url)
        else:
            return '*' * (self.width + 4) + "{0}".format("\n".join(scores)) + '*' * (self.width + 4)
