import csv
from time import time
from match_stats_funcs import *
from stadium_finder_funcs import append_row

match_dataset = 'C:/Users/fires/Python Projects/Home field advantage/datasets/epl_match_data.csv'
stadium_dataset = 'C:/Users/fires/Python Projects/Home field advantage/datasets/stadium_data.csv'
output_path = 'C:/Users/fires/Python Projects/Home field advantage/datasets/epl_matches_modified.csv'

#load in dictionary of teams
team_dict = {} 
with open(stadium_dataset, mode='r', newline='', encoding = 'cp850') as file:
    reader = csv.reader(file)
    next(reader, None) #skip header
    for stadium in reader:
        stadium.append(None) #add space in the array for home team's prev location
        stadium.append(None) #add space in the array for home team's prev gameday
        team_dict[stadium[0]] = stadium[1:] #stadium_dict[team] = [stadium name, lat, long, capacity, prevloc, prev_gameday]

#NOTES:
#need to keep away games because of FA cup/European matches where opponent's home perspective is not logged
#maybe cache until date changes and then write to file?
#should away games be flipped to opponent's home game?

with open(match_dataset, mode='r', newline='', encoding = 'cp850') as file:
    reader = csv.reader(file)
    next(reader, None) #skip header
    
    for match_data in reader: #[team,match_date,comp,stage,HAN,vs,gd,xgd,attendance]

        prem_team = match_data[0]
        prem_team_home = get_home_location(prem_team, team_dict)
        opponent = match_data[5]
        
        if match_data[2] == 'Premier League':
            if match_data[4] == 'H':
                #write a new row for the fixture
                modified_row = {
                'home' : prem_team,
                'away' : opponent,
                'comp' : match_data[2],
                'stage' : match_data[3],
                'match_date' : match_data[1],
                'gd' : match_data[6],
                'xgd' : match_data[7],
                'attendance %' : calculate_attendance(match_data, team_dict),
                'rest_advantage' : calculate_rest_diff(match_data, team_dict),
                'home_team_dist_traveled' : calc_dist_traveled(prem_team, prem_team_home, match_data[1], team_dict),
                'away_team_dist_traveled' : calc_dist_traveled(opponent, prem_team_home, match_data[1], team_dict),
                'distance_from_opp_home' : distance(prem_team_home, get_home_location(opponent, team_dict))
                }
                append_row(output_path, modified_row)
                
                #update previous match for both teams
                team_dict[prem_team][4] = team_dict[opponent][4] = prem_team_home #previous match coords
                #set both teams previous match date to this match
                team_dict[prem_team][5] = team_dict[opponent][5] = match_data[1] 
            #Note: ignoring Premier League away games since they will be represented as a home game elsewhere in the dataset
        else:
            #UCL Final, Domestic Finals/Semis, Super Cup
            if match_data[4] == 'N': 
                print(f"No venue for match: {prem_team} vs {opponent} on {match_data[1]}")
                coord_input = input("Give coordinates of neutral venue as:\n0.000 0.000\n").split()
                team_dict[prem_team][4] = (float(coord_input[0]),float(coord_input[1]))
            #cup away legs
            if match_data[4] == 'A': 
                team_dict[prem_team][4] = team_dict[opponent][4] = get_home_location(opponent, team_dict) #opponents home stadium
            #cup home legs
            if match_data[4] == 'H':
                team_dict[prem_team][4] = team_dict[opponent][4] = prem_team_home #prem team's home stadium
            #set both teams previous match date to this match regardless of type
            team_dict[prem_team][5] = team_dict[opponent][5] = match_data[1] 
        
print("Done")