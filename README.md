# ANALYSIS OF HOME ADVANTAGE IN THE ENGLISH PREMIER LEAGUE

## Goals
A few months ago I watched [this YouTube video](https://www.youtube.com/watch?v=kNy5XBae9Eg) about home court advantage in the NBA and really appreciated how he quantified this advantage and measured its causes. I watch a lot of soccer (or football) and wanted to see if these same methods could be applied to the English top flight.

My basic methodology was to find soccer equivalents of all the statistics from MacKelvie's video and see if they followed the same trends as the basketball statistics.

| Basketball Statistic (from video) | Soccer Statistic          |
|-----------------------------------|---------------------------|
| Win % Difference                  | Home Points - Away Points |
| Home vs Away Point Differential   | Home GD - Away GD         |
| Travel Amount Before a Game       | Method described below    |
| Calls that benefit home team      | Yellow cards              |
| Open 3 Shooting                   | xG overperformance        |
| Attendance                        | Attendance                |

## Skills/Tools Used

- Scraping HTML tables with BeautifulSoup
- Summarizing data with pivot tables in Excel
- Creating charts in Excel

## Steps

1. [Fbref](https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats) conventiently has each Premier League season summarized in a table that includes points, goal differential, and xG.
   - [season_reader.py](code/season_reader.py) scrapes this data from the website and writes it to a csv file.
   - Also scraped this data for the American MLS and German Bundesliga
2. Some statistics are not summarized in the team table, so they need to be scraped manually match-by-match.
   - Starting with [links](datasets/epl_2023_teams) to each Premier League team's page, [team_reader.py](code/team_reader.py) scrapes data for match date, competition, stage, venue (home/away/neutral), opponent,   gd, expected gd, and attendance.
   - Yellow cards data comes from a separate page on the website so they are scraped by [scrape_disciplinary_record.py](code/scrape_disciplinary_record.py)
   - I only did this for 2023 because the 3 new teams per season from promotion/relegation would make the summarizaiton complicated
3. Getting data for stadium locations and sizes from Wikipedia
   - The team names are not formatted in the same way as on Fbref, so matching teams to stadiums was a semi-automated process using [stadium_finder.py](code/stadium_finder.py) to create the [dataset](datasets/stadium_data.csv)
4. Calculating attendance ([match_stats_calculator.py](code/match_stats_calculator.py))
   - Done by dividing Fbref's match attendance by stadium capacity from the Wikipedia dataset.
   - Has innacuracies due to temporary or recent changes in stadium capacity.
   - This stat is calculated for away and neutral games but is not used.
5. Calculating rest ([match_stats_calculator.py](code/match_stats_calculator.py))
   - [stadium_data.csv](datasets/stadium_data.csv) is read into a dictionary for fast lookup of stadium location but also to track where/when the team last played a game.
   - For each game, calculate_rest_diff() looks in this dictionary and compares how long each team has had since their last game. 
   - Factors in matches from other competitions (FA Cup, EFL Cup, and UEFA matches)
   - If a Premier League match doesn't have a previous game logged, assumes their last game was 7 days ago.
   - For non-Premier League matches, assumes both teams have equal rest.
6. Calculating travel ([match_stats_calculator.py](code/match_stats_calculator.py))
   - For each game, distance() is also used to calculate how far the away team's home stadium is from the game location.
   - calculate_distance_traveled() calculates how far the home team and away team traveled to get there, based on where their previous matches were.
   - If a team has had a match in the last 5 days, assumes they didn't go home and calculates the distance from their previous match to the current match.
   
## Conclusions 

### Conclusion 1

### Conclusion 2

### Conclusion 3

## Sources

-
-
-
