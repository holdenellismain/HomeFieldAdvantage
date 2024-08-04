from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

def distance(coord1, coord2):
    '''
    returns approximate distance between two points on Earth in miles
    '''
    R = 3958.8

    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])
                    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_attendance(match_data, team_dict):
    '''
    match_data (list) - [team,match_date,comp,stage,HAN,vs,gd,xgd,attendance]
    team_dict (dictionary)
    team_dict[team] = [stadium name, lat, long, capacity, prev_coords, prev_date]
    '''
    if match_data[4] == 'H':
        return int(match_data[8]) / int(team_dict[match_data[0]][3]) #attendance / stadium capacity from team_dict
    else:
        WEMBLEY = 90000
        return int(match_data[8]) / WEMBLEY
    
def calculate_rest_diff(match_data, team_dict):
    '''
    match_data (list) - [team,match_date,comp,stage,HAN,vs,gd,xgd,attendance]
    team_dict (dictionary)
    team_dict[team] = [stadium name, lat, long, capacity, prev_coords, prev_date]
    '''
    match_date = match_data[1]
    team_prev_match_date = team_dict[match_data[0]][5]
    opp_prev_match_date = team_dict[match_data[5]][5]
    
    date_format = "%m/%d/%Y"
    date1 = datetime.strptime(match_date, date_format)
    
    #for other competitions, assume that the other team has been playing games at an equal rate
    if match_data[2] != "Premier League":
        return 0 
    
    #in the premier league
    if team_prev_match_date and opp_prev_match_date: 
        date2 = datetime.strptime(team_prev_match_date, date_format)
        date3 = datetime.strptime(opp_prev_match_date, date_format)
        delta = (date1 - date2) - (date1 - date3)
        return delta.days
    if team_prev_match_date: #assume other team has 1 week of rest, for 1st games of season
        date2 = datetime.strptime(team_prev_match_date, date_format)
        return (date1 - date2).days - 7 
    if opp_prev_match_date: #assume 1st team has 2 weeks of rest, for 1st games of season
        date3 = datetime.strptime(opp_prev_match_date, date_format)
        return 7 - (date1 - date3).days 
    else: 
        return 0

def get_home_location(team_name, team_dict):
    '''
    team_dict[team_name] = [stadium name, lat, long, capacity, prev_coords, prev_date]
    
    returns array of lat, lon
    '''
    return float(team_dict[team_name][1]), float(team_dict[team_name][2])

def calc_dist_traveled(team_name, match_location, match_date, team_dict):
    '''
    Calculates the distance a team travels from their previous match to their current match
    If they haven't played a match for more than 5 days, returns how far the current match is from home
    
    team_dict[team_name] = [stadium name, lat, long, capacity, prev_coords, prev_date]
    
    Returns:
    miles (float) - how far a team traveled to get to the game
    0 indicates a home game
    '''
    team_home = get_home_location(team_name, team_dict)
    
    date_format = "%m/%d/%Y"
    match_date = datetime.strptime(match_date, date_format)
    prev_match_date = team_dict[team_name][5]
    #if the team has a previous match
    if prev_match_date:
        prev_match_date = datetime.strptime(prev_match_date, date_format)
        delta = (match_date - prev_match_date).days
        #if more than 5 days since previous game
        if delta > 5:
            #assume team returned home
            return distance(team_home, match_location)
        else:
            #calculate distance between previous game location and current match location
            return distance(team_dict[team_name][4], match_location)
    #if team does not have a previous match
    #calculate distance between their home stadium and their current match
    return distance(team_home, match_location)
    
    


