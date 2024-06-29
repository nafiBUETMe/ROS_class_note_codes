#! /usr/bin/python3

#importing ros dependencies
import rospy
import sys

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image as Image_sub

#importing some basic dependencies

import numpy as np
import cv2
import sys
import time
import mediapipe as mp


#info opencv basic
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 0.75
color = (255, 0, 0)
thickness = 2



def callback_pc(data):
			global screen_text
			screen_text = data
			
def mediapipe_multi_face(input_image, edited_image, face_landmarks_matrix):

	mp_face_detection = mp.solutions.face_detection
	mp_drawing = mp.solutions.drawing_utils

	with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

    		image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    		image.flags.writeable = False
    		
    		# Make detection
    		results = face_detection.process(image)

    		# Draw the face detection annotations on the image.
    		image.flags.writeable = True
    		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    		
    		# Extract landmarks
    		try:
    			landmarks = results.detections
    			#print(landmarks)
    			for i in range (0,6):
    				face_landmarks_matrix[i,:] = [landmarks[0].location_data.relative_keypoints[i].x, landmarks[0].location_data.relative_keypoints[i].y]
    				#print(face_landmarks_matrix[i,:])
    			#print(nose)
    		except:
    			face_landmarks_matrix = np.full(face_landmarks_matrix.shape, -1.5)
    			pass
    		
    		#print(face_landmarks_matrix)
    		
    		# Render detections
    		if results.detections:
    			for detection in results.detections:
    				mp_drawing.draw_detection(edited_image, detection)

	return edited_image, face_landmarks_matrix

#the looping video processing thread------------------------------------------------------------
def video_thread():
 
	#landmark matrix variables
	face_landmarks_matrix = np.zeros((6,2))
	face_landmarks_matrix = np.full(face_landmarks_matrix.shape, -1.5)

	video_capture = cv2.VideoCapture(0)

	while True:
			
		#VIDEO FEED (FACE)
		face_landmarks_matrix = np.zeros((6,2))
		result, video_frame = video_capture.read()  # read frames from the video
		
		if result is False:
			pass
		else:
			#mediapipe detection
			video_frame, face_landmarks_matrix = mediapipe_multi_face(video_frame, video_frame, face_landmarks_matrix)
		
		#print(face_location_data)
		if(0 <= face_landmarks_matrix[0,0] <= 1):
			face_x = (100*(face_landmarks_matrix[0,0]))
			face_location_data = 'X'+str(round(face_x))
			data_pub.publish(face_location_data)
		
		#point of interest for feedback purpose
		#poi = [0.5, 0.5]
		poi = face_landmarks_matrix[0,0:2]
		#print(poi)
		#print('LOOP')
		
		cv2.circle(video_frame,(int(640*poi[0]), int(480*poi[1])),1,(0,0,255),4) #visual feedback purpose
		try:
			text_string = 'POT val:' + str(screen_text)
			cv2.putText(video_frame, text_string, org, font,  fontScale, color, thickness, cv2.LINE_AA) 
		except:
			pass
		
		#robot movement---------------------------------------------------
		cv2.imshow("Video Feed", video_frame)	
		
		
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	video_capture.release()
	cv2.destroyAllWindows()
	
			

if __name__ == '__main__':

    	rospy.init_node('Interactive_Bot',anonymous=True)
    	
    	rospy.Subscriber("data_to_pc", String, callback_pc)
    	data_pub = rospy.Publisher('data_to_arduino', String, queue_size=10)

    	video_thread()
    	
    	

