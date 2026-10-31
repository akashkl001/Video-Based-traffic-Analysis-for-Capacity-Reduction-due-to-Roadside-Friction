import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import cv2
import os
import matplotlib.pyplot as plt

from src.detector import Detector
from src.speed import SpeedEstimator
from src.counter import Counter
from src.friction import FrictionDetector
from src.utils import draw

print("Starting processing...")

raw_input = input("Enter camera position (front/back or f/b): ").strip().lower()

if raw_input in ["front", "f"]:
    cam_pos = "front"
elif raw_input in ["back", "b"]:
    cam_pos = "back"
else:
    print("Invalid input. Defaulting to 'back'.")
    cam_pos = "back"

FRAME_SKIP = 2 
VIDEO_SOURCE = "Dataset/wrong_direction.mp4"
MODEL_PATH = "yolov8n.pt"

# FRAME_SKIP = 2 #b7,f8,f9,b10,f1,b1,b2
# VIDEO_SOURCE = "Dataset/f8.mp4"
# MODEL_PATH = "best.pt"

detector = Detector(model_path=MODEL_PATH)
counter = Counter()
friction_detector = FrictionDetector(
    camera_position=cam_pos,
    stationary_frames_threshold=40
)

cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    print(f"Error: Could not open {VIDEO_SOURCE}")
    exit()

# --- FIX 1: Read actual frame dimensions from image array to handle phone rotation ---
ret, first_frame = cap.read()
if not ret:
    print("Error: Could not read first frame from video.")
    exit()

height, width = first_frame.shape[:2]
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps != fps:
    fps = 25

speed_estimator = SpeedEstimator(
    fps=fps,
    frame_skip=FRAME_SKIP,
    ppm=12.0
)

if not os.path.exists("output"):
    os.makedirs("output")

output_fps = fps // FRAME_SKIP if FRAME_SKIP > 0 else fps

out = cv2.VideoWriter(
    "output/output.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    output_fps,
    (width, height)
)

# --- Display Live Window at Original Video Resolution ---
cv2.namedWindow("Live", cv2.WINDOW_AUTOSIZE)

frame_id = 0

# --- Tracking Arrays for Live Count Visualization ---
counts_history = []
frame_ids = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    if frame_id % FRAME_SKIP != 0:
        continue

    objects = detector.detect(frame)
    speeds, previous_positions = speed_estimator.estimate(objects)
    friction_events = friction_detector.detect(objects, speeds)
    total_count = counter.count(objects)

    # Log values for the density graph
    counts_history.append(total_count)
    frame_ids.append(frame_id)

    frame = draw(
        frame,
        objects,
        speeds,
        total_count,
        friction_events
    )

    # Save full-resolution frame to output file
    out.write(frame)

    # Display frame at original input video resolution
    cv2.imshow("Live", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# --- Export Live Count Analytics Graph ---
if frame_ids:
    plt.figure(figsize=(10, 4))
    plt.plot(
        frame_ids,
        counts_history,
        color='#007acc',
        linewidth=1.8
    )
    plt.axhline(
        y=8,
        color='r',
        linestyle='--',
        label='Heavy Density Cutoff'
    )
    plt.axhline(
        y=4,
        color='y',
        linestyle='--',
        label='Moderate Density Cutoff'
    )
    plt.title('Real-Time Vehicle Density Profile')
    plt.xlabel('Frame Number')
    plt.ylabel('Active Vehicles (Live Count)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(
        'output/traffic_density_graph.png',
        dpi=300
    )
    plt.close()
    print("Saved traffic density graph to output/traffic_density_graph.png")

print("Processing complete. Saved to output/output.mp4")