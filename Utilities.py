import math as m
import matplotlib.pyplot as plt 
import mediapipe as mp
from PIL import Image
import cv2

# Initialize MediaPipe modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to process uploaded image and detect landmarks
def process_image(image):
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:  # Adjust confidence thresholds as needed
        results = pose.process(image)
        return results.pose_landmarks

# Function to draw landmarks and connections on the image
def draw_landmarks(image, landmarks):
    annotated_img = image.copy()
    point_spec = mp_drawing.DrawingSpec(color=(220, 100, 0), thickness=-1, circle_radius=5)
    line_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
    mp_drawing.draw_landmarks(
        annotated_img,
        landmark_list=landmarks,
        connections=mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=point_spec,
        connection_drawing_spec=line_spec
    )
    return annotated_img

# Function to extract landmark coordinates
def extract_landmark_coordinates(landmarks, img_width, img_height):
    l_knee_x = int(landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * img_width)
    l_knee_y = int(landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * img_height)
    # Extract other landmark coordinates similarly...
    return l_knee_x, l_knee_y  # Return coordinates of the left knee

# Function to visualize landmark coordinates
def visualize_landmark_coordinates(image, l_knee_x, l_knee_y):
    fig, ax = plt.subplots()
    ax.imshow(image[:, :, ::-1])
    ax.plot(l_knee_x, l_knee_y, 'ro')  # Plot left knee coordinates
    plt.show()
    
def findAngle(x1, y1, x2, y2):
    theta = m.acos( (y2 -y1)*(-y1) / (m.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
    degree = int(180/m.pi)*theta
    return degree