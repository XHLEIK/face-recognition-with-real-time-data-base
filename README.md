Face Recognition Attendance System with Real-time Database
This project implements a real-time face recognition attendance system using OpenCV, face_recognition, and a CSV-based attendance recording mechanism. It captures video through a webcam, identifies registered individuals, and logs their attendance into a structured CSV file system based on the date and week.

Table of Contents
Features
Technologies Used
Project Structure
Setup Instructions
Usage
Known Issues
Contributing
License
Features
Real-time face detection using a webcam feed.
Recognizes and matches faces against a database of registered users.
Automatically logs attendance in a CSV file, organized by year and week.
Displays different modes (ready, detected, and 4 seconds display) depending on the person’s interaction.
Provides a flexible mechanism to add new users with their face images.
Prevents duplicate attendance entries for the same day.
Technologies Used
Python 3.7+
OpenCV (for image processing and webcam interaction)
face_recognition (for face detection and encoding)
NumPy (for mathematical operations)
CSV (for attendance logging)
OS (for file and directory management)
Datetime (for organizing attendance records)
Project Structure
/FaceRecognitionAttendanceSystem
│
├── /Resources
│   ├── background.png        # Background template for the UI
│   └── Modes                 # Contains images for different modes (ready, 4 seconds, etc.)
├── /images                   # Contains images of registered users
│   ├── BWU_BCA_23_254.png    # Example image for a user
│   └── ...                   # Additional user images
├── /attendence_report         # Where CSV attendance files are stored, organized by year/week
│
└── attendance.py             # Main script for running the face recognition system
Setup Instructions
1. Prerequisites
Ensure you have Python 3.7+ installed on your machine. Install the required Python libraries by running the following command:
pip install opencv-python face-recognition numpy
2. Directory Structure
Make sure to create the necessary directories and resources:

Add face images of individuals in the /images folder.
Ensure the background.png and mode images (e.g., 1.png, 4.png) are correctly placed in the /Resources folder.
3. Edit Script
If needed, edit the file paths in attendance.py to match your system’s directory structure. For example:
ATTENDANCE_BASE_DIR = r"C:\path\to\attendence_report"
BACKGROUND_PATH = r"C:\path\to\Resources\background.png"
4. Run the Program
To start the attendance system, run the following command in the terminal:
python attendance.py
The program will:

Open a webcam feed.
Identify and log known users in a CSV file located in attendence_report/<year>/week_<number>/<date>.csv.
Display the person’s name and user ID when recognized.
Usage
Register users by adding their images and details into the script.
Run the program and allow the webcam to detect faces.
The system logs attendance automatically, creating a new CSV file for each day.
View attendance logs in the attendence_report folder, organized by week.
Known Issues
If face detection fails, ensure the image quality and lighting conditions are good.
Ensure the images used for face encoding are clear and properly cropped around the face.
If the program is unable to load specific images, check the file paths and file formats.
Contributing
Feel free to fork this repository and make improvements. Pull requests are welcome!

License
This project is licensed under the MIT License.
