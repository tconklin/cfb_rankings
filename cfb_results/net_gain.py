import numpy as np
import MySQLdb
import os
import json


db = MySQLdb.connect(user="root",passwd="057005223",db="cfb_game_results")
play_query = db.cursor() #query tool for teams
play_query.execute("""select play_number, spot, play_type, o_team_code,	o_points, game_code from play_by_play""")
play_codes = play_query.fetchall()
play_codes = np.array(play_codes)
net_gain = ["-999" for x in range(np.shape(play_codes)[0])]
for j in range(np.shape(play_codes)[0]-1):
    play_number = play_codes[j,0]
    game_code = play_codes[j,5]
    if play_codes[j,2] == 'KICKOFF':
        net_gain[j] = str(float(play_codes[j,1])+float(play_codes[j+1,1])-100.)
    elif play_codes[j,2] == 'PUNT':
        net_gain[j] = str(float(play_codes[j,1])+float(play_codes[j+1,1])-100.)
    elif play_codes[j,2] == 'FIELD_GOAL':
        net_gain[j] = str(float(play_codes[j,1])+18.)
    elif play_codes[j,2] == 'ATTEMPT':
        net_gain[j] = str(float(play_codes[j+1,4])-float(play_codes[j,4]))
        #print 'attemp', net_gain, play_codes[j,4], play_codes[j+1,4]
    elif float(play_codes[j,0])<float(play_codes[j+1,0]) and play_codes[j,3] == play_codes[j+1,3] and play_codes[j+1,2] != 'KICKOFF': #normal play
        net_gain[j] = str(float(play_codes[j,1])-float(play_codes[j+1,1]))
    elif float(play_codes[j,0])<float(play_codes[j+1,0]) and play_codes[j,3] != play_codes[j+1,3] and play_codes[j+1,2] != 'KICKOFF': #turnover
        net_gain[j] = str(float(play_codes[j,1])+float(play_codes[j+1,1])-100.)
    else:
        net_gain[j] = str(-999.)

net_gain_out = np.array([net_gain,play_codes[:,0],play_codes[:,5]])
np.savetxt('net_gain.txt',np.transpose(net_gain_out),fmt='%s',delimiter=',')

