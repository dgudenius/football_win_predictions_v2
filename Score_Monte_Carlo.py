# Calculate Points using NFL Score Distributions
import pandas as pd
import numpy as np
import random


Win_Score_Dist_data = pd.read_csv(
    'C:\Users\Daniel\PycharmProjects\NFL_Predictions_v2/Win_score_dist - Win_score_dist.csv')
Lose_Score_Dist_data = pd.read_csv(
    'C:\Users\Daniel\PycharmProjects\NFL_Predictions_v2/Lose_score_dist - Lose_score_dist.csv')
Win_Score_Dist_data.drop_duplicates()
Lose_Score_Dist_data.drop_duplicates()
#print(Win_Score_Dist_data)

Spread_For_Win_Percent = pd.read_csv('C:\Users\Daniel\PycharmProjects\NFL_Predictions_v2/Win Percentage to Spread - Sheet1.csv')
Spread_For_Win_Percent.astype(float)
print(Spread_For_Win_Percent)

Point_Diff_Table = []
win_percent = 0.0
while win_percent <= 100.0 :
    i = 0
    Point_Diff_Table = []
    while i < 10000:
        Win_Chance = random.random()
        if Win_Chance < win_percent/100 :
            Win_Score_Chance = random.random()
            Lose_Score_Chance = random.random()
            Win_Score_Row = Win_Score_Dist_data.loc[(np.searchsorted(Win_Score_Dist_data['Chance'], Win_Score_Chance))]
            Home_Score = (Win_Score_Row.iloc[0]['Score'])
            Lose_Score_Row = Lose_Score_Dist_data.loc[(np.searchsorted(Lose_Score_Dist_data['Chance'], Lose_Score_Chance))]
            Away_Score = (Lose_Score_Row.iloc[0]['Score'])
            Spread = Home_Score-Away_Score
            if Spread < 0:
                Spread = -Spread
            Point_Diff_Table.append(Spread)
            i += 1
        else:
            Win_Score_Chance = random.random()
            Lose_Score_Chance = random.random()
            Win_Score_Row = Win_Score_Dist_data.loc[(np.searchsorted(Win_Score_Dist_data['Chance'], Win_Score_Chance))]
            Away_Score = (Win_Score_Row.iloc[0]['Score'])
            Lose_Score_Row = Lose_Score_Dist_data.loc[
                (np.searchsorted(Lose_Score_Dist_data['Chance'], Lose_Score_Chance))]
            Home_Score = (Lose_Score_Row.iloc[0]['Score'])
            Spread = Home_Score - Away_Score
            if Spread > 0:
                Spread = -Spread
            Point_Diff_Table.append(Spread)
            i += 1
    Point_Diff_Mean = np.mean(Point_Diff_Table)
    print(win_percent)
    print(Point_Diff_Mean)
    win_percent += 1