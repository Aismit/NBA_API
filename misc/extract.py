from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def players():
    # NBA season we will be analyzing
    year = 2019
    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)

    # use findAll() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText() to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    stats = pd.DataFrame(player_stats, columns = headers)
    stats.to_csv("players.csv")
    
    
def teams():

    year = 2019

    url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(year)

    html = urlopen(url)

    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]

    # isolate names of teams from headers
    teams = headers[7:22] + headers[30:]

    # add "Name" attribute and remove team names from headers
    headers = ["Name"] + headers[:7]

    rows = soup.findAll('tr')[1:]
    team_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

    team_stats.pop(0)
    team_stats.pop(15)

    # add values of names to rows
    for i in range(30):
        team_stats[i] = [teams[i]] + team_stats[i]

    stats = pd.DataFrame(team_stats, columns = headers)
    stats.to_csv("teams.csv")
