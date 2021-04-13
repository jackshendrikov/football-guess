""" This module defines all of work with scores of commands of specific league for the last week """

from bs4 import BeautifulSoup
from urllib.request import urlopen


def scrape_page(url):
    """ Scrape certain web-page, find and retrieve the necessary tags """
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")

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
        scores = [game.text for game in games]

        if len(scores) == 0:
            return "I cann't find any score at {0}".format(self.url)
        else:
            return '*' * (self.width + 4) + "{0}".format("\n".join(scores)) + '*' * (self.width + 4)
