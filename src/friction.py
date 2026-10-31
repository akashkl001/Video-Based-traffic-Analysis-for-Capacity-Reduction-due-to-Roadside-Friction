import numpy as np
from collections import deque

class FrictionDetector:
    def __init__(self, camera_position="back", parked_speed_threshold=4.0, stationary_frames_threshold=30):
        self.camera_position = camera_position.strip().lower()
        self.parked_threshold = parked_speed_threshold
        self.stationary_threshold = stationary_frames_threshold
        
        
        self.stationary_frames = {}
        
        self.history = {} 

    def detect(self, objects, speeds):
        friction_events = {} 

        for obj_id, (cx, cy, det) in objects.items():
            speed = speeds.get(obj_id, 0)
            
            
            if obj_id not in self.history:
                self.history[obj_id] = deque(maxlen=15)
            self.history[obj_id].append((cx, cy))

            
            if speed < self.parked_threshold:
                self.stationary_frames[obj_id] = self.stationary_frames.get(obj_id, 0) + 1
            else:
                self.stationary_frames[obj_id] = 0

            
            if self.stationary_frames.get(obj_id, 0) > self.stationary_threshold:
                friction_events[obj_id] = "Occlusion"
                continue 

            
            history_len = len(self.history[obj_id])
            
            if history_len >= 10 and speed > self.parked_threshold:
                old_cx, old_cy = self.history[obj_id][0]
               
                dx = cx - old_cx
                dy = cy - old_cy 
                
                
                distance_covered = np.hypot(dx, dy)
                
                if distance_covered > 15:
                    if self.camera_position == "back":
                        
                        if dy > 15:
                            friction_events[obj_id] = "Wrong Way"
                            
                    elif self.camera_position == "front":
                        
                        if dy < -15:
                            friction_events[obj_id] = "Wrong Way"


        self.stationary_frames = {k: v for k, v in self.stationary_frames.items() if k in objects}
        self.history = {k: v for k, v in self.history.items() if k in objects}
        
        return friction_events