#FINAL PROJECT
#GROUP NAME: 707 BACKLOT BOYZ
#GROUP MEMBERS: COOPER DROBNICH & ADAM BRENNER

import sqlite3
import matplotlib.pyplot as plt
import os
import numpy as np

'''This function connects to the Top100nbaStats database'''
def get_database(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    return cur,conn

'''
This function creates a scatter plot with minutes played on the x-axis and
total points on the y-axis. It plots the most efficient player (the player with the highest
points per minute) in blue, the top 25 players in green, the middle 50 players in orange,
and the bottom 25 players in red. 
'''
def points_minutes_viz(cur,conn):
    points_lst = []
    minutes_lst = []
    efficiency_lst = []
    cur.execute('''SELECT points, minutes_played FROM PlayerStats''')
    for row in cur:
        points_lst.append(row[0])
        minutes_lst.append(row[1])
        efficiency_lst.append(row)
    #sorts players from largest to smallest by (points/minutes played)
    sorted_efficiency = sorted(efficiency_lst, key=lambda t: t[0]/t[1], reverse=True)
    eff_pts = []
    eff_min = []
    eff_pts.append(sorted_efficiency[0][0])
    eff_min.append(sorted_efficiency[0][1])
    top25pts = []
    top25min = []
    middle50_pts = []
    middle50_min = []
    for i in sorted_efficiency[1:25]:
        top25pts.append(i[0])
        top25min.append(i[1])
    for i in sorted_efficiency[25:75]:
        middle50_pts.append(i[0])
        middle50_min.append(i[1])
    plt.scatter(minutes_lst,points_lst, color='red')
    plt.scatter(eff_min,eff_pts,color="blue")
    plt.scatter(top25min,top25pts,color="green")
    plt.scatter(middle50_min, middle50_pts, color="orange")
    plt.xlabel("Total Minutes Played")
    plt.ylabel("Total Points")
    plt.title("Efficiency of Top 100 Players in NBA Season 21 - 22")
    plt.tight_layout()
    plt.show()

'''
This function creates a scatter plot with minutes played on the x-axis and
total turnovers on the y-axis. It plots the player with the largest turnover ratio 
in blue, the top 25 turnover ratio players in green, the middle 50 turnover ratio players 
in orange, and the bottom 25 turnover ratio players in red. 
in blue, the top 25 turnover ratio players in red, the middle 50 turnover ratio players 
in orange, and the bottom 25 turnover ratio players in green. 
'''
def turnovers_minutes_viz(cur,conn):
    turnovers_lst = []
    minutes_lst = []
    most_turnovers_lst = []
    cur.execute('''SELECT turnovers, minutes_played FROM PlayerStats''')
    for row in cur:
        turnovers_lst.append(row[0])
        minutes_lst.append(row[1])
        most_turnovers_lst.append(row)
    #sorts players from largest to smallest by (turnovers/minutes played)
    sorted_turnovers = sorted(most_turnovers_lst, key=lambda t: t[0]/t[1], reverse=True)
    most_turns = []
    most_turns_mins = []
    most_turns.append(sorted_turnovers[0][0])
    most_turns_mins.append(sorted_turnovers[0][1])
    top25 = []
    top25_min = []
    middle50 = []
    middle50_min = []
    for i in sorted_turnovers[1:25]:
        top25.append(i[0])
        top25_min.append(i[1])
    for i in sorted_turnovers[25:75]:
        middle50.append(i[0])
        middle50_min.append(i[1])
    plt.scatter(minutes_lst,turnovers_lst, color="green")
    plt.scatter(most_turns_mins, most_turns, color="blue")
    plt.scatter(top25_min,top25,color="red")
    plt.scatter(middle50_min, middle50, color="orange")
    plt.xlabel("Total Minutes Played")
    plt.ylabel("Total Turnovers")
    plt.title("Turnover Rate of Top 100 Players in NBA Season 21 - 22")
    plt.tight_layout()
    plt.show()

'''
This function gets the player with the highest points per minute from the database table,
PlayerStats by sorting all of the players into a list. This function returns the sorted
efficiency list with the format [(player1, points, minutes), (player2, points, minutes), ...].
This function also prints the player with the highest efficiency.
'''
def get_most_efficient(cur,conn):
    cur.execute('''SELECT name, points, minutes_played FROM PlayerStats''')
    efficiency_lst = []
    for row in cur:
        efficiency_lst.append(row)
    sorted_efficiency = sorted(efficiency_lst, key=lambda t: t[1]/t[2], reverse=True) 
    most_efficent_player = sorted_efficiency[0][0]
    most_efficent_ratio = sorted_efficiency[0][1] / sorted_efficiency[0][2]
    print("The most efficient player in the NBA Top 100 is " + str(most_efficent_player) + " scoring " + str(round(most_efficent_ratio,3)) + " points per minute.")
    return sorted_efficiency

'''
This function gets the player with the highest turnovers per minute from the database table,
PlayerStats by sorting all of the players into a list. This function returns the sorted
turnover ratio list with the format [(player1, turnovers, minutes), (player2, turnovers, minutes), ...].
This function also prints the player with the highest turnover ratio.
'''
def get_highest_turnover_rate(cur,conn):
    cur.execute('''SELECT name, turnovers, minutes_played FROM PlayerStats''')
    turnover_lst = []
    for row in cur:
        turnover_lst.append(row)
    turnover_efficiency = sorted(turnover_lst, key=lambda t: t[1]/t[2], reverse=True) 
    highest_turnover_rate = turnover_efficiency[0][0]
    turnover_ratio = turnover_efficiency[0][1] / turnover_efficiency[0][2]
    print("The player with the highest turnover rate in the NBA Top 100 is " + str(highest_turnover_rate) + " turning the ball over " + str(round(turnover_ratio,3)) + " times per minute.")
    return turnover_efficiency

'''
This function joins PlayerStats and TeamDivision on PlayerStats.team = TeamDivision.team.
It gets the count of players in the top 100 for each division and returns a dictionary with 
the division as the key and the number of players as the value.
Ex. {'Atlantic': 12, 'Central': 20, 'Northwest': 18, 'Pacific': 12, 'Southeast': 12, 'Southwest': 16}
'''
def get_division_dict(cur,conn):
    cur.execute('''
    SELECT TeamDivision.division, COUNT(*)
    FROM PlayerStats
    JOIN TeamDivision
    ON PlayerStats.team = TeamDivision.team
    GROUP BY TeamDivision.division''')
    return(dict(cur))

'''
This function creates a bar plot with division on the x-axis and
number of players on the y-axis. It rturns a dictionary that is sorted from largest
to smallest number of players for the divisions. It also prints the division with
the most players in the NBA top 100.
'''
def division_viz(dict):
    sorted_dict = sorted(dict.items(),key = lambda x:x[1], reverse=True)
    divisionlst = []
    numlst = []
    for i in dict:
        divisionlst.append(i)
        numlst.append(dict[i])
    plt.bar(divisionlst, numlst, align='center', alpha=1, width=0.8, color='blue')
    plt.xticks(divisionlst, rotation = 90)
    plt.ylabel('Number of Players')
    plt.xlabel('Divisions')
    plt.title('Number of Top 100 Players for Each Division')
    plt.tight_layout()
    plt.show()
    print("The division with the most top 100 players in the NBA is the " + sorted_dict[0][0] + " division with " + str(sorted_dict[0][1]) + " players.")
    return sorted_dict

'''
This function writes all of the calculations for each player/division in a text file called 'playerCalculations.txt'.
The text file has the ranks for the players with the top points per minute and turnovers per minute, as well as, 
the number of players in the top 100 for each division.
'''
def write_calculations(eff,turn,divs):
    count = 1
    with open('playerCalculations.txt','w') as f:
        f.write("The most efficient player in the NBA Top 100 is " + str(eff[0][0]) + " scoring " + str(round((eff[0][1]/eff[0][2]),3)) + " points per minute. \n")
        f.write("The player with the highest turnover rate in the NBA Top 100 is " + str(turn[0][0]) + " turning the ball over " + str(round((turn[0][1]/turn[0][2]),3)) + " times per minute. \n")
        f.write("The division with the most top 100 players in the NBA is the " + divs[0][0] + " division with " + str(divs[0][1]) + " players. \n")
        f.write("=======================================================================================\n")
        for i in range(len(eff)):
            f.writelines("-------------"+str(count)+"-------------\n")
            f.writelines(eff[i][0]+" scores about " + str(round((eff[i][1]/eff[i][2]),3)) + " points per minute \n")
            f.writelines(turn[i][0]+" turns the ball over about " + str(round((turn[i][1]/turn[i][2]),3)) + " times per minute \n")
            count += 1
        f.write("=======================================================================================\n")
        for div in divs:
            f.writelines("The " + div[0]+ " division has " + str(div[1])+" players in the NBA top 100 \n")
        f.close()

if __name__ == "__main__":
    cur,conn = get_database('Top100nbaStats.db')
    viz1 = points_minutes_viz(cur,conn)
    viz2 = turnovers_minutes_viz(cur, conn)
    calc1 = get_most_efficient(cur,conn)
    calc2 = get_highest_turnover_rate(cur,conn)
    div_dict = get_division_dict(cur,conn)
    viz3andcalc3 = division_viz(div_dict)

    write = write_calculations(calc1,calc2,viz3andcalc3)