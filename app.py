import streamlit as st
from PIL import Image

# Importing necessary modules
from data_processing import (
    fetch_team_data_from_json,
    get_head_to_head_history,
    get_winning_streak,
    get_injured_players,
    format_context_for_llm,
    fetch_football_data_from_json,
    get_head_to_head_football,
    format_football_context_for_llm,
)
from llm_integration import predict_match_with_rag
import os

# # Load environment variables
from dotenv import load_dotenv
load_dotenv()

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App Title and Description
st.title("Sports Match Predictor")
st.markdown(
    """
Predict outcomes for basketball and football matches using team performance, head-to-head history, winning streaks, and injury reports.
"""
)

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a predictor", ["Basketball", "Football"])

# Basketball Predictor
if app_mode == "Basketball":
    st.header("🏀 Basketball Match Predictor")

    col1, col2 = st.columns(2)
    with col1:
        basketball_team1 = st.text_input("🏠 Home Team (Basketball)", "Los Angeles Lakers")
    with col2:
        basketball_team2 = st.text_input("✈️ Away Team (Basketball)", "Golden State Warriors")

    basketball_json_file = "nba_games.json"

    if st.button("Predict Basketball Match"):
        with st.spinner("Fetching data and analyzing..."):
            # Fetch basketball data
            team1_games = fetch_team_data_from_json(basketball_json_file, basketball_team1)
            team2_games = fetch_team_data_from_json(basketball_json_file, basketball_team2)

            # Fetch head-to-head data
            head_to_head = get_head_to_head_history(basketball_json_file, basketball_team1, basketball_team2)

            # Analyze winning streaks
            team1_streak = get_winning_streak(team1_games)
            team2_streak = get_winning_streak(team2_games)

            # Get injured players
            team1_injuries = get_injured_players(basketball_team1)
            team2_injuries = get_injured_players(basketball_team2)

            # Format context for LLM
            team1_context = format_context_for_llm(basketball_team1, team1_games, head_to_head, team1_streak, team1_injuries)
            team2_context = format_context_for_llm(basketball_team2, team2_games, head_to_head, team2_streak, team2_injuries)

            # Predict using LLM
            basketball_prediction = predict_match_with_rag(
                basketball_team1, basketball_team2, team1_context, team2_context, GROQ_API_KEY
            )

            st.subheader("Basketball Prediction")
            st.markdown(f"🏀 **Predicted Winner:** {basketball_prediction}")
            st.markdown("---")

# Football Predictor
elif app_mode == "Football":
    st.header("🏈 Football Match Predictor")

    col3, col4 = st.columns(2)
    with col3:
        football_team1 = st.text_input("🏠 Home Team (Football)", "Kansas City Chiefs")
    with col4:
        football_team2 = st.text_input("✈️ Away Team (Football)", "Detroit Lions")

    football_json_file = "nfl_schedule.json"

    if st.button("Predict Football Match"):
        with st.spinner("Fetching data and analyzing..."):
            # Fetch football data
            team1_games = fetch_football_data_from_json(football_json_file, football_team1)
            team2_games = fetch_football_data_from_json(football_json_file, football_team2)

            # Fetch head-to-head data
            head_to_head = get_head_to_head_football(football_json_file, football_team1, football_team2)

            # Format context for LLM
            team1_context = format_football_context_for_llm(football_team1, team1_games)
            team2_context = format_football_context_for_llm(football_team2, team2_games)

            # Predict using LLM
            football_prediction = predict_match_with_rag(
                football_team1, football_team2, team1_context, team2_context, GROQ_API_KEY
            )

            st.subheader("Football Prediction")
            st.markdown(f"🏈 **Predicted Winner:** {football_prediction}")
            st.markdown("---")

# Footer Section
st.sidebar.markdown("---")
st.sidebar.markdown("🔗 [Learn More](https://example.com)")
st.sidebar.markdown("💡 Developed by [Your Name]")
