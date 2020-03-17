from imutils import face_utils
import dlib
import cv2
from win10toast import ToastNotifier 
from scipy.spatial import distance
import time
import numpy as np

# CREDITS
# Facial Landmarks: Italo José (https://towardsdatascience.com/facial-mapping-landmarks-with-dlib-python-160abcf7d672)
# EAR calculation and blink counter syntax: Adrian Rosebrock (https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
# 20-20-20 rule: MedicalNewsToday (https://www.medicalnewstoday.com/articles/321536)
# Blink Rate: Blehm et al. (Computer Vision Syndrome: A Review)

p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)

def EAR(landmarks):
	ear_1 = distance.euclidean(landmarks[1], landmarks[5])
	ear_2 = distance.euclidean(landmarks[2], landmarks[4])
	ear_3 = distance.euclidean(landmarks[0], landmarks[3])

	ear = (ear_1 + ear_2)/(2*ear_3)
	return ear

EAR_THRESH = 0.3
EAR_CONSEC_FRAMES = 3

blink_counter = 0 # how many blinks
frame_blink_counter = 0 # how many frames with less than EAR threshold
frame_counter = 0 # frame counter from initialization

time_array = [] # store corresponding time when user blinks
frame_blink_array = [] # store corresponding frame when user blinks
blink_20_array = []
blink_20_counter = 0
start = False
abs_start = time.time() # initialized time

while True:
    # Getting out image by webcam 
    _, image = cap.read()

    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Get faces into webcam's image
    rects = detector(gray, 0)
    # For each detected face, find the landmark.

    for (i, rect) in enumerate(rects):
        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        left_ear = EAR(left_eye)
        right_ear = EAR(right_eye)
        eye_ear = (left_ear+right_ear)/2
        
        if not start:
            start = True
            time_start = time.time() # start timer
        
        frame_counter+=1
        time_frame = time.time() # corresponding time for the last frame
            
        if time_frame-time_start > 1210: #if it has been X seconds since the timer started, show toast notification. Extra 10 seconds for slack
            toaster = ToastNotifier()
            toaster.show_toast('Take a break.', "You've been looking at the screen for 20 minutes", duration=5)
            
            blink_20_array.append((blink_20_counter, time_frame-time_start))
            blink_20_counter = 0
            start = False

        if eye_ear < EAR_THRESH:
            frame_blink_counter+=1

        else:
            if frame_blink_counter >= EAR_CONSEC_FRAMES:
                blink_counter+=1
                blink_20_counter+=1
                frame_blink_array.append(frame_counter)
                time_array.append(time.time())

            frame_blink_counter=0

        # Draw on our image, all the finded cordinate points (x,y) 
        for (x, y) in shape[36:48]:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
    
    # Show the image
    cv2.imshow("Output", image)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        abs_end = time.time() - abs_start

        blink_20_array.append((blink_20_counter, time_frame-time_start))

        x = 0 #temporary blink counter
        y = 0 #temporary duration counter
        for i in blink_20_array:
            x = x + i[0]
            y = y + i[1]
        
        blink_per_min = (x/y)*60
        print(blink_20_array, x, y, blink_per_min)
        string = 'APP INFO \nApplication Run Time: {:.2f} seconds\n \nBLINK INFO \nTotal: {} blinks\nBlinks/Minute: {:.2f} blinks/minute'.format(abs_end, blink_counter, blink_per_min)

        file1 = open("Blink Summary.txt","w") 
        file1.write(string)
        file1.close() 
        break

cv2.destroyAllWindows()
cap.release()