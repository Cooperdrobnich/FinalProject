#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER s

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup

"""This file will create a database called 'LebronAndMJStats.db' with all statistics from MJ and Lebron's """

def get_season_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    seasons_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:19]:
            season = row.find_all('th',{'data-stat':'season'})
            for i in season:
                year = i.find('a').text
                seasons_lebron.append(year)
    return seasons_lebron

def get_season_mj():
    urls = ['https://www.basketball-reference.com/players/j/jordami01.html']
    seasons_mj = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:15]:
            season = row.find_all('th',{'data-stat':'season'})
            for i in season:
                year = i.find('a').text
                seasons_mj.append(year)
    return seasons_mj

def get_age_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    seasons_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:19]:
            age = row.find_all('td', {'data-stat':'age'})
            seasons_lebron.append(age[0].text)
    return seasons_lebron

def create_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

if __name__ == '__main__':
    lebron_season_lst = get_season_lebron()
    mj_season_lst = get_season_mj()
    lebron_age_lst = get_age_lebron()