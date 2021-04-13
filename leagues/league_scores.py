""" This module defines all of work with current scores of commands of specific league """

from bs4 import BeautifulSoup
from urllib.request import urlopen


class ChampionshipScores:
    """ Class representing current scores of commands of specific League.
           url (String) - url for parse scores.
    """

    def __init__(self, url):
        """ Initialize type """
        self.url = url

    def scrape_score(self):
        """ Scrape web page, retrieve necessary data, format it and return to the user """
        page = urlopen(self.url)
        parsed_markup = BeautifulSoup(page, "html.parser")

        # dictionary to contain scores
        scores = []

        # scrape needed data from the parsed markup
        for element in parsed_markup.find_all("div", "row-gray"):

            match_name_element = element.find(attrs={"class": "scorelink"})

            if match_name_element is not None:
                # this means the match is about to be played

                home_team = '-'.join(element.find("div", "tright").get_text().strip().split(" "))
                away_team = '-'.join(element.find(attrs={"class": "ply name"}).get_text().strip().split(" "))

                match_name = match_name_element.get('href').split('/')[4]
                home_team_score = element.find("div", "sco").get_text().split("-")[0].strip()
                away_team_score = element.find("div", "sco").get_text().split("-")[1].strip()

                print(match_name)

                scores.append("{} %s vs {} %s".format(home_team, away_team) % (home_team_score, away_team_score))

        return '\n'.join(scores)
