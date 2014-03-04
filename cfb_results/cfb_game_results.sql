create database cfb_game_results;
use cfb_game_results;
create table results (team_code varchar(4),
                      game_code varchar(20),
                      rush_att INT,
                      rush_yard INT,
                      rush_td INT,
                      pass_att INT,
                      pass_comp INT,
                      pass_yd INT,
                      pass_td INT,
                      pass_int INT,
                      pass_conv INT,
                      kick_ret INT,
                      kick_ret_yds INT,
                      kick_ret_tds INT,
                      punt_ret INT,
                      punt_ret_yds INT,
                      punt_ret_td INT,
                      fum_ret INT,
                      fum_ret_yds INT,
                      fum_ret_td INT,
                      int_ret INT,
                      int_ret_yds INT,
                      int_ret_td INT,
                      misc_ret INT,
                      misc_ret_yds INT,
                      misc_ret_td INT,
                      fg_att INT,
                      fg_made INT,
                      xp_att INT,
                      xp_made INT,
                      xp2_att INT,
                      xp2_conv INT,
                      dxp2_att INT,
                      dxp2_conv INT,
                      safety INT,
                      points INT,
                      punt INT,
                      punt_yds INT,
                      kickoff INT,
                      kickoff_yds INT,
                      kickoff_tbs INT,
                      kickoff_ob INT,
                      kickoff_onside INT,
                      fumble INT,
                      fumble_lost INT,
                      tackle_solo INT,
                      tackle_assist INT,
                      tackle_loss INT,
                      tackle_loss_yds INT,
                      sack INT,
                      sack_yds INT,
                      qb_hurry INT,
                      fumble_forced INT,
                      pass_def INT,
                      kick_block INT,
                      first_run INT,
                      first_pass INT,
                      first_penalty INT,
                      time_poss INT,
                      penalty INT,
                      penalty_yds INT,
                      third_down_att INT,
                      third_down_conv INT,
                      fourth_down_att INT,
                      fourth_down_conv INT,
                      red_zone_att INT,
                      red_zone_td INT,
                      red_zone_fg INT,
                      season INT,
                      defense_code INT,
                      defense_points INT);


create table adjusted_wp (team_code varchar(4),
                          winning_percentage float,
                          adj_winning_percentage float,
                          SoS float,
                          pure_points float,
                          pure_points_sos float,
                          season INT);


load data local infile '/home/tim/cfb_results/cfb_game_results_2005-2013.csv' -- path to directory
into table results
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

update results set defense_code=mid(game_code,6,4) where mid(game_code,6,4) != offense_code;
update results set defense_code=mid(game_code,2,4) where mid(game_code,2,4) != offense_code;
update results as t1, results as t2 set t1.defense_points = t2.offense_points where t1.game_code = t2.game_code and t1.offense_code != t2.offense_code
