import pandas as pd
# This function compiles rolling pregame features for games that happened before the current game
# A rolling window of 5 is used to compute the features
def compile_features(games):
    df = games.copy()

    df = df.sort_values(by=["GAME_DATE", "TEAM_ID"])

    print(df.head())

    rolling_cols = {
        "team_win": "win_pct",
        "point_diff": "point_diff",
        "PTS": "pts",
        "REB": "reb",
        "AST": "ast",
        "TOV": "tov",
        "FG_PCT": "fg_pct",
        "FG3_PCT": "fg3_pct",
        "FT_PCT": "ft_pct",
    }

    for source_col, name in rolling_cols.items():
        df[f"{name}_last_5"] = (
            df.groupby("TEAM_ID")[source_col]
            .transform(lambda x: x.shift(1).rolling(window=5, min_periods=3).mean())
        )

        df[f"{name}_last_10"] = (
            df.groupby("TEAM_ID")[source_col]
            .transform(lambda x: x.shift(1).rolling(window=10, min_periods=5).mean())
        )

    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df["prev_game_date"] = df.groupby("TEAM_ID")["GAME_DATE"].shift(1)
    df["rest_days"] = (df["GAME_DATE"] - df["prev_game_date"]).dt.days
    df["rest_days"] = df["rest_days"].clip(lower=0, upper=7)

    return df



file_df = pd.read_csv("data/nba_team_game_logs.csv")
df = compile_features(file_df)
print(df.head())
