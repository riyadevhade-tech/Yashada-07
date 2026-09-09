from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime


def generate_pdf_report(
    player_name,
    sport,
    performance_score,
    performance_level,
    frames_analyzed,
    video_fps,
    movement_score,
    recommendation
):

    filename = "reports/AI_Sports_Performance_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    story = []

    story.append(
        Paragraph(
            "AI SPORTS PERFORMANCE REPORT",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Generated On: "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "PLAYER DETAILS",
            heading_style
        )
    )

    player_data = [
        ["Player Name", player_name],
        ["Sport", sport],
        ["Performance Score", f"{performance_score}/100"],
        ["Performance Level", performance_level]
    ]

    table = Table(
        player_data,
        colWidths=[180, 280]
    )

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "VIDEO ANALYSIS",
            heading_style
        )
    )

    video_data = [
        ["Frames Analyzed", str(frames_analyzed)],
        ["Video FPS", str(video_fps)],
        ["Movement Score", f"{movement_score}/100"]
    ]

    video_table = Table(
        video_data,
        colWidths=[180, 280]
    )

    video_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    story.append(video_table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "AI RECOMMENDATION",
            heading_style
        )
    )

    story.append(
        Paragraph(
            recommendation,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "CONCLUSION",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "The AI Sports Performance Analyzer "
            "analyzed the available player and video "
            "movement data and generated a performance "
            "assessment.",
            styles["Normal"]
        )
    )

    doc.build(story)

    return filename