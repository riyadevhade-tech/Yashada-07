import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Sport Performance Analyzer",
    page_icon="🏆",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    text-align: center;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("data/sports_data.csv")
except:
    # Demo dataset
    data = {
        "Player": [
            "Aditya", "Rahul", "Rohit", "Amit", "Sahil",
            "Vijay", "Karan", "Akash", "Om", "Yash"
        ],
        "Sport": [
            "Cricket", "Football", "Cricket", "Football", "Basketball",
            "Cricket", "Football", "Basketball", "Cricket", "Football"
        ],
        "Performance": [98, 87, 81, 72, 89, 88, 97, 76, 83, 91],
        "Fitness": [95, 84, 79, 70, 88, 90, 92, 75, 82, 89],
        "Speed": [92, 86, 80, 74, 87, 91, 95, 78, 84, 90],
        "Accuracy": [96, 82, 78, 69, 91, 89, 94, 73, 85, 88]
    }

    df = pd.DataFrame(data)


# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Player Filters")

sport_options = ["All"] + sorted(df["Sport"].unique().tolist())

selected_sport = st.sidebar.selectbox(
    "Select Sport",
    sport_options
)

if selected_sport != "All":
    filtered_df = df[df["Sport"] == selected_sport]
else:
    filtered_df = df.copy()


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🏆 AI Sport Performance Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Player Performance, Fitness & AI Prediction System</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- KPI CALCULATIONS ----------------
total_players = len(filtered_df)

avg_performance = round(
    filtered_df["Performance"].mean(), 2
)

avg_fitness = round(
    filtered_df["Fitness"].mean(), 2
)

top_player = filtered_df.loc[
    filtered_df["Performance"].idxmax(),
    "Player"
]


# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Players",
        total_players
    )

with col2:
    st.metric(
        "📊 Avg Performance",
        avg_performance
    )

with col3:
    st.metric(
        "💪 Avg Fitness",
        avg_fitness
    )

with col4:
    st.metric(
        "🏆 Top Player",
        top_player
    )


st.divider()


# ---------------- PLAYER PERFORMANCE ----------------
st.markdown(
    '<div class="section-title">📈 Player Performance</div>',
    unsafe_allow_html=True
)

fig1 = px.bar(
    filtered_df,
    x="Player",
    y="Performance",
    text="Performance",
    title="Player Performance Score",
    labels={
        "Performance": "Performance Score",
        "Player": "Player"
    }
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    yaxis_range=[0, 110],
    height=450
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ---------------- FITNESS ANALYSIS ----------------
st.markdown(
    '<div class="section-title">💪 Fitness Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    fig2 = px.bar(
        filtered_df,
        x="Player",
        y="Fitness",
        text="Fitness",
        title="Player Fitness Score"
    )

    fig2.update_traces(
        textposition="outside"
    )

    fig2.update_layout(
        yaxis_range=[0, 110],
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


with col2:

    fig3 = px.scatter(
        filtered_df,
        x="Fitness",
        y="Performance",
        size="Speed",
        color="Sport",
        hover_name="Player",
        title="Fitness vs Performance"
    )

    fig3.update_layout(
        height=400
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# ---------------- PLAYER COMPARISON ----------------
st.markdown(
    '<div class="section-title">⚡ Player Skill Analysis</div>',
    unsafe_allow_html=True
)

skill_df = filtered_df[
    ["Player", "Speed", "Accuracy"]
].melt(
    id_vars="Player",
    var_name="Skill",
    value_name="Score"
)

fig4 = px.bar(
    skill_df,
    x="Player",
    y="Score",
    color="Skill",
    barmode="group",
    title="Speed & Accuracy Comparison"
)

fig4.update_layout(
    yaxis_range=[0, 110],
    height=450
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# ---------------- AI PREDICTION ----------------
st.markdown(
    '<div class="section-title">🤖 AI Performance Prediction</div>',
    unsafe_allow_html=True
)

prediction_df = filtered_df.copy()

prediction_df["Predicted_Score"] = (
    prediction_df["Performance"] * 0.5
    + prediction_df["Fitness"] * 0.3
    + prediction_df["Speed"] * 0.1
    + prediction_df["Accuracy"] * 0.1
).round(2)

prediction_df["Prediction"] = prediction_df[
    "Predicted_Score"
].apply(
    lambda x:
        "Excellent" if x >= 90
        else "Good" if x >= 80
        else "Needs Improvement"
)

st.dataframe(
    prediction_df[
        [
            "Player",
            "Sport",
            "Performance",
            "Fitness",
            "Speed",
            "Accuracy",
            "Predicted_Score",
            "Prediction"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# ---------------- TOP PLAYER INSIGHT ----------------
st.markdown(
    '<div class="section-title">🏅 Performance Insight</div>',
    unsafe_allow_html=True
)

best = filtered_df.loc[
    filtered_df["Performance"].idxmax()
]

st.success(
    f"🏆 **{best['Player']}** is the top-performing player "
    f"with a performance score of **{best['Performance']}** "
    f"and fitness score of **{best['Fitness']}**."
)


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<center>🏆 AI Sport Performance Analyzer | "
    "Python • Pandas • Plotly • Streamlit</center>",
    unsafe_allow_html=True
)