import numpy as np

class Tracker:
    def __init__(self, dist_threshold=60):
        self.objects = {}
        self.id_count = 0
        self.dist_threshold = dist_threshold

    def update(self, detections):
        new_objects = {}

        for det in detections:
            x1, y1, x2, y2, label, conf = det
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            matched = False
            best_match_id = None
            min_dist = float('inf')

            for obj_id, (ox, oy) in self.objects.items():
                dist = np.sqrt((cx - ox)**2 + (cy - oy)**2)
                if dist < self.dist_threshold and dist < min_dist:
                    min_dist = dist
                    best_match_id = obj_id

            if best_match_id is not None:
                new_objects[best_match_id] = (cx, cy, det)
                matched = True
                del self.objects[best_match_id] 
            else:
                new_objects[self.id_count] = (cx, cy, det)
                self.id_count += 1

        self.objects = {k: (v[0], v[1]) for k, v in new_objects.items()}
        return new_objects