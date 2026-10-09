import os
import cv2

video_dir = r"D:\AI-Traffic-Management-System\data\raw\traffic_videos"
output_dir = r"C:\Users\DELL\.gemini\antigravity\brain\b1350ca3-b7f0-4568-935f-35689bd07991\video_previews_batch2"

os.makedirs(output_dir, exist_ok=True)

files = os.listdir(video_dir)
for f in files:
    if f.startswith('traffic_'):
        continue  # Skip already kept ones
    if not f.endswith(('.mp4', '.mov')):
        continue
    
    vid_path = os.path.join(video_dir, f)
    cap = cv2.VideoCapture(vid_path)
    
    # Check width/height to auto-skip vertical
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    # Fast forward a bit to avoid black starting frames
    cap.set(cv2.CAP_PROP_POS_FRAMES, 30)
    ret, frame = cap.read()
    
    if ret:
        out_path = os.path.join(output_dir, f + ".jpg")
        
        if w < h:
            # Draw "VERTICAL" on it so we know immediately
            cv2.putText(frame, "VERTICAL REJECT", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
            
        # Optional: Save thumbnail
        thumb = cv2.resize(frame, (1280, 720)) if w > 1280 else frame
        cv2.imwrite(out_path, thumb)
        print(f"Extracted {f}")
    else:
        print(f"Failed to read {f}")
        
    cap.release()

print("All done!")
