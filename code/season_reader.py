from reader_funcs import html_to_data_frame
import os
import time

#arguments, could be done via command line or a function but I'm too lazy
start_year = 2023
end_year = 2002
league = "mls-wc"

'''
fbref has epl data going back to 1992
and mls (mls-ec or mls-wc) data going back to 2002
and bundesliga data going back to 1988
'''

file_path = f"C:/Users/fires/Python Projects/Home field advantage/{league}_data.csv"

for year in range(start_year, end_year-1, -1):
    time.sleep(4) #avoid rate limiting (20 requests/min is maximum)
    curr_df = html_to_data_frame(league, year)
    file_exists = os.path.isfile(file_path)
    if file_exists:
        curr_df.to_csv(file_path, mode='a', index=False, header=False)
    else:
        curr_df.to_csv(file_path, index=False, header=True)
    print(year, " season written to file")
