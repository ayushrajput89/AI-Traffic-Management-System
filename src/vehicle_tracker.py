import cv2
from ultralytics import YOLO

class VehicleTracker:
    def __init__(self, model_path='yolov8s.pt'):
        """
        Initializes the YOLOv8 model for vehicle tracking.
        We use yolov8s.pt for a good balance of speed and accuracy.
        """
        print(f"Loading YOLO model from {model_path}...")
        self.model = YOLO(model_path)
        # COCO class IDs: 2: car, 3: motorcycle, 5: bus, 7: truck
        # Ambulance is not a default COCO class, but it usually gets detected as a truck or van (car/bus).
        # We will handle emergency vehicle classification later.
        self.target_classes = [2, 3, 5, 7]

    def process_frame(self, frame, conf=0.3):
        """
        Runs YOLOv8 detection and ByteTrack tracking on a single frame.
        """
        # persist=True keeps track IDs across frames
        # tracker="bytetrack.yaml" uses the ByteTrack algorithm (better for occlusion)
        results = self.model.track(
            frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            classes=self.target_classes,
            conf=conf,
            verbose=False
        )
        return results[0]
