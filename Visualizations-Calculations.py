#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import matplotlib.pyplot as plt
import os
import numpy as np

def get_database(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    return cur,conn
    # cur.execute('''
    # SELECT TeamDivision.division, COUNT(*)
    # FROM PlayerStats
    # JOIN TeamDivision
    # ON PlayerStats.team = TeamDivision.team
    # GROUP BY TeamDivision.division''')
    # print(dict(cur))

def points_minutes_viz(cur,conn):
    points_lst = []
    minutes_lst = []
    cur.execute('''SELECT points, minutes_played FROM PlayerStats''')
    for row in cur:
        points_lst.append(row[0])
        minutes_lst.append(row[1])
    plt.scatter(minutes_lst,points_lst)
    plt.xlabel("Total Minutes Played")
    plt.ylabel("Total Points")
    plt.title("Efficiency of Top 100 PLayers in NBA Season 21 - 22")
    plt.tight_layout()
    plt.show()
    


if __name__ == "__main__":
    cur,conn = get_database('Top100nbaStats.db')
    viz1 = points_minutes_viz(cur,conn)