import cv2
import os
from src.vehicle_tracker import VehicleTracker
from src.counter import VehicleCounter
from src.signal_controller import SignalController

def main():
    # Let's test on one of the new videos, e.g., the rain highway one or night intersection
    video_path = r"D:\AI-Traffic-Management-System\data\raw\traffic_videos\traffic_10.mp4"
    output_path = r"D:\AI-Traffic-Management-System\outputs\test_signal_10.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Could not find video at {video_path}")
        return

    # Initialize modules
    tracker = VehicleTracker('yolov8s.pt')
    signal_controller = SignalController(max_capacity=15)  # Set expected capacity based on road size

    
    # Open video to get resolution dynamically
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create counting zone dynamically based on resolution (e.g. middle 20% of the screen)
    zone_y1 = int(height * 0.6)
    zone_y2 = int(height * 0.8)
    counter = VehicleCounter(zone_y1=zone_y1, zone_y2=zone_y2)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Processing video: {video_path}")
    print(f"Resolution: {width}x{height} @ {fps} FPS")
    print(f"Counting Zone: y={zone_y1} to y={zone_y2}")
    
    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # 1. Run tracking
        result = tracker.process_frame(frame)
        
        # 2. Draw standard YOLO boxes
        annotated_frame = result.plot()
        
        # 3. Update and draw counting zone
        counter.process_tracks(result)
        annotated_frame = counter.draw_zone(annotated_frame)
        
        # 4. Adaptive Signal Logic
        density, status, green_time = signal_controller.compute_signal(counter.current_in_zone)
        
        # Draw signal logic on frame
        cv2.putText(annotated_frame, f"Density: {density:.1f}%", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.putText(annotated_frame, f"Status: {status}", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.putText(annotated_frame, f"Green Time: {green_time}s", (30, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        
        # Write to output video
        out.write(annotated_frame)

        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames. Current count: {counter.total_count}")
            
        # Run test for about 10 seconds (roughly 300 frames)
        if frame_count >= 300:
            print("Stopping early for test run.")
            break
            
    cap.release()
    out.release()
    print(f"Done! Counting test output saved to {output_path}")
    print(f"Final Count breakdown: {counter.class_counts}")

if __name__ == "__main__":
    main()
