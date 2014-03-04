use cfb_game_results;
create table play_by_play (game_code varchar(20),
                    play_number INT,
                    period_number INT,
                    clock INT,
                    o_team_code INT,
                    d_team_code INT,
                    o_poINTs INT,
                    d_poINTs INT,
                    down INT,
                    distance INT,
                    spot INT,
                    play_type varchar(32),
                    drive_num INT,
                    drive_play INT,
                    net_yards INT);

load data local infile '/home/tim/cfb_results/cfb_play_results_2005.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2006.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2007.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2008.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2009.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2010.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2011.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2012.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/cfb_results/cfb_play_results_2013.csv' -- path to directory
into table play_by_play
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

create table drive (game_code varchar(20),
                    drive_number INT,
                    o_team_code INT,
                    start_period INT,
                    start_clock INT,
                    start_spot INT,
                    start_reason varchar(30),
                    end_period INT,
                    end_clock INT,
                    end_spot INT,
                    end_reason varchar(30),
                    plays INT,
                    yards INT,
                    time_possession INT,
                    redzone INT,
                    d_team_code INT);

load data local infile '/home/tim/cfb_results/cfb_drive_results_2005-2013.csv' -- path to directory
into table drive
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

update results set d_team_code=mid(game_code,6,4) where mid(game_code,6,4) != o_team_code;
update results set d_team_code=mid(game_code,2,4) where mid(game_code,2,4) != o_team_code;
