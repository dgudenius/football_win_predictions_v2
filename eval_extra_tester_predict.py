from util2_predict import *
from Pythag_Win import *
from Combined5_predict import *

# Read historical games from CSV
games = Util2.read_games("data/nfl_games.csv")

# Forecast every game
Combined5.combined5(games)

# Evaluate our forecasts against Elo
Util2.evaluate_forecasts(games)


