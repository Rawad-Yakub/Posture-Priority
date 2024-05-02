import cv2                      #computer vision
import math as m
import matplotlib.pyplot as plt 
import mediapipe as mp          #body recognition
import numpy as np
from PIL import Image
import streamlit as st

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

def EvalImage(image):
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    landmarks = process_image(image)
    annotated_image = draw_landmarks(image, landmarks)
    st.image(annotated_image, channels="BGR", caption="Landmarks and Connections Detected")

        # Extract and print landmark coordinates
    img_width, img_height = image.shape[1], image.shape[0]
    l_knee_x, l_knee_y = extract_landmark_coordinates(landmarks, img_width, img_height)
        ##st.write(f"Left knee coordinates: ({l_knee_x}, {l_knee_y})")
        
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    results = pose.process(image)

    h, w = image.shape[:2]

        # Use lm and lmPose as representative of the following methods.
    lm = results.pose_landmarks
    lmPose = mp_pose.PoseLandmark
        # Left shoulder.
    l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
    l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

        # Right shoulder.
    r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
    r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

        # Left ear.
    l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
    l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

        # Left hip.
    l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
    l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)
    neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
    torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

    if neck_inclination > 40 or neck_inclination > 10:
            st.write("Your posture is bad")
    else:
            st.write("Your posture is good")
    
    visualize_landmark_coordinates(image, l_knee_x, l_knee_y)