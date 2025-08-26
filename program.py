import cv2
import face_recognition
import numpy as np
import csv
import os
from datetime import datetime, timedelta

# Paths
ATTENDANCE_BASE_DIR = r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\FaceRecognitionAttendenceWithDataBase\attendence_report"
BACKGROUND_PATH = r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\background.png"

# Load the background image
background = cv2.imread(BACKGROUND_PATH)

# Check if background image was loaded successfully
if background is None:
    print("Error: Could not load background image. Check the file path.")
    exit(1)

# Load mode images (these will be replaced with individual images for each person)
mode_ready = cv2.imread(r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\1.png")
mode_4 = cv2.imread(r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\4.png")  # Image for 5 seconds

# Check if mode images are loaded properly
if mode_ready is None or mode_4 is None:
    print("Error: Mode images could not be loaded.")
    exit(1)

# Load known faces and their details
def load_known_faces():
    known_faces = [
        ("Alakh", "BWU_BCA_23_265", "images/321654.png"),
        ("Emily", "BWU_BCA_23_241", "images/852741.png"),
        ("Elon Musk", "BWU_BCA_23_963", "images/963852.png"),
        ("Arindam Das", "BWU_BCA_23_265", r"images\BWU_BCA_23_265.png"),
        ("Ankita Seth", "BWU_BCA_23_241", r"images\BWU_BCA_23_241.png"),
        ("Sujata", "BWU_BCA_23_258", r"images\BWU_BCA_23_258.PNG"),
        ("Katha Nandi", "BWU_BCA_23_254", r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\images\BWU_BCA_23_254.PNG"),
        ("Debabrata Das", "BWU_BCA_23_242", r"images\BWU_BCA_23_242.png"),
        ("Snehasish Harbab", "BWU_BCA_23_245", r"images\BWU_BCA_23_245.png"),
        ("Ankur", "BWU_BCA_23_250", r"images\BWU_BCA_23_250.PNG"),
        ("Sayantani", "BWU_BCA_23_253", r"images\BWU_BCA_23_253.png"),
        ("Subham Bose", "BWU_BCA_23_283", r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\images\BWU_BCA_23_283.PNG")
    ]

    known_face_encodings = []
    known_face_names = []
    known_face_ids = []
    name_to_image_map = {
        "Elon Musk": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\10.png",
        "Alakh": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\11.png",
        "Emily": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\12.png",
        "Ankita Seth": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\241.png",
        "Debabrata Das": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\242.png",
        "Snehasish Harbab": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\245.png",
        "Ankur": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\250.png",
        "Sayantani": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\253.png",
        "Katha Nandi": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\254.png",
        "Sujata": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\258.png",
        "Arindam Das": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\265.png",
        "Subham Bose": r"C:\Users\ASUS\Desktop\pythonProject\FaceRecognitionRealTimeDatabase\Resources\Modes\283.png"
    }

    for name, user_id, image_path in known_faces:
        if not os.path.exists(image_path):
            print(f"Error: Could not find image for {name} at {image_path}")
            continue
        try:
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
            known_face_ids.append(user_id)
        except Exception as e:
            print(f"Error loading or encoding image {image_path}: {e}")
            continue

    return known_face_encodings, known_face_names, known_face_ids, name_to_image_map

# Initialize
known_face_encodings, known_face_names, known_face_ids, name_to_image_map = load_known_faces()
video_capture = cv2.VideoCapture(0)

# Date and directory setup
current_date = datetime.now()
year = current_date.strftime("%Y")
week_number = current_date.strftime("%U")
day = current_date.strftime("%Y-%m-%d")

year_dir = os.path.join(ATTENDANCE_BASE_DIR, year)
week_dir = os.path.join(year_dir, f"week_{week_number}")
os.makedirs(week_dir, exist_ok=True)

attendance_file = os.path.join(week_dir, f"{day}.csv")

# Check if attendance file exists to prevent duplicate entries
attendance_recorded = set()
if os.path.isfile(attendance_file):
    with open(attendance_file, "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            attendance_recorded.add(row[0])  # Add the User ID to recorded set
else:
    with open(attendance_file, "w", newline="") as f:
        lnwriter = csv.writer(f)
        lnwriter.writerow(["User ID", "Name", "Time"])

last_detected_times = {}  # Track last detection times for each user
person_shown_4_seconds = {}  # Track when each person should see the 4.png

while True:
    output_image = background.copy()
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    name = "Unknown"  # Default name if no face is detected
    user_id = None  # Default user_id if no face is detected

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            user_id = known_face_ids[best_match_index]

            # Load the person's specific image from the name_to_image_map
            person_image_path = name_to_image_map.get(name, "images/default.png")
            person_image = cv2.imread(person_image_path)

            if person_image is None:
                print(f"Error: Could not load image for {name} from {person_image_path}")
                continue

            # Check if the person is already recorded for the day
            if user_id not in attendance_recorded:
                current_time = datetime.now().strftime("%H:%M:%S")
                with open(attendance_file, "a", newline="") as f:
                    lnwriter = csv.writer(f)
                    lnwriter.writerow([user_id, name, current_time])
                attendance_recorded.add(user_id)  # Add user_id to recorded set

            # Update the last detected time
            last_detected_times[user_id] = datetime.now()

            # Draw rectangle around the face on output image
            top, right, bottom, left = face_location
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(output_image, (50 + left, 150 + top), (50 + right, 150 + bottom), (0, 255, 0), 2)

            # Resize person image to 414x633 for overlay
            person_image_resized = cv2.resize(person_image, (414, 633))

            # Define the shift
            shift = 8  # You can adjust this value to shift more or less
            vertical_shift = -5  # Move the image 4 pixels up (negative value moves it up)

            # Place the resized image at the new shifted position
            output_image[50 + vertical_shift:50 + vertical_shift + person_image_resized.shape[0],
            800 + shift:800 + shift + person_image_resized.shape[1]] = person_image_resized

            # Track the time of detection for 4 seconds image
            if user_id not in person_shown_4_seconds:
                person_shown_4_seconds[user_id] = datetime.now()

            # Check if 5 seconds have passed since last detection
            if datetime.now() - person_shown_4_seconds[user_id] >= timedelta(seconds=5):
                # Show 4.png for this person
                person_4_resized = cv2.resize(mode_4, (414, 633))
                output_image[50 + vertical_shift:50 + vertical_shift + person_4_resized.shape[0],
                             800 + shift:800 + shift + person_4_resized.shape[1]] = person_4_resized

    # If no faces are detected, display the "ready" mode (1.png)
    if name == "Unknown":
        # Resize the "ready" image (1.png)
        mode_ready_resized = cv2.resize(mode_ready, (414, 633))  # Resize to desired size

        # Define the shift values for the "ready" image
        shift = 8  # Horizontal shift
        vertical_shift = -5  # Vertical shift (move image up)

        # Place the resized "ready" image at the shifted position
        output_image[50 + vertical_shift:50 + vertical_shift + mode_ready_resized.shape[0],
                     800 + shift:800 + shift + mode_ready_resized.shape[1]] = mode_ready_resized

    # Place the camera frame
    resized_frame = cv2.resize(frame, (650, 500))
    output_image[150:650, 50:700] = resized_frame

    # Display name near the top-right corner of the image
    cv2.putText(output_image, f"{name} Present", (200, 600), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 3)
    cv2.putText(output_image, f"{name} ", (935, 495), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display ID below name
    if user_id:  # Only show ID if a valid user_id is found
        cv2.putText(output_image, f"{user_id}", (935, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show the image
    cv2.imshow("Attendance System", output_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
video_capture.release()
cv2.destroyAllWindows()
