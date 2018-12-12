from Info_Gather import *
from Pythag_Win import *
from collections import Counter
import pandas as pd

# Read historical games from CSV

REVERT = 1/2.99
REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}
Win_score = []
Lose_score = []

class Score_Dist:

    @staticmethod
    def score_dist(games):
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
                    if game['result1'] == 0.5:
                        pass
                    elif game['result1'] == 1.0:
                        Win_score.append(game['score1'])
                        Lose_score.append(game['score2'])
                    elif game['result1'] == 1.0:
                        Win_score.append(game['score2'])
                        Lose_score.append(game['score1'])
        Win_score_dist = Counter(Win_score)
        Lose_score_dist = Counter(Lose_score)
        (Win_score_dist)
        (Lose_score_dist)
        Win_Score_Dist_data = pd.read_csv(
            'C:\Users\Daniel\PycharmProjects\NFL_Predictions_v2/Win_score_dist - Win_score_dist.csv')
        Lose_score_dist_data = pd.read_csv(
            'C:\Users\Daniel\PycharmProjects\NFL_Predictions_v2/Lose_score_dist - Lose_score_dist.csv')
        Win_Score_Dist_data.dropna()
        Lose_score_dist_data.dropna()
        print(Win_Score_Dist_data)
        print(Lose_score_dist_data)
