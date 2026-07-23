import time
import pandas as pd
import numpy as np

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

    