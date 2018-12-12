import csv
import math

past_games = 18     # Past Games to include in Pythagorean Win Projection (must be integer greater than 3)
v_value = 1      # Rate at which previous seasons are discounted (not yet in use)
wf = 1.39      # Exponential for Pythagorean calcs, default for football is 2.37(?) (must be a float)
HFA = 7.4      # home field advantage as percentage, default is 5.5
team_below_min = 32.25 # Expected win percentage by teams that have played 1 game (must be float)
new_team = 27.5       # Expected win percentage by team in first game (must be float)
a_factor = 2.465          # Exponential factor to compare Expected Wins Head to Head (2.465)
expect_points = 45.7   # Expected total points for calculating point differential
y_factor  = 1.9        # Multiplier for points expectations
x_factor  = 1.4        # Root for points expectations, this and the y_factor are used in compressing/expanding scores
backup_qb_loss = 2.3  # Expected point loss if backup QB is starting (not yet in use)
backup_qb_loss_percent = backup_qb_loss/(expect_points/2)


class Pythag_Win:

    @staticmethod
    def pythag_win(games):
        """ Generates win probabilities in the my_prob1 field for each game based on Pythagorean Win Theorem model """

        # Initialize team objects(?)
        teams = {}
        for row in [item for item in csv.DictReader(open("data/initial_elos.csv"))]:
            teams[row['team']] = {
                'name': row['team'],
                'season': 'season',
                'Pwin': float(new_team/100),
                'Pfor': [],
                'Pagainst': [],
                'PforSumInRange' : 0
            }

        for game in games:
            team1, team2 = teams[game['team1']], teams[game['team2']]

            # My difference includes home field advantage
            my_diff = (team1['Pwin']+  HFA/100) - (team2['Pwin'])
            #(0 if game['neutral']) == 1 else

            # This is the most important piece, where we set my_prob1 to our forecasted probability
            if game['elo_prob1'] != None:
            #    game['my_prob1'] = .5+my_diff
                 game['my_prob1'] = (team1['Pwin']+(HFA/100))**a_factor/((team1['Pwin']+(HFA/100))**a_factor+team2['Pwin']**a_factor)
                 game['point_diff'] = ((expect_points * game['my_prob1']) - (expect_points / 2))
                 game['point_diff2'] = (y_factor * (abs(((expect_points * game['my_prob1']) - (expect_points / 2))))) ** (1 / x_factor)

            # If game was played, maintain team Elo ratings
            if game['score1'] != None:

                # Margin of victory is used as a K multiplier
              #   pd = abs(game['score1'] - game['score2'])
              #  mult = math.log(max(pd, 1) + 1.0) * (2.2 / (1.0 if game['result1'] == 0.5 else ((my_diff if game['result1'] == 1.0 else -my_diff) * 0.001 + 2.2)))

                # Elo shift based on K and the margin of victory multiplier
               # Pwin = (K * mult) * (game['result1'] - game['my_prob1'])

                # Add Points to team arrays
                team1['Pfor'].append(game['score1'])
                team1['Pagainst'].append(game['score2'])
                team2['Pfor'].append(game['score2'])
                team2['Pagainst'].append(game['score1'])
              #  print (team1['Pfor'])
                # Sum team all time points
                team1['PforSum']=(sum(team1['Pfor']))
                team1['PagainstSum'] = (sum(team1['Pagainst']))
                team2['PforSum']=(sum(team2['Pfor']))
                team2['PagainstSum'] = (sum(team2['Pagainst']))


                if len(team1['Pfor']) <= past_games and (team1['PforSum'] or team1['PagainstSum']) != 0:
                    team1['Pwin'] = ((team1['PforSum']) ** wf) / (((team1['PforSum']) ** wf) + (team1['PagainstSum']) ** wf)
                elif len(team1['Pfor']) > past_games and (team1['PforSum'] or team1['PagainstSum']) !=0:
                  #  print len(team1['Pfor'])
                    # Sum points for games in past_games range
                    team1['PforSumInRange'] = (sum(team1['Pfor'][len(team1['Pfor']) - past_games:]))
                    team1['PagainstSumInRange'] = (sum(team1['Pagainst'][len(team1['Pagainst']) - past_games:]))
                    team1['Pwin'] = (team1['PforSumInRange']**wf)/(((team1['PforSumInRange'])**wf)+((team1['PagainstSumInRange'])**wf))
                    #team1['Pwin'] = ((sum(team1['Pfor'][len(team1['Pfor'])-past_games:]))** wf)/(((sum(team1['Pfor'][len(team1['Pfor'])-past_games:]))**wf)+((sum(team1['Pagainst'][len(team1['Pagainst'])-past_games:]))**wf))
                    # print len(team1['Pfor'])
                else:
                   team1['Pwin'] = team_below_min/100
                if len(team1['Pfor']) <= past_games and (team2['PforSum'] or team2['PagainstSum']) != 0:
                    team2['Pwin'] = ((team2['PforSum']) ** wf) / (((team2['PforSum']) ** wf) + (team2['PagainstSum']) ** wf)
                elif len(team2['Pfor']) > past_games and (team2['PforSum'] or team2['PagainstSum']) != 0:
                    # Sum points for games in past_games range
                    team2['PforSumInRange'] = (sum(team2['Pfor'][len(team2['Pfor']) - past_games:]))
                    team2['PagainstSumInRange'] = (sum(team2['Pagainst'][len(team2['Pagainst']) - past_games:]))
                    #
                    team2['Pwin'] = ((sum(team2['Pfor'][len(team2['Pfor'])-past_games:]))**wf)/(((sum(team2['Pfor'][len(team2['Pfor'])-past_games:]))**wf)+((sum(team2['Pagainst'][len(team2['Pagainst'])-past_games:]))**wf))
                else:
                    team2['Pwin'] = team_below_min/100

