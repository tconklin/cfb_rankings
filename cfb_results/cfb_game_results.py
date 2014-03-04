import numpy as np
import MySQLdb
import os
import json


db = MySQLdb.connect(user=/user,passwd=/pw,db="cfb_game_results")
game_query = db.cursor() #query tool for teams
game_a = db.cursor() #query tool for original plays
insert_query = db.cursor()
insert_query.execute("""truncate table adjusted_wp;""")

for year in range(2005,2014):
  team_query = db.cursor()
  opponent_query = db.cursor()
  opponent_2_query = db.cursor()
  team_query.execute("""select team_code from (select count(*) as counter,team_code from results where season = %s group by team_code) as T1 where T1.counter > 5;""", (year,)) #only include rankings for teams that have played more than 5 games
  team_codes = team_query.fetchall()
  n_teams = np.size(team_codes)
  print n_teams
  team_db = np.zeros((n_teams,11))
  adj_wp = np.zeros((n_teams,6))
  for j in range(n_teams):
    #print team_codes[j][0]
    team_query.execute("""select count(*) from results where team_code = %s and points > defense_points and season = %s""", (team_codes[j][0],year,))
    wins = team_query.fetchall()
    team_query.execute("""select count(*) from results where team_code = %s and points < defense_points and season = %s""", (team_codes[j][0],year,))
    losses = team_query.fetchall()
    team_query.execute("""select points,defense_points,team_code,left(game_code,5) from results where team_code = %s and season = %s""", (team_codes[j][0],year,))
    win_points = team_query.fetchall()
    win_points = np.array(win_points)
    t_win_points = 0
    ngames = np.shape(win_points)[0]
    for m in range(ngames):
       home_away = float(float(win_points[m,2])==float(win_points[m,3]))
       home_multiplier = 7.3*(-1)**(home_away-1)
       q_points = (float(win_points[m,0])+home_multiplier)/(float(win_points[m,0])+float(win_points[m,1])+home_multiplier)/float(np.shape(win_points)[0])+.25/ngames*np.sign(float(win_points[m,0])-float(win_points[m,1]))
       q_points = max(q_points,0)
       q_points = min(q_points, 1./ngames)
       t_win_points += q_points
    print t_win_points
    opponent_query.execute("""select defense_code from results where team_code = %s and season = %s""", (team_codes[j][0],year,))
    opponents = opponent_query.fetchall()
    n_opponents = np.size(opponents)
    wins2 = -int(wins[0][0])
    losses2 = -int(losses[0][0])
    wins3 = 0
    losses3 = 0
    for k in range(n_opponents):
        opponent_query.execute("""select count(*) from results where team_code = %s and points > defense_points and season = %s""", (opponents[k][0],year,))
        wins2_a = opponent_query.fetchall()
        opponent_query.execute("""select count(*) from results where team_code = %s and points < defense_points and season = %s""", (opponents[k][0],year,))
        losses2_a = opponent_query.fetchall()
        wins2 += wins2_a[0][0]
        losses2 += losses2_a[0][0]
        wins3 -= wins2
        losses3 -= losses2
        for l in range(n_opponents):
            opponent_2_query.execute("""select count(*) from results where team_code = %s and points > defense_points and season = %s""", (opponents[l][0],year,))
            wins3_a = opponent_2_query.fetchall()
            opponent_2_query.execute("""select count(*) from results where team_code = %s and points < defense_points and season = %s""", (opponents[l][0],year,))
            losses3_a = opponent_2_query.fetchall()
            wins3 += wins3_a[0][0]
            losses3 += losses3_a[0][0]

    team_db[j,:] = [int(team_codes[j][0]), int(wins[0][0]), int(losses[0][0]), 0, int(wins2), int(losses2), 0, int(wins3), int(losses3), 0, t_win_points]
    team_db[j,3] = team_db[j,1]/(team_db[j,1]+team_db[j,2])
    team_db[j,6] = team_db[j,4]/(team_db[j,4]+team_db[j,5])
    team_db[j,9] = team_db[j,7]/(team_db[j,7]+team_db[j,8])

  adj_wp[:,0] = team_db[:,0]
  adj_wp[:,1] = team_db[:,3]
  adj_wp[:,2] = team_db[:,3]*(team_db[:,6]/np.mean(team_db[:,6]))**0.333333*(team_db[:,9]/np.mean(team_db[:,9]))**.111111
  adj_wp[:,3] = (team_db[:,6]/np.mean(team_db[:,6]))*(team_db[:,9]/np.mean(team_db[:,9]))**.33333
  adj_wp[:,4] = team_db[:,10]
  adj_wp[:,5] = team_db[:,10]*(team_db[:,6]/np.mean(team_db[:,6]))**0.33333*(team_db[:,9]/np.mean(team_db[:,9]))**0.11111
  for j in range(n_teams):
    insert_query.execute("""insert into adjusted_wp (team_code, winning_percentage, adj_winning_percentage, SoS, pure_points, pure_points_sos, season) values(%s, %s, %s, %s, %s, %s, %s)""",(str(int(adj_wp[j,0])),str(adj_wp[j,1]),str(adj_wp[j,2]),str(adj_wp[j,3]),str(adj_wp[j,4]),str(adj_wp[j,5]),str(year)))

