from reader_funcs import get_season_dataframe
import time
import os

in_file_path = 'C:/Users/fires/Python Projects/Home field advantage/epl_2023_teams.txt' #list of fbref team page links
out_file_path = "C:/Users/fires/Python Projects/Home field advantage/epl_match_data.csv"

teams_list = open(in_file_path, 'r').read().splitlines() #path to file of team pages

for team_url in teams_list:
    curr_df = get_season_dataframe(team_url)
    time.sleep(4) #avoid rate limiting (20 requests/min is maximum)
    file_exists = os.path.isfile(out_file_path)
    if file_exists:
        curr_df.to_csv(out_file_path, mode='a', index=False, header=False)
    else:
        curr_df.to_csv(out_file_path, index=False, header=True)
    print(team_url[57:], "  written to file")
