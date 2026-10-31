import numpy as np
from collections import deque


class SpeedEstimator:
    def __init__(self, fps=25, ppm=12.0, frame_skip=1):
        self.fps = fps
        self.ppm = ppm
        self.frame_skip = frame_skip

        self.previous_positions = {}
        self.speeds = {}

        # Store position history for smoother speed calculation
        self.position_history = {}

        # Smoothing factor
        self.alpha = 0.15

        # Minimum movement in pixels to avoid detection jitter
        self.min_pixel_movement = 2.0

    def estimate(self, objects):
        current_speeds = {}
        current_prev_positions = self.previous_positions.copy()

        # Actual time between two processed frames
        time_delta = self.frame_skip / self.fps

        for obj_id, (cx, cy, det) in objects.items():

            x1, y1, x2, y2, label, conf = det

            # ---------------------------------------------------------
            # Initialize history for new vehicle
            # ---------------------------------------------------------
            if obj_id not in self.position_history:
                self.position_history[obj_id] = deque(maxlen=5)

            self.position_history[obj_id].append((cx, cy))

            # ---------------------------------------------------------
            # New vehicle
            # ---------------------------------------------------------
            if obj_id not in self.previous_positions:
                speed = 0.0

            else:
                px_x, px_y = self.previous_positions[obj_id]

                # Calculate pixel movement
                dx = cx - px_x
                dy = cy - px_y

                pixel_dist = np.sqrt(dx ** 2 + dy ** 2)

                # -----------------------------------------------------
                # Ignore small detector/tracker jitter
                # -----------------------------------------------------
                if pixel_dist < self.min_pixel_movement:
                    speed = 0.0

                else:
                    # -------------------------------------------------
                    # Convert pixels to meters
                    # -------------------------------------------------
                    meters_dist = pixel_dist / self.ppm

                    # -------------------------------------------------
                    # Convert to meters/second
                    # -------------------------------------------------
                    meters_per_second = meters_dist / time_delta

                    # -------------------------------------------------
                    # Convert m/s to km/h
                    # -------------------------------------------------
                    raw_speed = meters_per_second * 3.6

                    # -------------------------------------------------
                    # Smooth speed
                    # -------------------------------------------------
                    if obj_id in self.speeds:
                        previous_speed = self.speeds[obj_id]

                        speed = (
                            self.alpha * raw_speed
                            + (1 - self.alpha) * previous_speed
                        )
                    else:
                        speed = raw_speed

            # ---------------------------------------------------------
            # Limit unrealistic instantaneous values
            # ---------------------------------------------------------
            if speed > 120:
                speed = 120

            # ---------------------------------------------------------
            # Store current position and speed
            # ---------------------------------------------------------
            self.previous_positions[obj_id] = (cx, cy)
            self.speeds[obj_id] = speed

            current_speeds[obj_id] = int(round(speed))

        # -------------------------------------------------------------
        # Remove vehicles that are no longer being tracked
        # -------------------------------------------------------------
        active_ids = set(objects.keys())

        self.previous_positions = {
            k: v
            for k, v in self.previous_positions.items()
            if k in active_ids
        }

        self.speeds = {
            k: v
            for k, v in self.speeds.items()
            if k in active_ids
        }

        self.position_history = {
            k: v
            for k, v in self.position_history.items()
            if k in active_ids
        }

        return current_speeds, current_prev_positions