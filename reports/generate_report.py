from datetime import datetime


def generate_report(
    player_name,
    sport,
    performance_score,
    performance_level,
    frames_analyzed,
    movement_score,
    recommendation
):

    report = f"""
==================================================
          AI SPORTS PERFORMANCE REPORT
==================================================

Generated On:
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

--------------------------------------------------
PLAYER DETAILS
--------------------------------------------------

Player Name        : {player_name}
Sport              : {sport}

--------------------------------------------------
PERFORMANCE ANALYSIS
--------------------------------------------------

Performance Score  : {performance_score}/100
Performance Level  : {performance_level}

--------------------------------------------------
VIDEO ANALYSIS
--------------------------------------------------

Frames Analyzed    : {frames_analyzed}
Movement Score     : {movement_score}/100

--------------------------------------------------
AI RECOMMENDATION
--------------------------------------------------

{recommendation}

--------------------------------------------------
CONCLUSION
--------------------------------------------------

The AI system analyzed the available performance
and video movement data and generated an overall
performance assessment.

==================================================
       AI SPORTS PERFORMANCE ANALYZER
==================================================
"""

    filename = "reports/AI_Sports_Performance_Report.txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    return filename


if __name__ == "__main__":

    report_file = generate_report(
        player_name="Demo Player",
        sport="Football",
        performance_score=68.79,
        performance_level="Good",
        frames_analyzed=240,
        movement_score=68.79,
        recommendation=(
            "Good movement performance. "
            "Continue regular practice and "
            "improve movement consistency."
        )
    )

    print("======================================")
    print("AI SPORTS REPORT GENERATED")
    print("======================================")
    print("Report:", report_file)
    print("======================================")