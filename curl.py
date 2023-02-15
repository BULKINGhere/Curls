import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Curl counter variables


def calculate_angle(a,b,c):
      a = np.array(a) # First
      b = np.array(b) # Mid
      c = np.array(c) # End

      radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
      angle = np.abs(radians*180.0/np.pi)

      if angle >180.0:
            angle = 360-angle
        
      return angle 

# VIDEO FEED
cap = cv2.VideoCapture(0)

def start_curl(pose):
      counter_left = 0
      counter_right = 0 
      stage_left = None
      stage_right = None
      while cap.isOpened():
            ret, frame = cap.read()
        
        # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
        # Make detection
            results = pose.process(image)
    
        # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
            try:
                  landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                  left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                  left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                  left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
                  right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                  right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                  right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # Calculate angle
                  angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
                  angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

            
            # Visualize angle
                  cv2.putText(image, str(angle_left), tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                  cv2.putText(image, str(angle_right), tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                       
        # Visualize angle
                  cv2.putText(image, str(angle_left), 
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                  cv2.putText(image, str(angle_right), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA
                                )
            # Curl counter logic
                  if angle_left > 145:
                        stage_left = "down"
                  if angle_left < 40 and stage_left =='down':
                        stage_left = "up"
                        counter_left += 1
                        print("L",counter_left)

                  if angle_right > 145:
                        stage_right = "down"
                  if angle_right < 40 and stage_right =='down':
                        stage_right = "up"
                        counter_right += 1
                        print("R",counter_right)
                       
            except:
                  pass
        
        # Render curl counter
        # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
            cv2.putText(image, 'REPS', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_left), (15,60), cv2.FONT_ITALIC, 2, (255,255,255), 2, cv2.LINE_AA)
        

            cv2.putText(image, 'REPS', (150,10), cv2.FONT_ITALIC, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_right), (150,60), cv2.FONT_ITALIC, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
            cv2.putText(image, 'STAGE', (65,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage_left, (65,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            cv2.putText(image, 'STAGE', (200,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage_right, (200,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
         
         # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                  break

      cap.release()
      cv2.destroyAllWindows()

