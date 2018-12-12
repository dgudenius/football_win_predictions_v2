from util2_predict import *
from Pythag_Win import *
from Combined6_predict import *
import pandas as pd

# Read historical games from CSV
games = Util2.read_games("data/nfl_games.csv")

# Forecast every game
Combined6.combined6(games)

# Evaluate our forecasts against Elo
Util2.evaluate_forecasts(games)


