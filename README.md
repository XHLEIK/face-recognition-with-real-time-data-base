# Face Recognition with Real-Time Database

A real-time face recognition attendance system that uses computer vision to identify individuals and maintain attendance records.

## Features

- Real-time face recognition using webcam
- Automatic attendance logging
- CSV-based attendance reports organized by date and week
- Background overlay with mode indicators
- Support for multiple known faces

## Requirements

- Python 3.x
- OpenCV (cv2)
- face_recognition
- numpy
- csv (built-in)
- datetime (built-in)

## Installation

1. Clone this repository
2. Install required packages:
   ```bash
   pip install opencv-python face_recognition numpy
   ```
3. Create the following directory structure:
   ```
   images/          # Add your reference face images here
   Resources/
   ├── background.png    # Background image for the UI
   └── Modes/           # Mode indicator images (1.png, 4.png, etc.)
   ```

## Setup

1. Add reference face images to the `images/` folder
2. Update the `load_known_faces()` function in `program.py` with your face data
3. Ensure the paths in the script match your directory structure

## Usage

Run the main program:
```bash
python program.py
```

## File Structure

- `program.py` - Main application file
- `FaceRecognitionAttendenceWithDataBase/attendence_report/` - Attendance logs organized by year/week
- `.gitignore` - Excludes images and other non-essential files from version control

## Note

The `images/` and `Resources/` folders are excluded from version control for privacy and size reasons. You'll need to add your own reference images and UI resources.
