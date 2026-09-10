import cv2
import tempfile
import os
import subprocess
import imageio_ffmpeg
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# -------------------------------------------------
# MEDIAPIPE POSE LANDMARKER
# -------------------------------------------------

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "models",
        "pose_landmarker_lite.task"
    )
)


def create_pose_detector():

    base_options = python.BaseOptions(
        model_asset_path=MODEL_PATH
    )

    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )

    return vision.PoseLandmarker.create_from_options(options)


# -------------------------------------------------
# PROCESS VIDEO
# -------------------------------------------------

def process_video(video_file):

    # -----------------------------------------
    # HANDLE STREAMLIT FILE OR FILE PATH
    # -----------------------------------------

    if isinstance(video_file, (str, os.PathLike)):

        input_path = str(video_file)

    else:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        ) as temp_video:

            temp_video.write(video_file.getvalue())
            input_path = temp_video.name

    # -----------------------------------------
    # OPEN VIDEO
    # -----------------------------------------

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():

        if os.path.exists(input_path):
            os.remove(input_path)

        return None, 0

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width <= 0 or height <= 0:

        cap.release()

        if os.path.exists(input_path):
            os.remove(input_path)

        return None, 0

    # -----------------------------------------
    # TEMPORARY OUTPUT
    # -----------------------------------------

    temp_output = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_output_path = temp_output.name
    temp_output.close()

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        temp_output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():

        cap.release()

        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        return None, 0

    # -----------------------------------------
    # INITIALIZE MEDIAPIPE TASKS
    # -----------------------------------------

    if not os.path.exists(MODEL_PATH):

        cap.release()
        writer.release()

        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        raise FileNotFoundError(
            f"Pose model not found: {MODEL_PATH}"
        )

    detector = create_pose_detector()

    frame_count = 0
    detected_frames = 0

    # -----------------------------------------
    # PROCESS VIDEO
    # -----------------------------------------

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp in milliseconds
        timestamp_ms = int(
            (frame_count / fps) * 1000
        )

        # Pose detection
        results = detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # -------------------------------------
        # DRAW POSE
        # -------------------------------------

        if results.pose_landmarks:

            detected_frames += 1

            for pose_landmarks in results.pose_landmarks:

                # Draw landmark points
                for landmark in pose_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    if 0 <= x < width and 0 <= y < height:

                        cv2.circle(
                            frame,
                            (x, y),
                            4,
                            (0, 255, 0),
                            -1
                        )

                # Draw connections
                connections = [
                    (11, 12),
                    (11, 13),
                    (13, 15),
                    (12, 14),
                    (14, 16),
                    (11, 23),
                    (12, 24),
                    (23, 24),
                    (23, 25),
                    (25, 27),
                    (24, 26),
                    (26, 28)
                ]

                for start, end in connections:

                    if (
                        start < len(pose_landmarks)
                        and end < len(pose_landmarks)
                    ):

                        p1 = pose_landmarks[start]
                        p2 = pose_landmarks[end]

                        x1 = int(p1.x * width)
                        y1 = int(p1.y * height)

                        x2 = int(p2.x * width)
                        y2 = int(p2.y * height)

                        cv2.line(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

            cv2.putText(
                frame,
                "POSE DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                "POSE NOT DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # Frame information
        cv2.putText(
            frame,
            f"Frame: {frame_count}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        writer.write(frame)

    # -----------------------------------------
    # RELEASE
    # -----------------------------------------

    cap.release()
    writer.release()
    detector.close()

    # -----------------------------------------
    # CHECK FRAMES
    # -----------------------------------------

    if frame_count == 0:

        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        return None, 0

    # -----------------------------------------
    # FFMPEG H.264 CONVERSION
    # -----------------------------------------

    final_output = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    final_output_path = final_output.name
    final_output.close()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-y",
        "-i",
        temp_output_path,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        final_output_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # -----------------------------------------
    # CLEAN TEMP FILES
    # -----------------------------------------

    if os.path.exists(input_path):
        os.remove(input_path)

    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

    # -----------------------------------------
    # CHECK FFMPEG
    # -----------------------------------------

    if result.returncode != 0:

        if os.path.exists(final_output_path):
            os.remove(final_output_path)

        error_message = result.stderr.decode(
            errors="ignore"
        )

        raise RuntimeError(
            f"Video conversion failed:\n{error_message[-1000:]}"
        )

    print(
        f"Pose detection completed: "
        f"{detected_frames}/{frame_count} frames"
    )

    return final_output_path, frame_count