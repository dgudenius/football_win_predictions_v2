from util import *
from Pythag_Win import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}


@staticmethod
def count_scores(games):
    """ Generates win probabilities in the my_prob1 field for each game based on Pythagorean Win Theorem model """

    # Initialize team objects(?)
    teams = {}
    for row in [item for item in csv.DictReader(open("data/initial_elos.csv"))]:
        teams[row['team']] = {
            'name': row['team'],
            'season': 'season',
            'Pwin': float(new_team / 100),
            'Pfor': [],
            'Pagainst': [],
            'elo': float(row['elo']),
            'Wfor': [],
            'WforSum': 0,
            'WinTable': .5
        }

    for game in games:

        team1, team2 = teams[game['team1']], teams[game['team2']]

        # Revert teams at the start of seasons
        for team in [team1, team2]:
            if team['season'] and game['season'] != team['season']:
                team['Wfor'] = []
                # Revert Pythag Win points
                team['Pfor'][:] = [n / v_value for n in team['Pfor']]
                team['Pagainst'][:] = [n / v_value for n in team['Pagainst']]
                k = "%s%s" % (team['name'], game['season'])
                if k in REVERSIONS:
                    team['elo'] = REVERSIONS[k]
                else:
                    team['elo'] = 1505.0 * REVERT + team['elo'] * (1 - REVERT)
            team['season'] = game['season']

            if game['score1'] != None:

              #   Find Winner and Loser's Scores

