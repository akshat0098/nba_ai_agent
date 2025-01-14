from groq import Groq


def predict_match_with_rag(team1, team2, team1_context, team2_context, api_key):
    client = Groq(api_key=api_key)
    prompt = f"""
    Analyze the following basketball team performance data and predict the outcome of a match between {team1} and {team2}.
    
    Context for {team1}:
    {team1_context}
    
    Context for {team2}:
    {team2_context}
    
    Include the following in your response:
    1. Predicted winner.
    2. Predicted score.
    3. Key factors influencing the prediction (based on performance, history, streaks, and injuries).
    4. Confidence level (as a percentage).
    5. Summary of head-to-head history (home/away results).
    6. Current winning streak for both teams.
    7. Injured players for both teams.

    Format your response as:
    - Predicted Winner:
    - Predicted Score:
    - Key Factors:
    - Confidence Level:
    - Head-to-Head History Summary:
    - Winning Streaks:
    - Injuries:
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=750
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in LLM interaction: {str(e)}"
    
    # Existing predict_match_with_rag works for both sports, but you can customize football-specific prompts:
def predict_football_match(team1, team2, team1_context, team2_context, api_key):
    client = Groq(api_key=api_key)
    prompt = f"""
    Analyze the following football team performance data and predict the outcome of a match between {team1} and {team2}.
    
    Context for {team1}:
    {team1_context}
    
    Context for {team2}:
    {team2_context}
    
     Include the following in your response:
    1. Predicted winner.
    2. Predicted score.
    3. Key factors influencing the prediction (based on performance, history, streaks, and injuries).
    4. Confidence level (as a percentage).
    5. Summary of head-to-head history (home/away results).
    6. Current winning streak for both teams.
    7. Injured players for both teams.

    Format your response as:
    - Predicted Winner:
    - Predicted Score:
    - Key Factors:
    - Confidence Level:
    - Head-to-Head History Summary:
    - Winning Streaks:
    - Injuries:
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=750
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in LLM interaction: {str(e)}"

