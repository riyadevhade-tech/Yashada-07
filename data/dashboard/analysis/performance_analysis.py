import pandas as pd


def calculate_performance_score(row):
    """
    Calculate AI-based overall sports performance score.
    """

    points_score = min(row["Points"], 100)
    accuracy_score = min(row["Accuracy"], 100)
    speed_score = min(row["Speed"], 100)
    stamina_score = min(row["Stamina"], 100)
    win_score = (row["Wins"] / row["Matches"]) * 100
    training_score = min((row["Training_Hours"] / 20) * 100, 100)

    performance_score = (
        points_score * 0.25
        + accuracy_score * 0.20
        + speed_score * 0.15
        + stamina_score * 0.15
        + win_score * 0.15
        + training_score * 0.10
    )

    return round(performance_score, 2)


def analyze_performance(file_path):

    df = pd.read_csv(file_path)

    required_columns = [
        "Player_Name",
        "Sport",
        "Matches",
        "Points",
        "Assists",
        "Accuracy",
        "Speed",
        "Stamina",
        "Training_Hours",
        "Wins"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    # Calculate performance score
    df["Performance_Score"] = df.apply(
        calculate_performance_score,
        axis=1
    )

    # Performance category
    def performance_category(score):
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 55:
            return "Average"
        else:
            return "Needs Improvement"

    df["Performance_Level"] = df["Performance_Score"].apply(
        performance_category
    )

    return df


if __name__ == "__main__":

    file_path = "data/sports_performance.csv"

    result = analyze_performance(file_path)

    print("\n==============================================")
    print("       AI SPORTS PERFORMANCE ANALYZER")
    print("==============================================")

    print("\nPLAYER PERFORMANCE RESULTS")
    print("----------------------------------------------")

    print(
        result[
            [
                "Player_Name",
                "Sport",
                "Points",
                "Accuracy",
                "Speed",
                "Stamina",
                "Wins",
                "Performance_Score",
                "Performance_Level"
            ]
        ].to_string(index=False)
    )

    print("\n----------------------------------------------")
    print(
        "Average Performance Score:",
        round(result["Performance_Score"].mean(), 2)
    )

    best_player = result.loc[
        result["Performance_Score"].idxmax()
    ]

    print(
        "Top Performing Player:",
        best_player["Player_Name"]
    )

    print(
        "Top Performance Score:",
        best_player["Performance_Score"]
    )

    print("==============================================")