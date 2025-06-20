import cv2
import mediapipe as mp
from ultralytics import YOLO

# Path to input video
input_video = r"C:\Users\hp\OneDrive\Desktop\touch_design_proj\Dante_catto.mp4"  # Change to your video filename
output_video = "catto_pose.mp4"

# Toggle detection modes
USE_MEDIAPIPE = True
USE_YOLO = True

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) if USE_MEDIAPIPE else None

# Load YOLOv8 model
yolo_model = YOLO("yolov8n.pt") if USE_YOLO else None

# Open input video
cap = cv2.VideoCapture(input_video)

# Video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Video writer setup
out = cv2.VideoWriter(
    output_video,
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (frame_width, frame_height)
)

print(f"📹 Processing {frame_count} frames from {input_video}...")

# Frame-by-frame processing
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO
    if yolo_model:
        yolo_results = yolo_model(frame, verbose=False)
        frame = yolo_results[0].plot()

    # Run MediaPipe Pose
    if pose:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2)
            )

    out.write(frame)

# Clean up
cap.release()
out.release()
print(f"✅ Saved processed video to: {output_video}")
