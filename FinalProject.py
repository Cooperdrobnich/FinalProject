#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup

"""This file will create a database called 'Top100nbaStats.db' with all statistics from the top 100 players in the NBA for the 2021 - 2022 season """

def get_player_names():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    players = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        player = row.find_all('td',{'data-stat':'player'})
        for i in player:
            name = i.find('a').text
            players.append(name)
    return players

def get_team():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    team_abbr = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        team = row.find_all('td',{'data-stat':'team_id'})
        for i in team:
            team_id = i.find('a').text
            team_abbr.append(team_id)
    return team_abbr

def get_minutes_played():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    minutes_played = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        mp = row.find_all('td',{'data-stat':'mp'})
        try:
            minutes_played.append(int(mp[0].text))
        except:
            continue
    return minutes_played

def get_points():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    total_points = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        pts = row.find_all('td',{'data-stat':'pts'})
        try:
            total_points.append(int(pts[0].text))
        except:
            continue
    return total_points

def get_turnovers():
    url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
    turnovers = []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        tov = row.find_all('td',{'data-stat':'tov'})
        try:
            turnovers.append(int(tov[0].text))
        except:
            continue
    return turnovers

def create_data_dict():
    data_dict = {}

def get_id_team():
    id_abbr = {}
    url ='https://www.balldontlie.io/api/v1/teams'
    response = requests.get(url)
    data = response.json()
    for i in data['data']:
        abbr = i['abbreviation']
        division = i['division']
        if abbr not in id_abbr:
            id_abbr[abbr] = division
    return id_abbr

def create_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

def create_table(cur,conn):
    player = get_player_names()
    team = get_team()
    mp = get_minutes_played()
    pts = get_points()
    turnover = get_turnovers()
    cur.execute("DROP TABLE IF EXISTS PlayerStats")
    cur.execute("""CREATE TABLE PlayerStats 
    ('name' TEXT PRIMARY KEY, 'team' TEXT,'minutes_played' INTEGER, 'points' INTEGER, 'turnovers' INTEGER)""")
    for i in range(len(player)):
        cur.execute('''INSERT INTO PlayerStats 
        (name, team, minutes_played, points, turnovers) VALUES (?,?,?,?,?)''', (player[i], team[i], mp[i], pts[i], turnover[i]))
    conn.commit()



if __name__ == '__main__':
    player_lst = get_player_names()
    team_lst = get_team()
    mp_lst = get_minutes_played()
    pts_lst = get_points()
    turnover_lst = get_turnovers()
    id_abbr_dict = get_id_team()


    cur,conn = create_database('Top100nbaStats.db')
    table = create_table(cur,conn)