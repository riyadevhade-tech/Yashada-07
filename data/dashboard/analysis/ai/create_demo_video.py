import cv2
import numpy as np

output = "data/demo_sports_video.mp4"

width = 640
height = 360
fps = 24
duration = 10

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    output,
    fourcc,
    fps,
    (width, height)
)

total_frames = fps * duration

for i in range(total_frames):

    frame = np.full(
        (height, width, 3),
        240,
        dtype=np.uint8
    )

    # Ground
    cv2.line(
        frame,
        (0, 290),
        (width, 290),
        (80, 150, 80),
        4
    )

    # Moving player
    x = 80 + int(
        480 * i / (total_frames - 1)
    )

    y = 210

    # Head
    cv2.circle(
        frame,
        (x, y - 55),
        18,
        (40, 40, 40),
        3
    )

    # Body
    cv2.line(
        frame,
        (x, y - 35),
        (x, y + 35),
        (40, 40, 40),
        4
    )

    # Arms
    cv2.line(
        frame,
        (x, y - 20),
        (x - 35, y + 10),
        (40, 40, 40),
        4
    )

    cv2.line(
        frame,
        (x, y - 20),
        (x + 35, y + 10),
        (40, 40, 40),
        4
    )

    # Legs
    cv2.line(
        frame,
        (x, y + 35),
        (x - 30, 290),
        (40, 40, 40),
        4
    )

    cv2.line(
        frame,
        (x, y + 35),
        (x + 35, 290),
        (40, 40, 40),
        4
    )

    # Ball
    ball_x = min(x + 60, 610)

    cv2.circle(
        frame,
        (ball_x, 270),
        12,
        (50, 50, 50),
        3
    )

    cv2.putText(
        frame,
        "AI SPORTS PERFORMANCE DEMO",
        (120, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (30, 30, 30),
        2
    )

    writer.write(frame)

writer.release()

print("======================================")
print("Demo Sports Video Created Successfully")
print("======================================")
print("File:", output)
print("Duration: 10 seconds")
print("======================================")