import os
import urllib.request
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path="best.pt"):
        
        model_url = "https://huggingface.co/kushagrahere/vehicle-detection-yolov8/resolve/main/best.pt"
        
        
        if not os.path.exists(model_path):
            print(f"\nDownloading Indian vehicle weights to '{model_path}'...")
            try:
                urllib.request.urlretrieve(model_url, model_path)
                print("Download complete!\n")
            except Exception as e:
                print(f"Download failed: {e}")
                
        self.model = YOLO(model_path)

    def detect(self, frame):
       
        results = self.model.track(frame, persist=True, tracker="bytetrack.yaml", conf=0.15, verbose=False)[0]
        
        tracked_objects = {}

        if results.boxes.id is None:
            return tracked_objects

        for box, obj_id in zip(results.boxes, results.boxes.id):
            cls_id = int(box.cls[0])
            raw_label = str(self.model.names[cls_id]).lower()

           
            if raw_label in ["auto", "auto-rickshaw", "autorickshaw", "tuk-tuk", "three-wheeler", "rickshaw", "cng"]:
                label = "autorickshaw"
            elif raw_label in ["motorcycle", "bike", "two-wheeler", "scooter"]:
                label = "bike"
            elif raw_label in ["lcv", "truck", "multiaxle", "tractor", "pickup", "van"]:
                label = "truck"
            elif raw_label in ["car", "bus"]:
                label = raw_label
            else:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            track_id = int(obj_id)
            
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            det = [x1, y1, x2, y2, label, conf]
            tracked_objects[track_id] = (cx, cy, det)

        return tracked_objects