#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import time

"""This file will create a database called 'LebronAndMJStats.db' with all statistics from MJ and Lebron's """

#=================LEBRON FUNCTIONS=================#
def get_season_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    seasons_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            season = row.find_all('th',{'data-stat':'season'})
            for i in season:
                year = i.find('a').text
                seasons_lebron.append(year)
    return seasons_lebron

def get_age_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    age_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            age = row.find_all('td', {'data-stat':'age'})
            age_lebron.append(age[0].text)
    return age_lebron

def get_minutes_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    minutes_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            age = row.find_all('td', {'data-stat':'mp'})
            minutes_lebron.append(age[0].text)
    return minutes_lebron

def get_points_lebron():
    urls = ['https://www.basketball-reference.com/players/j/jamesle01.html']
    points_lebron = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            points = row.find_all('td', {'data-stat':'pts'})
            points_lebron.append(points[0].text)
    return points_lebron

def get_fgm_lebron():
    count = 2003
    fgm_lebron = []
    for num in range(15):
        url = f'https://www.balldontlie.io/api/v1/season_averages?season={count}&player_ids[]=237'
        response = requests.get(url)
        data = response.json()
        count += 1
        for i in data:
            fgm = data[i][0]['fgm']
            fgm_lebron.append(fgm)
    return fgm_lebron


#=================MJ FUNCTIONS=================#






def get_season_mj():
    urls = ['https://www.basketball-reference.com/players/j/jordami01.html']
    seasons_mj = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            season = row.find_all('th',{'data-stat':'season'})
            for i in season:
                year = i.find('a').text
                seasons_mj.append(year)
    return seasons_mj

def get_age_mj():
    urls = ['https://www.basketball-reference.com/players/j/jordami01.html']
    age_mj = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            age = row.find_all('td', {'data-stat':'age'})
            age_mj.append(age[0].text)
    return age_mj

def get_minutes_mj():
    urls = ['https://www.basketball-reference.com/players/j/jordami01.html']
    minutes_mj = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            age = row.find_all('td', {'data-stat':'mp'})
            minutes_mj.append(age[0].text)
    return minutes_mj

def get_points_mj():
    urls = ['https://www.basketball-reference.com/players/j/jordami01.html']
    points_mj = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        table = soup.find('table', {'id':'totals'})
        rows = table.find_all('tr')
        for row in rows[1:16]:
            points = row.find_all('td', {'data-stat':'pts'})
            points_mj.append(points[0].text)
    return points_mj

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

def setUpLebronTable(cur, conn):
    seasons = get_season_lebron()
    age = get_age_lebron()
    minutes = get_minutes_lebron()
    points = get_points_lebron()
    fgm = get_fgm_lebron()
    cur.execute("DROP TABLE IF EXISTS Lebron")
    cur.execute("CREATE TABLE Lebron ('id' INTEGER PRIMARY KEY, 'Season' TEXT, 'Age' INTEGER, 'Minutes' INTEGER, 'Points' INTEGER, 'AVG_FGM' FLOAT)")
    for i in range(len(seasons)):
        cur.execute("INSERT INTO Lebron (id,Season,Age,Minutes,Points,AVG_FGM) VALUES (?,?,?,?,?,?)",(i,seasons[i],age[i],minutes[i],points[i],fgm[i]))
    conn.commit()

def setUpJordanTable(cur, conn):
    seasons = get_season_mj()
    age = get_age_mj()
    minutes = get_minutes_mj()
    points = get_points_mj()
    fgm = get_fgm_mj()
    cur.execute("DROP TABLE IF EXISTS Jordan")
    cur.execute("CREATE TABLE Jordan ('id' INTEGER PRIMARY KEY, 'Season' TEXT, 'Age' INTEGER, 'Minutes' INTEGER, 'Points' INTEGER, 'AVG_FGM' FLOAT)")
    for i in range(len(seasons)):
        cur.execute("INSERT INTO Jordan (id,Season,Age,Minutes,Points,AVG_FGM) VALUES (?,?,?,?,?,?)",(i,seasons[i],age[i],minutes[i],points[i],fgm[i]))
    conn.commit()



if __name__ == '__main__':
    lebron_season_lst = get_season_lebron()
    mj_season_lst = get_season_mj()
    lebron_age_lst = get_age_lebron()
    mj_age_lst = get_age_mj()
    lebron_minutes_lst = get_minutes_lebron()
    mj_minutes_lst = get_minutes_mj()
    mj_points_lst = get_points_mj()
    lebron_points_lst = get_points_lebron()
    lebron_fgm_lst = get_fgm_lebron()
    mj_fgm_lst = get_fgm_mj()

    cur,conn = create_database('LebronAndMJStats.db')
    lebronTable = setUpLebronTable(cur,conn)
    jordanTable = setUpJordanTable(cur,conn)