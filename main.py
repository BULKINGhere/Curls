import Left_curl
import Right_curl
import curls
#import cv2
import mediapipe as mp
#import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Right_curl.start_right_curl(pose)
        #Left_curl.start_left_curl(pose)
        curls.start_curl(pose)
