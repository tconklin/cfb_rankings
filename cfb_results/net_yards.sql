use cfb_game_results;

load data local infile '/home/tim/cfb_results/net_gain.txt' -- path to directory
into table tmptab
columns terminated by ','
optionally enclosed by '"'
lines terminated by '/n'
(net_yards, play_number, game_code);
