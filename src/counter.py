import cv2
import math

class VehicleCounter:
    def __init__(self, zone_y1=400, zone_y2=600, fps=30):
        self.zone_y1 = zone_y1
        self.zone_y2 = zone_y2
        self.fps = fps if fps > 0 else 30
        
        self.counted_ids = set()
        self.total_count = 0
        self.current_in_zone = 0
        self.class_counts = {}
        
        # New Features: Speed & Violations
        self.last_positions = {}
        self.speeds = {}
        self.violations = 0
        self.violator_ids = set()
        self.pixels_per_meter = 25 # Rough calibration factor
        self.current_draw_data = [] # To store text overlay info for the current frame

    def process_tracks(self, results, signal_color="🟢"):
        self.current_in_zone = 0
        self.current_draw_data = []
        
        if results.boxes is None or results.boxes.id is None:
            return self.total_count

        boxes = results.boxes.xyxy.cpu().numpy()
        track_ids = results.boxes.id.int().cpu().numpy()
        classes = results.boxes.cls.int().cpu().numpy()

        for box, track_id, cls_id in zip(boxes, track_ids, classes):
            x1, y1, x2, y2 = box
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            # --- Speed Estimation ---
            speed_kmh = 0
            if track_id in self.last_positions:
                prev_cx, prev_cy = self.last_positions[track_id]
                dist_pixels = math.hypot(cx - prev_cx, cy - prev_cy)
                
                # Formula: Speed (km/h) = (Distance in meters / Time in seconds) * 3.6
                instant_speed = (dist_pixels / self.pixels_per_meter) * self.fps * 3.6
                
                # Exponential Moving Average for smoothing speed
                if track_id in self.speeds:
                    self.speeds[track_id] = int(0.8 * self.speeds[track_id] + 0.2 * instant_speed)
                else:
                    self.speeds[track_id] = int(instant_speed)
                    
                speed_kmh = self.speeds[track_id]
                
            self.last_positions[track_id] = (cx, cy)

            # --- Zone & Violation Logic ---
            if self.zone_y1 <= cy <= self.zone_y2:
                self.current_in_zone += 1
                
                if track_id not in self.counted_ids:
                    self.counted_ids.add(track_id)
                    self.total_count += 1
                    cls_name = results.names[cls_id]
                    self.class_counts[cls_name] = self.class_counts.get(cls_name, 0) + 1
                    
                    # Red Light Violation Logic
                    if signal_color == "🔴":
                        self.violations += 1
                        self.violator_ids.add(track_id)
                        
            # Store drawing data for this vehicle
            is_violator = track_id in self.violator_ids
            self.current_draw_data.append((x1, y1, speed_kmh, is_violator))

        return self.total_count

    def draw_zone(self, frame):
        width = frame.shape[1]
        
        # Draw the zone boundaries
        cv2.line(frame, (0, self.zone_y1), (width, self.zone_y1), (0, 255, 0), 2)
        cv2.line(frame, (0, self.zone_y2), (width, self.zone_y2), (0, 255, 0), 2)
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, self.zone_y1), (width, self.zone_y2), (0, 255, 0), -1)
        cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

        # Draw vehicle speeds and violation alerts
        for x1, y1, speed, is_violator in self.current_draw_data:
            if speed > 5: # Only show speed if moving
                text = f"{speed} km/h"
                color = (0, 255, 255)
                if is_violator:
                    text = f"VIOLATION! {speed}km/h"
                    color = (0, 0, 255) # Red for violator
                cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Helper function for drawing metrics
        def draw_text_with_bg(img, text, position, font_scale=0.8, thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
            x, y = position
            (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            cv2.rectangle(img, (x - 10, y - text_h - 10), (x + text_w + 10, y + 10), bg_color, -1)
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

        # Drawing improved metrics on top left
        draw_text_with_bg(frame, f"Total Passed: {self.total_count}", (30, 50), text_color=(0, 255, 255))
        draw_text_with_bg(frame, f"In Zone: {self.current_in_zone}", (30, 100), text_color=(0, 255, 0))
        
        if self.violations > 0:
            draw_text_with_bg(frame, f"Red Light Violations: {self.violations}", (30, 150), text_color=(0, 0, 255), bg_color=(200, 200, 200))
                    
        return frame
