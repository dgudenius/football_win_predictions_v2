from util import *
from Score_Dist import *
from Pythag_Win import *

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

# Forecast every game
Score_Dist.score_dist(games)



