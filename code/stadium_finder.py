import csv
from stadium_finder_funcs import *

#wikipedia query used to get wikipedia_query.csv
'''
SELECT ?clubLabel ?venueLabel ?coordinates ?capacity
WHERE
{
  ?club wdt:P31 wd:Q476028 .
  ?club wdt:P115 ?venue .
  ?venue wdt:P625 ?coordinates .
  ?venue wdt:P1083 ?capacity .
  FILTER(?capacity > 1500)
  BIND(geof:latitude(?coordinates) AS ?lat)
  BIND(geof:longitude(?coordinates) AS ?lon)
  FILTER(?lat >= 31 && ?lat <= 73 && ?lon >= -14.5 && ?lon <= 42)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
'''
#This program creates a file with the stadium for every team in the matches in the dataset
#semi-auto since wikipedia team names don't match fbref team names

file_path = 'C:/Users/fires/Python Projects/Home field advantage/epl_match_data.csv'
wikipedia_file_path = 'C:/Users/fires/Python Projects/Home field advantage/wikipedia_query.csv'
output_file_path = 'C:/Users/fires/Python Projects/Home field advantage/stadium_data.csv'

#open matches file and add every team to a dictionary to get a list of unique teams
team_dict = {} #initialize an empty dictionary
with open(file_path, mode='r', newline='', encoding = 'cp850') as file:
    reader = csv.reader(file)
    next(reader, None) #skip header
    for row in reader:
        team_name = row[5]
        if team_name[0].islower(): #remove country code
            team_name = team_name[3:] 
        team_dict[team_name] = [] #add each team to the dictionary

#remove teams that have already gotten their stadium in the output file
with open(output_file_path, mode='r', newline='', encoding = 'cp850') as file:
    reader = csv.reader(file)
    next(reader, None) #skip header
    for row in reader:
        if row[0] in team_dict:
            print(row[0], "removed")
            del team_dict[row[0]]

print(team_dict)
#open wikipedia dataset and convert to a dictionary with cleaned team names
stadium_dict = {}
with open(wikipedia_file_path, mode='r', newline='', encoding = 'cp850') as file:
    reader = csv.reader(file)
    next(reader, None) #skip header
    for row in reader:
        key = clean_team_name(row[0])
        stadium_dict[key] = row[1:] #add each team to dictionary with venue name, coordinates and capacity list as the value

#search wikipedia dictionary for each team name and if a match is found, write data to the file
count = 0
for team in team_dict:
    data = []
    if team in stadium_dict:
        data = stadium_dict[team]
        print(team, ' found successfully')
    else: #if a team cannot be found automatically, the user can give the rest of the data manually
        print(team, ' not found')
        data = input('Give data as "Stadium Name,Point(),Capacity"?\n').split(',')
    coordinates = convert_coords(data[1])
    new_row = {
        'team' : team,
        'stadium_name' : data[0],
        'lat' : coordinates[0],
        'long' : coordinates[1],
        'capacity' : data[2]
        }
    try:
        append_row(output_file_path, new_row)
    except:
        print("Row formatting error. Skipping to next team.")
print("All teams logged")