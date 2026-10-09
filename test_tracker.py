import cv2
import os
from src.vehicle_tracker import VehicleTracker

def main():
    video_path = r"D:\AI-Traffic-Management-System\data\raw\traffic_videos\traffic_02.mp4"
    output_path = r"D:\AI-Traffic-Management-System\outputs\test_output_02.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Could not find video at {video_path}")
        return

    # Initialize tracker
    tracker = VehicleTracker('yolov8s.pt')
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Prepare video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Processing video: {video_path}")
    print(f"Resolution: {width}x{height} @ {fps} FPS")
    
    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Process frame
        result = tracker.process_frame(frame)
        
        # Draw results on frame
        annotated_frame = result.plot()
        
        # Write to output video
        out.write(annotated_frame)
        
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames...")
            
        # For testing, stop after 150 frames (approx 5 seconds)
        if frame_count >= 150:
            print("Stopping early for test run.")
            break
            
    cap.release()
    out.release()
    print(f"Done! Test output saved to {output_path}")

if __name__ == "__main__":
    main()
