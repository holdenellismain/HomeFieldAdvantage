import csv
import os

def convert_coords(coordinates_str):
    pos1 = coordinates_str.find('(')
    pos2 = coordinates_str.find(' ')
    pos3 = coordinates_str.find(')')
    return coordinates_str[pos2+1:pos3], coordinates_str[pos1+1:pos2]

def clean_team_name(team_str):
    '''
    inefficient af but better than doing it manually
    '''
    key = team_str.split()
    try:
        key.remove('1.') #bunesliga teams labeled this way
    except:
        pass
    try:
        key.remove('F.C.')
    except:
        pass
    try:
        key.remove('FC')
    except:
        pass
    try:
        key.remove('C.F.')
    except:
        pass
    try:
        key.remove('CF')
    except:
        pass
    try:
        key.remove('SG')
    except:
        pass
    if len(key) > 2: #reduce long names
        key = key[:2]
    key = ' '.join(key)
    return key

def append_row(file_path, dict_data):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding = 'cp850') as csvfile:
        # Get the fieldnames from the dictionary keys
        fieldnames = dict_data.keys()
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(dict_data)