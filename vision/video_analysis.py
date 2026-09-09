import cv2


def convert_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError("Cannot open input video")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 24

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        writer.write(frame)

    cap.release()
    writer.release()

    return output_path


if __name__ == "__main__":

    input_video = "data/demo_sports_video.mp4"
    output_video = "data/sports_video_final.mp4"

    convert_video(input_video, output_video)

    print("Video conversion completed!")
    print("Output:", output_video)