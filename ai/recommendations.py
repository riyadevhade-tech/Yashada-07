import pandas as pd

def generate_recommendations(row):
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


df = pd.read_csv("data/sports_performance.csv")

print("\n==============================================")
print("        AI SPORTS RECOMMENDATION ENGINE")
print("==============================================")

for _, row in df.iterrows():
    print(f"\nPlayer: {row['Player_Name']}")
    print(f"Sport: {row['Sport']}")
    print("\nAI Recommendations:")

    for i, recommendation in enumerate(generate_recommendations(row), 1):
        print(f"{i}. {recommendation}")

    print("----------------------------------------------")
