# AI Traffic Management System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-traffic-management-system.streamlit.app/)

> 🚀 **Live Demo:** [ai-traffic-management-system.streamlit.app](https://ai-traffic-management-system.streamlit.app/)

A real-time traffic management project built using Computer Vision to dynamically adjust traffic signals based on live vehicle density. Instead of relying on static timers, this system calculates active road congestion and allocates green light duration accordingly.

## Features

- **Vehicle Tracking:** Uses YOLOv8s and ByteTrack for robust object detection and ID tracking across frames.
- **Zone-Based Counting:** Replaces traditional line-counting with a 200px band to handle chaotic and cross-lane traffic more effectively.
- **Adaptive Signal Control:** Calculates the real-time density of vehicles inside the zone. High density yields longer green lights, while lower density shortens them.
- **Speed Estimation:** Calculates relative speed (in km/h) based on pixel displacement and frame rates.
- **Red Light Violations:** Flags vehicles that cross the counting zone during a simulated red light phase.
- **Interactive Dashboard:** A complete Streamlit web interface containing live video feeds, real-time metrics, line charts for traffic density, and model evaluation stats.

## Tech Stack
- Python 3.x
- OpenCV (Computer Vision logic)
- Ultralytics YOLOv8 (Object Detection)
- ByteTrack (Multi-object tracking)
- Streamlit (Web UI)
- Pandas (Data processing)

## Setup Instructions

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install ultralytics opencv-python pandas streamlit
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

*Note: The original video datasets and weights (yolov8s.pt) are excluded from version control to save space. Place any traffic videos in `data/raw/traffic_videos/` and the dashboard will automatically detect them.*

## Future Improvements
- Integration with GroundingDINO for zero-shot detection of emergency vehicles (ambulances/firetrucks) to implement automatic signal overrides.
- Applying perspective transformation (Bird's Eye View) to correct camera angle distortion for mathematically precise speed calculations.
