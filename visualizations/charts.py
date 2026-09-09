import pandas as pd
import matplotlib.pyplot as plt

# Load analyzed data
df = pd.read_csv("data/analyzed_sports_performance.csv")

# 1. Player Performance Score
plt.figure(figsize=(10, 6))
plt.bar(df["Player_Name"], df["Performance_Score"])
plt.title("Player Performance Score")
plt.xlabel("Players")
plt.ylabel("Performance Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/player_performance.png")
plt.show()

# 2. Fitness Analysis
plt.figure(figsize=(10, 6))
plt.plot(df["Player_Name"], df["Speed"], marker="o", label="Speed")
plt.plot(df["Player_Name"], df["Stamina"], marker="o", label="Stamina")
plt.title("Player Fitness Analysis")
plt.xlabel("Players")
plt.ylabel("Fitness Score")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("visualizations/fitness_analysis.png")
plt.show()

# 3. Top 5 Players
top5 = df.nlargest(5, "Performance_Score")

plt.figure(figsize=(8, 5))
plt.bar(top5["Player_Name"], top5["Performance_Score"])
plt.title("Top 5 Performing Players")
plt.xlabel("Players")
plt.ylabel("Performance Score")
plt.tight_layout()
plt.savefig("visualizations/top_5_players.png")
plt.show()

print("===================================")
print("     SPORTS ANALYSIS CHARTS")
print("===================================")
print("Performance chart created successfully.")
print("Fitness chart created successfully.")
print("Top 5 players chart created successfully.")
print("Charts saved in visualizations folder.")