#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import time

"""This file will create a database called 'Top100nbaStats.db' with all statistics from the top 100 players in the NBA for the 2021 - 2022 season """

def get_player_names():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html'
    seasons_lebron = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        player = row.find_all('td',{'data-stat':'player'})
        for i in player:
            name = i.find('a').text
            seasons_lebron.append(name)
    print(seasons_lebron)
    

def get_fgm_mj():
    count = 1984
    fgm_mj = []
    for num in range(20):
        url = f'https://www.balldontlie.io/api/v1/season_averages?season={count}&player_ids[]=2931'
        response = requests.get(url)
        data = response.json()
        count += 1
        try:
            for i in data:
                fgm = data[i][0]['fgm']
                fgm_mj.append(fgm)
        except:
            continue
    return fgm_mj


def create_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn



if __name__ == '__main__':
    lebron_season_lst = get_player_names()

    cur,conn = create_database('Top100nbaStats.db')