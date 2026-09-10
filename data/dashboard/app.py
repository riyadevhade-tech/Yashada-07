import sys
import os
import tempfile

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="AI Sports Performance Analyzer",
    page_icon="🏆",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "sports_performance.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "performance_model.pkl")

df = pd.read_csv(DATA_PATH)

# Performance Score
df["Performance_Score"] = (
    df["Points"] * 0.25
    + df["Accuracy"] * 0.20
    + df["Speed"] * 0.15
    + df["Stamina"] * 0.15
    + (df["Wins"] / df["Matches"] * 100) * 0.15
    + (df["Training_Hours"] / 20 * 100).clip(upper=100) * 0.10
).round(2)


def performance_level(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 55:
        return "Average"
    return "Needs Improvement"


df["Performance_Level"] = df["Performance_Score"].apply(
    performance_level
)

# -------------------------------------------------
# AI RECOMMENDATIONS
# -------------------------------------------------

def get_recommendations(row):

    recommendations = []

    if row["Accuracy"] < 80:
        recommendations.append("Improve accuracy through regular skill practice.")
    else:
        recommendations.append("Accuracy is good. Maintain consistent practice.")

    if row["Speed"] < 80:
        recommendations.append("Focus on speed and agility training.")
    else:
        recommendations.append("Speed is strong. Continue agility exercises.")

    if row["Stamina"] < 80:
        recommendations.append("Increase endurance and stamina training.")
    else:
        recommendations.append("Stamina is good. Maintain endurance training.")

    if row["Training_Hours"] < 14:
        recommendations.append("Increase training consistency.")
    else:
        recommendations.append("Training routine is consistent.")

    win_rate = (row["Wins"] / row["Matches"]) * 100

    if win_rate < 60:
        recommendations.append("Focus on match strategy and decision making.")
    else:
        recommendations.append("Match performance is strong.")

    return recommendations


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("🏆 AI Sports Analyzer")

st.sidebar.markdown("### Dashboard Controls")

sport_options = ["All"] + sorted(df["Sport"].unique().tolist())

selected_sport = st.sidebar.selectbox(
    "Select Sport",
    sport_options
)

if selected_sport != "All":
    filtered_df = df[df["Sport"] == selected_sport].copy()
else:
    filtered_df = df.copy()

player_options = ["All"] + sorted(
    filtered_df["Player_Name"].unique().tolist()
)

selected_player = st.sidebar.selectbox(
    "Select Player",
    player_options
)

if selected_player != "All":
    filtered_df = filtered_df[
        filtered_df["Player_Name"] == selected_player
    ].copy()

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🏆 AI Sports Performance Analyzer")

st.markdown(
    "### Intelligent Player Performance & AI Analytics Dashboard"
)

st.divider()

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "👥 Players",
    len(filtered_df)
)

col2.metric(
    "📊 Avg Score",
    f"{filtered_df['Performance_Score'].mean():.2f}"
)

col3.metric(
    "⚡ Avg Speed",
    f"{filtered_df['Speed'].mean():.1f}"
)

col4.metric(
    "🎯 Avg Accuracy",
    f"{filtered_df['Accuracy'].mean():.1f}%"
)

col5.metric(
    "🏆 Total Wins",
    int(filtered_df["Wins"].sum())
)

st.divider()

# -------------------------------------------------
# TOP PLAYER
# -------------------------------------------------

if not filtered_df.empty:

    top_player = filtered_df.loc[
        filtered_df["Performance_Score"].idxmax()
    ]

    st.success(
        f"🏆 Top Performing Player: **{top_player['Player_Name']}** "
        f"| Score: **{top_player['Performance_Score']}** "
        f"| Sport: **{top_player['Sport']}**"
    )

# -------------------------------------------------
# PERFORMANCE TABLE
# -------------------------------------------------

st.subheader("📋 Player Performance")

display_columns = [
    "Player_Name",
    "Sport",
    "Matches",
    "Points",
    "Assists",
    "Accuracy",
    "Speed",
    "Stamina",
    "Training_Hours",
    "Wins",
    "Performance_Score",
    "Performance_Level"
]

st.dataframe(
    filtered_df[display_columns],
    width="stretch",
    hide_index=True
)

# -------------------------------------------------
# CHART 1 — PERFORMANCE SCORE
# -------------------------------------------------

st.subheader("📊 Player Performance Score")

fig_score = px.bar(
    filtered_df.sort_values(
        "Performance_Score",
        ascending=False
    ),
    x="Player_Name",
    y="Performance_Score",
    color="Sport",
    text="Performance_Score",
    title="Overall Performance Score"
)

fig_score.update_layout(
    yaxis_title="Performance Score",
    xaxis_title="Player"
)

st.plotly_chart(
    fig_score,
    width="stretch"
)

# -------------------------------------------------
# CHART 2 — SKILL ANALYSIS
# -------------------------------------------------

st.subheader("⚡ Player Skill Analysis")

skill_columns = [
    "Accuracy",
    "Speed",
    "Stamina"
]

skill_data = filtered_df[
    ["Player_Name"] + skill_columns
].melt(
    id_vars="Player_Name",
    var_name="Skill",
    value_name="Score"
)

fig_skill = px.bar(
    skill_data,
    x="Player_Name",
    y="Score",
    color="Skill",
    barmode="group",
    title="Accuracy, Speed & Stamina"
)

fig_skill.update_layout(
    yaxis_title="Score",
    xaxis_title="Player"
)

st.plotly_chart(
    fig_skill,
    width="stretch"
)

# -------------------------------------------------
# CHART 3 — TRAINING VS PERFORMANCE
# -------------------------------------------------

st.subheader("🏋️ Training vs Performance")

fig_training = px.scatter(
    filtered_df,
    x="Training_Hours",
    y="Performance_Score",
    size="Wins",
    color="Sport",
    hover_name="Player_Name",
    title="Training Hours vs Performance Score"
)

st.plotly_chart(
    fig_training,
    width="stretch"
)

# -------------------------------------------------
# CHART 4 — WINS
# -------------------------------------------------

st.subheader("🏅 Player Wins")

fig_wins = px.bar(
    filtered_df.sort_values(
        "Wins",
        ascending=False
    ),
    x="Player_Name",
    y="Wins",
    color="Sport",
    title="Wins by Player"
)

st.plotly_chart(
    fig_wins,
    width="stretch"
)

# -------------------------------------------------
# PLAYER AI INSIGHTS
# -------------------------------------------------

st.subheader("🤖 AI Player Insights")

if selected_player != "All" and not filtered_df.empty:

    player = filtered_df.iloc[0]

    st.info(
        f"### 👤 {player['Player_Name']}\n\n"
        f"**Sport:** {player['Sport']}  \n"
        f"**Performance Score:** {player['Performance_Score']}  \n"
        f"**Performance Level:** {player['Performance_Level']}"
    )

    st.markdown("#### 🧠 AI Recommendations")

    for recommendation in get_recommendations(player):
        st.write("•", recommendation)

else:

    st.write(
        "Select a player from the sidebar to view personalized AI recommendations."
    )

    # -----------------------------------------

# -------------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------------

st.subheader("📥 Export Performance Data")

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Performance Report",
    data=csv_data,
    file_name="AI_Sports_Performance_Report.csv",
    mime="text/csv"
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "AI Sports Performance Analyzer | "
    "Python • Pandas • Scikit-learn • Plotly • Streamlit"
)
# -------------------------------------------------
# AI VIDEO ANALYSIS
# -------------------------------------------------

st.divider()

st.subheader("🎥 AI Sports Video Analysis")

st.write(
    "Upload a sports video to perform AI movement analysis."
)

uploaded_video = st.file_uploader(
    "📤 Upload Sports Video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_video is not None:

    st.success(
        f"Video uploaded successfully: {uploaded_video.name}"
    )

    st.video(uploaded_video)

    if st.button("🚀 Analyze Sports Video"):

        with st.spinner("AI is analyzing the video..."):

            try:

                from vision.pose_analysis import process_video
                from vision.movement_analysis import analyze_movement

                output_path, frame_count = process_video(
                    uploaded_video
                )

                if output_path:

                    st.success(
                        "✅ Video analysis completed successfully!"
                    )

                    st.video(output_path)

                    # -------------------------------
                    # MOVEMENT ANALYSIS
                    # -------------------------------

                    movement_result = analyze_movement(
                        output_path
                    )

                    st.divider()

                    st.subheader(
                        "🏆 AI Movement Analysis"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "🎞️ Frames Analyzed",
                            movement_result["frames_analyzed"]
                        )

                    with col2:
                        st.metric(
                            "🎥 Video FPS",
                            movement_result["video_fps"]
                        )

                    with col3:
                        st.metric(
                            "🏃 Avg Movement",
                            movement_result["average_motion"]
                        )

                    with col4:
                        st.metric(
                            "⚡ Max Movement",
                            movement_result["maximum_motion"]
                        )

                    # -------------------------------
                    # SCORE
                    # -------------------------------

                    score = movement_result[
                        "movement_score"
                    ]

                    st.subheader(
                        "🏆 Movement Score"
                    )

                    st.metric(
                        "AI Performance Score",
                        f"{score}/100"
                    )

                    # -------------------------------
                    # PERFORMANCE LEVEL
                    # -------------------------------

                    performance_level = movement_result[
                        "performance_level"
                    ]

                    st.success(
                        f"🏆 Performance Level: "
                        f"{performance_level}"
                    )

                    # -------------------------------
                    # RECOMMENDATION
                    # -------------------------------

                    if score >= 75:

                        recommendation = (
                            "Excellent movement detected. "
                            "Continue regular training "
                            "and maintain consistency."
                        )

                    elif score >= 50:

                        recommendation = (
                            "Good movement performance. "
                            "Continue regular practice "
                            "and improve movement consistency."
                        )

                    elif score >= 30:

                        recommendation = (
                            "Average movement detected. "
                            "Focus on regular movement "
                            "practice and technique."
                        )

                    else:

                        recommendation = (
                            "Low activity detected in "
                            "this video. Consider more "
                            "active movement practice."
                        )

                    st.subheader(
                        "🤖 AI Recommendation"
                    )

                    st.info(
                        recommendation
                    )

                    # -------------------------------
                    # DOWNLOAD VIDEO
                    # -------------------------------

                    with open(
                        output_path,
                        "rb"
                    ) as video_file:

                        st.download_button(
                            label="⬇️ Download Analyzed Video",
                            data=video_file,
                            file_name=(
                                "AI_Analyzed_Sports_Video.mp4"
                            ),
                            mime="video/mp4"
                        )

                else:

                    st.error(
                        "Unable to process the video."
                    )

            except Exception as e:

                st.error(
                    f"Video analysis error: {e}"
                )