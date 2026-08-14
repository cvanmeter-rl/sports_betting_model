import time
import pandas as pd
import numpy as np
from pathlib import Path

from nba_api.stats.endpoints import leaguegamefinder

def fetch_nba_games(seasons, season_type='Regular Season', sleep_time=1.0):
    """
    Gathers team-level NBA game data from nba_api.
    Each game will return two rows: one for each team
    """

    all_games = []

    for season in seasons:
        print(f"Fetching games for season: {season}...")
        gf = leaguegamefinder.LeagueGameFinder(
            season_nullable = season,
            season_type_nullable = season_type,
            league_id_nullable = '00'  # NBA league ID
        )

        dataframe = gf.get_data_frames()[0]
        dataframe["Season"] = season  # Add a column for the season
        all_games.append(dataframe)

        time.sleep(sleep_time)  # Sleep to avoid hitting API rate limits
    
    games = pd.concat(all_games, ignore_index=True)

    games["GAME_DATE"] = pd.to_datetime(games["GAME_DATE"])
    games["is_home"] = games["MATCHUP"].str.contains("vs.").astype(int)
    games["opp_abbr"] = games["MATCHUP"].str[-3:]
    games["team_win"] = (games["WL"] == "W").astype(int)
    games["point_diff"] = games["PLUS_MINUS"]

    return games

if __name__ == "__main__":
    seasons = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]

    games = fetch_nba_games(seasons)

    Path("data").mkdir(exist_ok=True, parents=True)
    games.to_csv("data/nba_team_game_logs.csv", index=False)

    print(games.head())
    print(games.shape)

    