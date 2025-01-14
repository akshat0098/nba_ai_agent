import pandas as pd
import json


def fetch_team_data_from_json(json_file, team_name, max_games=5):
    # Load data from the saved JSON file
    with open(json_file, 'r') as file:
        games = json.load(file)

    # Convert JSON to DataFrame
    games_df = pd.DataFrame(games)

    # Filter for the specific team
    team_games = games_df[games_df["TEAM_NAME"] == team_name]

    # Sort games by date and take only the most recent ones
    team_games = team_games.sort_values("GAME_DATE", ascending=False).head(max_games)

    return team_games


def get_head_to_head_history(json_file, team1, team2, max_games=5):
    # Load data from the saved JSON file
    with open(json_file, 'r') as file:
        games = json.load(file)

    # Convert JSON to DataFrame
    games_df = pd.DataFrame(games)

    # Filter for games between the two teams
    head_to_head = games_df[
        ((games_df["TEAM_NAME"] == team1) & (games_df["MATCHUP"].str.contains(team2))) |
        ((games_df["TEAM_NAME"] == team2) & (games_df["MATCHUP"].str.contains(team1)))
    ]

    # Sort by date and limit the number of games
    head_to_head = head_to_head.sort_values("GAME_DATE", ascending=False).head(max_games)

    return head_to_head


def get_winning_streak(games):
    if games.empty:
        return "No recent games to analyze."

    streak = 0
    for _, row in games.iterrows():
        if row["WL"] == "W":
            streak += 1
        else:
            break

    return f"Currently on a {streak}-game winning streak." if streak > 0 else "Not on a winning streak."


def get_injured_players(team_name):
    # Placeholder for actual injury report API integration
    injuries = {
        "Los Angeles Lakers": ["LeBron James (ankle)", "Anthony Davis (rest)"],
        "Golden State Warriors": ["Stephen Curry (knee)", "Draymond Green (back)"],
    }
    return injuries.get(team_name, [])


def format_context_for_llm(team_name, games, head_to_head, streak, injuries):
    # Summarize team performance
    if games.empty:
        return f"No recent data available for {team_name}."

    team_summary = f"Team {team_name} has played {len(games)} recent games."
    performance_summary = "\n".join(
        [f"Game {idx+1}: {row['MATCHUP']} | Points: {row['PTS']} | FG%: {row['FG_PCT']} | Rebounds: {row['REB']} | Assists: {row['AST']} | Turnovers: {row['TOV']}"
         for idx, row in games.iterrows()]
    )

    head_to_head_summary = "\n".join(
        [f"Game {idx+1}: {row['MATCHUP']} | Date: {row['GAME_DATE']} | Points: {row['PTS']}"
         for idx, row in head_to_head.iterrows()]
    )

    injury_summary = ", ".join(injuries) if injuries else "No reported injuries."

    return (
        f"{team_summary}\n\n"
        f"Recent Performance:\n{performance_summary}\n\n"
        f"Head-to-Head History:\n{head_to_head_summary}\n\n"
        f"Winning Streak: {streak}\n\n"
        f"Injured Players: {injury_summary}"
    )


def fetch_football_data_from_json(json_file, team_name, max_games=5):
    import json
    import pandas as pd

    # Load JSON file
    with open(json_file, 'r') as file:
        games = json.load(file)
    games_df = pd.DataFrame(games)

    # Filter games where the team was either home or away
    team_games = games_df[
        (games_df["home_team"] == team_name) | (games_df["away_team"] == team_name)
    ]

    # Sort by date and take the most recent games
    team_games = team_games.sort_values("gameday", ascending=False).head(max_games)
    return team_games
def get_head_to_head_football(json_file, team1, team2, max_games=5):
    import json
    import pandas as pd

    # Load JSON file
    with open(json_file, 'r') as file:
        games = json.load(file)
    games_df = pd.DataFrame(games)

    # Filter games between the two teams
    head_to_head = games_df[
        ((games_df["home_team"] == team1) & (games_df["away_team"] == team2)) |
        ((games_df["home_team"] == team2) & (games_df["away_team"] == team1))
    ]

    # Sort by date and limit to the last max_games
    head_to_head = head_to_head.sort_values("gameday", ascending=False).head(max_games)
    return head_to_head
def format_football_context_for_llm(team_name, games):
    if games.empty:
        return f"No recent data available for {team_name}."

    team_summary = f"Recent games for {team_name}:\n"
    performance_summary = "\n".join([
        f"Game {idx + 1}: {row['away_team']} vs {row['home_team']} | "
        f"Score: {row['away_score']}-{row['home_score']} | Date: {row['gameday']}"
        for idx, row in games.iterrows()
    ])
    return team_summary + performance_summary


