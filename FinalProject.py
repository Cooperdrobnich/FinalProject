#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup

"""This file will create a database called 'Top100nbaStats.db' with all statistics from the top 100 scoring players in the NBA for the 2021 - 2022 season """

'''
This function uses beautiful soup to parse through the urls table data. This function then
returns a list of all the players in the current 21'-22' NBA season.
'''
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

'''
This function uses beautiful soup to parse through the urls table data. This function then
returns a list of all the team abbreviations correlated to the players from the function 
above in the current 21'-22' NBA season.
'''
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

'''
This function uses beautiful soup to parse through the urls table data. This function then
returns a list of the total minutes played correlated to the players from the first function 
in the current 21'-22' NBA season.
'''
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

'''
This function uses beautiful soup to parse through the urls table data. This function then
returns a list of the total number of points correlated to the players from the first function 
in the current 21'-22' NBA season.
'''
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

'''
This function uses beautiful soup to parse through the urls table data. This function then
returns a list of the total number of turnovers correlated to the players from the first function 
in the current 21'-22' NBA season.
'''
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

'''
This function takes in a list of players, team abbreviations, minutes_played, total points,
and total turnovers and adds them to a dictionary called data_dict with player being the key and
a dictionary as the value. Within the value dictionary it has the players specific stat titles as 
the keys and the stat as the value. 
Ex. {'Precious Achiuwa': {'team': 'TOR', 'minutes_played': 556, 'points': 168, 'turnovers': 23}
The function then sorts the list from highest to lowest total points scored by players. Finally,
it returns a dictionary of the top 100 NBA players stats by points.
'''
def create_data_dict(player,team,mp,pts,turnover):
    data_dict = {}
    for i in range(len(player)):
        #formats the dictionary into the correct format
        data_dict[player[i]] = {'team':team[i], 'minutes_played':mp[i],'points':pts[i],'turnovers':turnover[i]}
    #sorts dictionary from highest to lowest total points
    sorted_dict = list(sorted(data_dict.items(), key = lambda x:x[1]['points'], reverse=True))
    return(sorted_dict[:100])

'''
This function uses the 'balldontlie' API to create a dictionary with the team abbreviation
as the key and the correlating division for that specific team as the value. This function
returns a dictionary in this format...
Ex. {'ATL': 'Southeast', 'BOS': 'Atlantic', 'BKN': 'Atlantic', 'CHA': 'Southeast', ... }
'''
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

'''This function creates a database called 'Top100nbaStats.db' '''
def create_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

'''
This function creates two tables within 'Top100nbaStats.db', 'PlayerStats' and 'TeamDivision'.
The PlayerStats table has column headers name, team, minutes_played, points, and turnovers. The
TeamDivision table has coliumn headers team and division.
'''
def create_table(cur,conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS PlayerStats 
    ('name' TEXT PRIMARY KEY, 'team' TEXT,'minutes_played' INTEGER, 'points' INTEGER, 'turnovers' INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS TeamDivision ('team' TEXT PRIMARY KEY, 'division' TEXT)""")
    conn.commit()

'''
This function takes in a dictionary from the create_data_dict() function and inserts the stats
for 25 unique players into the PlayerStats table. 
'''    
def insert_player_data(cur,conn,data):
    cur.execute("SELECT name FROM PlayerStats")
    lst = []
    for i in cur:
        #appends existing player names from PlayerStats into lst
        lst.append(i[0])
    count = 0
    for i in range(len(data)):
        #if the name from the data_dict is not in lst it inserts it into the database table
        if data[i][0] not in lst:
            name = data[i][0]
            team = data[i][1]['team']
            minutes = data[i][1]['minutes_played']
            points = data[i][1]['points']
            turnovers = data[i][1]['turnovers']
            cur.execute('''INSERT INTO PlayerStats 
            (name, team, minutes_played, points, turnovers) VALUES (?,?,?,?,?)''',(name,team,minutes,points,turnovers))
            count += 1
            #limits the number of players added to the database to 25
            if count == 25:
                break
    conn.commit()

'''
This function takes in a dictionary from the get_id_team() function and inserts the division
for 25 unique teams into the TeamDivision table. 
''' 
def insert_team_data(data,cur,conn):
    cur.execute("SELECT team FROM TeamDivision")
    lst = []
    for i in cur:
        #appends existing team abbreviations names from TeamDivision into lst
        lst.append(i[0])
    count = 0
    for i in data:
        #if the team abbreviation from the data_dict is not in lst it inserts it into the database table
        if i not in lst:
            team = i
            division = data[i]
            cur.execute('''INSERT INTO TeamDivision
            (team, division) VALUES (?,?)''',(team,division))
            count += 1
            #limits the number of players added to the database to 25
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
    