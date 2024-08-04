from bs4 import BeautifulSoup
import requests
import pandas as pd

def html_scrape(league, year):
    """
    params
    ------
    league (str) : 'epl', 'mls-ec', 'mls-wc', or 'bundesliga'
    year (int) : year the competition season started
    
    returns
    -------
    HTML for a table of home stats 
    """
    if league == "epl":
        url = f'https://fbref.com/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats'
    elif league == "bundesliga":
        url = f'https://fbref.com/en/comps/20/{year}-{year+1}/{year}-{year+1}-Bundesliga-Stats'
    elif league == "mls-ec":
        url = f'https://fbref.com/en/comps/22/{year}/{year}-Major-League-Soccer-Stats'
    elif league == "mls-wc":
        url = f'https://fbref.com/en/comps/22/{year}/{year}-Major-League-Soccer-Stats'
    else:
        raise ValueError
    print("Requesting data from: ", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if league == "mls-wc":
        table = soup.find_all("table")[3]
    else:
        table = soup.find_all("table")[1]
    return table
    
def calc_gd_diff(cols):
    '''
    returns difference between home gd and away gd
    for season without this data, returns 0
    '''
    if len(cols) == 27:
        return int(cols[7].text) - int(cols[20].text)
    if len(cols) == 19:
        if cols[7].text == '':
            return 0
        return int(cols[7].text) - int(cols[16].text)

def calc_goal_diff(gf, ga):
    '''
    more readable implementation that works for both xg and goals
    slightly slower since it does float conversion on ints
    '''
    if gf == '':
        return 0
    return float(gf) - float(ga)

def html_to_data_frame(league, year):
    """
    params
    ------
    league (str) : 'epl' or 'mls'
    year (int) : for epl this is the 1st year in the xxxx-xxxx season
    
    returns
    -------
    data frame with desired stats for each team within chosen year
    """
    data = html_scrape(league, year) #get data for epl season from fbref

    df = pd.DataFrame() #intialize an empty data frame

    for row in data.find_all("tr"):
        cols = row.find_all("td")
        df_row = {}
        if cols == []: #skip the row if its empty
            continue
        if len(cols) == 27:
            home_games = int(cols[1].text)
            away_games = int(cols[14].text)
            home_points = int(cols[8].text)
            away_points = int(cols[21].text)
            home_gd = int(cols[7].text)
            away_gd = int(cols[20].text)
            df_row = {
                'team': cols[0].text.strip(),
                'season': year,
                'league': league,
                'mp': home_games + away_games,
                'pts_diff': home_points - away_points, 
                'gd': calc_goal_diff(home_gd, away_gd), #goal diff home - goal diff away
                'home_xg_overperf': calc_goal_diff(cols[5].text, cols[10].text) #how a team outperforms xG at home (goals for - xG)
            }
        elif len(cols) == 19: #for pre-xG season tables
            home_games = int(cols[1].text)
            away_games = int(cols[10].text)
            home_points = int(cols[8].text)
            away_points = int(cols[17].text)
            try: #for season tables without home vs away gd
                home_vs_away_gd = int(cols[7].text) - int(cols[16].text) #ex: (+5) - (-10) = 15
            except:
                home_vs_away_gd = 0
            df_row = {
                'team': cols[0].text.strip(),
                'season': year,
                'league': league,
                'mp': home_games + away_games,
                'pts_diff': home_points - away_points, 
                'gd': home_vs_away_gd, #goal differential
                'home_xg_overperf': 0
            }
        df = df._append(df_row, ignore_index=True) 
    return df

def calc_attendance(num_string):
    if num_string == '':
        return 0
    return int(num_string.replace(',',''))

def get_season_dataframe(season_url):
    response = requests.get(season_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", id="matchlogs_for")
    rows = table.find_all('tr')

    season_df = pd.DataFrame()

    for row in rows:
        cols = row.find_all('td')
        if cols != []:
            gf = cols[6].text[:2] #penalties are formatted as 0 (4) so need to ignore characters
            ga = cols[7].text[:2]
            xgf = cols[9].text #might be blank so don't convert to float yet
            xga = cols[10].text
            df_row = {
                'match_date' : row.find('th').text,
                'comp' : cols[1].text,
                'stage' : cols[2].text,
                'HAN' : cols[4].text[0],
                'vs' : cols[8].text,
                'gd' : calc_goal_diff(gf,ga),
                'xgd' : calc_goal_diff(xgf, xga),
                'attendance' : calc_attendance(cols[12].text)
            }
            season_df = season_df._append(df_row, ignore_index=True) #append match to season dataframe'
    return season_df

def get_disciplinary_record(season_url):
    response = requests.get(season_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", id="matchlogs_for")
    
    #initialize dataframe
    season_df = pd.DataFrame()

    #get opponent yellow card data
    opp_yellows = []
    rows_against = soup.find_all("table")[1].find_all('tr')
    for row in rows_against:
        cols = row.find_all('td')
        if cols  != []: #avoid headers and summary row
            opp_yellows.append(cols[8].text)
        else:
            opp_yellows.append(None) #so that indexes match with enumerate

    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cols = row.find_all('td')
        if cols != [] and cols[0].get('class') == ['right']: #avoid headers and summary row
            df_row = {
                'match_date' : row.find('th').text,
                'HAN' : cols[3].text[0],
                'vs' : cols[7].text,
                'team_yellows' : cols[8].text,
                'opponent_yellows' : opp_yellows[i],
                'team_fouls' : cols[11].text,
                'opponent_fouls' : cols[12].text
            }
            season_df = season_df._append(df_row, ignore_index=True) #append match to season dataframe
    return season_df