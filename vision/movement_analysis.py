import cv2
import numpy as np


def analyze_movement(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open video")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 25

    motion_values = []
    previous_gray = None
    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            (320, 240)
        )

        if previous_gray is not None:

            difference = cv2.absdiff(
                previous_gray,
                gray
            )

            motion_score = np.mean(difference)

            motion_values.append(
                float(motion_score)
            )

        previous_gray = gray

    cap.release()

    if motion_values:
        average_motion = float(np.mean(motion_values))
        max_motion = float(np.max(motion_values))
    else:
        average_motion = 0
        max_motion = 0

    # AI Movement Performance Score
    performance_score = min(
        100,
        round(
            40 + (average_motion * 25),
            2
        )
    )

    if performance_score >= 75:
        level = "Excellent"
    elif performance_score >= 50:
        level = "Good"
    elif performance_score >= 30:
        level = "Average"
    else:
        level = "Low Activity"

    return {
        "frames_analyzed": frame_count,
        "video_fps": round(fps, 2),
        "average_motion": round(average_motion, 2),
        "maximum_motion": round(max_motion, 2),
        "movement_score": performance_score,
        "performance_level": level
    }


if __name__ == "__main__":

    video = "data/sports_video_h264.mp4"

    result = analyze_movement(video)

    print()
    print("=" * 45)
    print("       AI MOVEMENT ANALYSIS")
    print("=" * 45)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("=" * 45)