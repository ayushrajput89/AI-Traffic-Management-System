import os

video_dir = r"D:\AI-Traffic-Management-System\data\raw\traffic_videos"

keep_files = [
    "10297595-hd_3840_2160_30fps.mp4",
    "12519640_1920_1080_30fps.mp4",
    "12973804_3840_2160_30fps.mp4",
    "13550711_3840_2160_25fps.mp4",
    "13654799_1920_1080_30fps.mp4",
    "16385623_3840_2160_30fps.mp4",
    "18733707-uhd_3840_2160_60fps.mp4",
    "19532260-uhd_3840_2160_60fps.mp4",
    "2863232-uhd_3840_2160_30fps.mp4",
    "3360811-uhd_3840_2160_30fps.mp4",
    "3694427-hd_1920_1080_30fps.mp4",
    "3696011-hd_1920_1080_24fps.mp4"
]

delete_files = [
    "12010437_2160_3840_30fps.mp4",
    "13489225_3840_2160_60fps.mp4",
    "1388383-hd_1920_1080_30fps.mp4",
    "1390281-hd_1920_1080_30fps.mp4",
    "1390562-hd_1920_1080_30fps.mp4",
    "1393755-hd_1920_1080_30fps.mp4",
    "1393766-hd_1920_1080_30fps.mp4",
    "14958812_3840_2160_30fps.mp4",
    "15123110_1920_1080_60fps.mp4",
    "18496733-hd_1920_1080_30fps.mp4",
    "3759222-hd_1920_1080_30fps.mp4"
]

# Delete bad files
for f in delete_files:
    path = os.path.join(video_dir, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {f}")

# Rename keep files to sequential format (traffic_09 to traffic_20)
start_idx = 9
for f in keep_files:
    old_path = os.path.join(video_dir, f)
    if os.path.exists(old_path):
        ext = os.path.splitext(f)[1]
        new_name = f"traffic_{start_idx:02d}{ext}"
        new_path = os.path.join(video_dir, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {f} -> {new_name}")
        start_idx += 1

print("Cleanup and renaming completed successfully!")
