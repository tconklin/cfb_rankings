import numpy as np
import MySQLdb

db = MySQLdb.connect(passwd="057005223",db=nfl_pbp)
team_query = db.cursor() #query tool for teams
op = db.cursor() #query tool for original plays
np = db.cursor() #query tool for next plays
net_punt = np.zeros((10000,1))
count = 0

for y in range(2002,2013):
    team_query.execute("""select distinct offense from pbp order by offense asc""")
    team = team_query.fetchall()
    for j in range(np.shape(team)[0]):
        team_name = team[j][0] #teams name in alphabetical order
        ######################SPECIAL TEAMS#####################
        #Net Punting (offense)
        op.execute("""select play_id,ydline from pbp where offense = %s and description like '%%punts%%'""",(team_name,))
        punt_start = op.fetchall()
        for k in range(np.shape(punt_start)[0]):
            np.execute("""select ydline from pbp where play_id=%s and offense <> %s""",(punt_start[0][k]+1,team_name))
            punt_end = np.fetchall()
            net_punt[count] = punt_start[k][1]+punt_end[0][0]-100
            print net_punt[count]
            count += 1
        #Field Goals Made
        #Field Goals Attempted
        #Extra Points Made
        #Extra Points Attempted
        #Blocked Kicks
        #Net Punting (defense)
        ######################OFFENSE###########################
        #First Down (yards gained)
        #Second Down (yards gained)
        #Third Down (yards gained)
        #Fourth Down (yards gained)
        #First Down (yards to gain)
        #Second Down (yards to gain)
        #Third Down (yards to gain)
        #Fourth Down (yards to gain)
        #First Down (converted (during drive))
        #Second Down (converted (during drive))
        #Third Down (converted (during drive))
        #Fourth Down (converted)
        #Drive (points gained)
        #Drive (starting position)
        #Drive (ending position)
        #####################DEFENSE#############################
    



#####DEFINITIONS#######
#Garbage Time: score differential of 25+ entering the 4th quarter, 17+ with 5 min to play
#Net Punting: ydline_2+ydline_1-100
#Play Success: difference in first down odds after previous play (negative value for defense)
#Drive Success: difference in winning percentage between the beginning and end of the drive (negative value for defense)

