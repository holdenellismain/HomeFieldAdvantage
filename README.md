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

1. [FBref](https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats) conventiently has each Premier League season summarized in a table that includes points, goal differential, and xG.
   - [season_reader.py](code/season_reader.py) scrapes this data from the website and writes it to a csv file.
   - Also scraped this data for the American MLS and German Bundesliga
2. Some statistics are not summarized in the team table, so they need to be scraped manually match-by-match.
   - Starting with [links](datasets/epl_2023_teams) to each Premier League team's page, [team_reader.py](code/team_reader.py) scrapes data for match date, competition, stage, venue (home/away/neutral), opponent,   gd, expected gd, and attendance.
   - Yellow cards data comes from a separate page on the website so they are scraped by [scrape_disciplinary_record.py](code/scrape_disciplinary_record.py)
   - I only did this for 2023 because the 3 new teams per season from promotion/relegation would make the summarizaiton complicated
3. Getting data for stadium locations and sizes from Wikipedia
   - The team names are not formatted in the same way as on FBref, so matching teams to stadiums was a semi-automated process using [stadium_finder.py](code/stadium_finder.py) to create the [dataset](datasets/stadium_data.csv)
4. Calculating attendance ([match_stats_calculator.py](code/match_stats_calculator.py))
   - Done by dividing FBref's match attendance by stadium capacity from the Wikipedia dataset.
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
   - If a team has had a match in the last 5 days, the program assumes they didn't go home and calculates the distance from their previous match to the current match (road trips).
   - If a team did not have a match in the last 5 days, the program assumes they are coming from their home stadium.
7. Visualizing the data [Excel](charts.xlsx)
   - Data that was already summarized to the season could be directly plugged into charts but for some stats, I used Pivot Tables to agreggate it further by season or team.
   - Match data had to be summarized by team. I filtered to only include Premier League home matches. Including all matches would lead to many teams being in the final dataset that only played a few games against Premier League teams. Also neutral venues would make any modeling more complicated. 

## Conclusions 
### There is a measurable home field advantage in soccer.

The two statistics to estimate this advantage are home points - away points and home goal differential - away goal differential. They are very closely correlated as shown below, so I use them interchangably based on the sample.
![different measures](https://github.com/user-attachments/assets/362be50b-e40d-4868-a041-c7ec5a7d5919)
*MLS is used because home vs away goal differential is logged on FBref going back to 2002. It is only logged back to 2016-17 in the Premier League*<br>

Some teams have a stronger home field advantage than others. Below are the top 10 teams that have more than 5 seasons (at least 95 home games) in the Premier League.
![strongest home field advantage](https://github.com/user-attachments/assets/3b58707e-6f44-41c5-bacd-06b43b524e81)

### Referees Favor Home Teams
![excess yellows earned](https://github.com/user-attachments/assets/fb51c220-0058-4666-9c86-87cb475415ee)
By measuring the amount of yellow cards that a team earns at home relative to their traveling opponents, we see that 15/20 teams got carded less. This cannot be used to draw conclusions about referee bias though because there are many confounding variables. For example:
- Possession - a team is less likely to get carded if they have the ball since they don't have to play defense as much. Burnley did worse at home than away in terms of points earned but because they had high average possession, they had had their traveling opponents earning more yellows.
- Losing - teams will foul more when they are losing, which is why Sheffield, the worst team in the league, got lots of yellow cards at home.

### Travel is not a significant factor to home advantage in the Premier League
Originally I was using a more complicated measurement that accounts for travel time from previous match to get this plot:
![travel vs xg (delta distance)](https://github.com/user-attachments/assets/7be799c0-7ea4-4528-9a92-66ae0fdebf58)
*Explanation: The point at -2000 is from when Aston Villa played a home game against a well rested Liverpool 6 days after an away game in Greece. This should have theoretically reduced their home advantage, hence the negative travel advantage, but they created enough chances for 1 goal more than Liverpool. The point at +1485 is from a match where Chelsea came from Newcastle to play at home against Brighton, who played an away game in Greece 4 days prior. Most games have very little travel advantage, hence the cluster in the middle*<br>

An interesting pattern here is that any correlation that exists is negative, suggesting that teams that travelling long distances before Premier League away games gives a slight advantage. This is obviously not true and only occurs because the only teams that travel long distances are the teams that are good enough to qualify for international tournaments.<br>

This measurement had a very low R<sup>2</sup>, so I checked the more simple measurement of away team distance from home. I also got rid of games where the away team traveled less than 50 miles because this would be a short bus ride from home for all the players, so any disadvantage due to travel/insufficient rest would be minimal.
![travel vs xg](https://github.com/user-attachments/assets/1ffbc4f1-5890-454e-8736-8a7456d84bd8)
Here, the R<sup>2</sup> is slightly higher, but still insignificant.

## Attendance is inconclusive
![attendance](https://github.com/user-attachments/assets/8e63c3e3-186d-426f-be02-11e0bed5df82)
While this graph makes it look like there is no correlation between attendance and a home team winning, there are many issues with this model.
1. Stadium capacity measurements are not accurate
   - Certain Brighton home games were recorded as having over 120% attendance, which isn't possible.
   - Liverpool expanded their stadium part way through the season, so some games were at 100%, but in a smaller version of Anfield.
   - Many stadiums like London Stadium (West Ham) had multiple capacity figures listed online, and I don't know which one accurately represents a Premier League game.
2. There is very little variance in attendance team-to-team

There is strong evidence for fans affecting the game because in 2020/21 when games were played without fans due to COVID-19, home field advantage disappeared. Additionally, teams typically associated with having passionate fans like Newcastle and Liverpool rank on top of all home strength measurements.

## Points of Future Exploration
1. Do teams outperform their xG more often at home?
2. How does MLS compare for travel and rest advantages with its longer travel distances?
3. Could other leagues with worse attendance offer more insight into the correlation between attendance and winning?
4. A more complex model for yellow cards/fouls

## Sources
- Team and match data - [FBref](https://fbref.com)
- Stadium data - [Wikidata Query Service](https://query.wikidata.org/)
- Inspiration - [Michael MacKelvie, YouTube](https://www.youtube.com/watch?v=kNy5XBae9Eg)
