from reader_funcs import get_disciplinary_record
import time
import os

in_file_path = 'C:/Users/fires/Python Projects/Home field advantage/datasets/epl_2023_teams.txt' #list of fbref team page links
out_file_path = "C:/Users/fires/Python Projects/Home field advantage/datasets/epl_match_discipline.csv"

teams_list = open(in_file_path, 'r').read().splitlines() #path to file of team pages

for team_url in teams_list:
    team_url = team_url.replace("all_comps", "matchlogs/c9/misc").replace("Stats-All-Competitions", "Match-Logs-Premier-League")
    curr_df = get_disciplinary_record(team_url)
    time.sleep(4) #avoid rate limiting (20 requests/min is maximum)
    file_exists = os.path.isfile(out_file_path)
    if file_exists:
        curr_df.to_csv(out_file_path, mode='a', index=False, header=False)
    else:
        curr_df.to_csv(out_file_path, index=False, header=True)
    print(team_url[57:], "  written to file")
