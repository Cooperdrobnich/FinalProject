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
    plt.title("Efficiency of Top 100 Players in NBA Season 21 - 22")
    plt.tight_layout()
    plt.show()

def get_most_efficient(cur,conn):
    cur.execute('''SELECT name, points, minutes_played FROM PlayerStats''')
    efficiency_lst = []
    for row in cur:
        efficiency_lst.append(row)
    sorted_efficiency = sorted(efficiency_lst, key=lambda t: t[1]/t[2], reverse=True) 
    most_efficent_player = sorted_efficiency[0][0]
    most_efficent_ratio = sorted_efficiency[0][1] / sorted_efficiency[0][2]
    print("The most efficient player in the NBA Top 100 is " + str(most_efficent_player) + " scoring " + str(round(most_efficent_ratio,3)) + " points per minute.")
    


if __name__ == "__main__":
    cur,conn = get_database('Top100nbaStats.db')
    viz1 = points_minutes_viz(cur,conn)
    calc1 = get_most_efficient(cur,conn)