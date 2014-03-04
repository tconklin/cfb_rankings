use cfb_game_results;
create table teams (team_code INT,
                    team_name varchar(32),
                    conf_code INT);

load data local infile '/home/tim/cfb_results/team.csv' -- path to directory
into table teams
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;


