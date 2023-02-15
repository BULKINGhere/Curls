#import numpy as np
# import Left_curl
#import right_curl
import curl
#import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        #right_curl.start_right_curl(pose)
        #Left_curl.start_left_curl(pose)
        curl.start_curl(pose)
