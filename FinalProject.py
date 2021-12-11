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

def create_data_dict(player,team,mp,pts,turnover):
    data_dict = {}
    for i in range(len(player)):
        data_dict[player[i]] = {'team':team[i], 'minutes_played':mp[i],'points':pts[i],'turnovers':turnover[i]}
    sorted_dict = list(sorted(data_dict.items(), key = lambda x:x[1]['points'], reverse=True))
    return(sorted_dict[:100])

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
    cur.execute("""CREATE TABLE IF NOT EXISTS PlayerStats 
    ('name' TEXT PRIMARY KEY, 'team' TEXT,'minutes_played' INTEGER, 'points' INTEGER, 'turnovers' INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS TeamDivision ('team' TEXT PRIMARY KEY, 'division' TEXT)""")
    conn.commit()
    
def insert_player_data(cur,conn,data):
    cur.execute("SELECT name FROM PlayerStats")
    lst = []
    for i in cur:
        lst.append(i[0])
    count = 0
    for i in range(len(data)):
        if data[i][0] not in lst:
            name = data[i][0]
            team = data[i][1]['team']
            minutes = data[i][1]['minutes_played']
            points = data[i][1]['points']
            turnovers = data[i][1]['turnovers']
            cur.execute('''INSERT INTO PlayerStats 
            (name, team, minutes_played, points, turnovers) VALUES (?,?,?,?,?)''',(name,team,minutes,points,turnovers))
            count += 1
            if count == 25:
                break
    conn.commit()

def insert_team_data(data,cur,conn):
    cur.execute("SELECT team FROM TeamDivision")
    lst = []
    for i in cur:
        lst.append(i[0])
    count = 0
    for i in data:
        if i not in lst:
            team = i
            division = data[i]
            cur.execute('''INSERT INTO TeamDivision
            (team, division) VALUES (?,?)''',(team,division))
            count += 1
            if count == 25:
                break
    conn.commit()

if __name__ == '__main__':
    player_lst = get_player_names()
    team_lst = get_team()
    mp_lst = get_minutes_played()
    pts_lst = get_points()
    turnover_lst = get_turnovers()
    id_abbr_dict = get_id_team()
    data_dict = create_data_dict(player_lst,team_lst,mp_lst,pts_lst,turnover_lst)

    cur,conn = create_database('Top100nbaStats.db')
    table = create_table(cur,conn)
    insert_player = insert_player_data(cur, conn, data_dict)
    insert_team = insert_team_data(id_abbr_dict,cur,conn)