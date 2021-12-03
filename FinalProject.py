#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup

"""This file will create a database called 'LebronAndMJStats.db' with all statistics from MJ and Lebron's """

def get_season():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html','https://www.basketball-reference.com/players/j/jordami01.html']
    seasons = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')



def create_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

if __name__ == '__main__':
    season_lst = get_season()