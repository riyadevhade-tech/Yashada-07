import cv2
import tempfile
import os
import subprocess
import imageio_ffmpeg


def process_video(video_file):

    # -----------------------------------------
    # HANDLE STREAMLIT UPLOADED FILE OR FILE PATH
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
    # CREATE TEMPORARY OUTPUT
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

        os.remove(temp_output_path)

        return None, 0

    frame_count = 0

    # -----------------------------------------
    # PROCESS VIDEO FRAMES
    # -----------------------------------------

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        processed_frame = cv2.cvtColor(
            gray,
            cv2.COLOR_GRAY2BGR
        )

        cv2.putText(
            processed_frame,
            f"AI Video Analysis | Frame: {frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        writer.write(processed_frame)

    cap.release()
    writer.release()

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
    # CONVERT TO BROWSER COMPATIBLE MP4
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
    # CLEAN TEMPORARY FILES
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

    return final_output_path, frame_count