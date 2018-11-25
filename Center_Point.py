import numpy as np
import cv2
import time
import os
import math

width=320
height=240
preLeft=0
preRight=0

h1=int(0.6*height)
h2=int(0.7*height)
y_point=int(0.65*height)
carPos=(160,240)


lower=np.array([0,17,100 ])
upper=np.array([180,255,255])

def filter(image, kernel_er, kernel_di):
	kernel_1 = np.ones((kernel_er,kernel_er),np.uint8)
	kernel_2 = np.ones((kernel_di,kernel_di),np.uint8)
	image = cv2.erode(image,kernel_1,iterations = 1)
	image = cv2.dilate(image,kernel_2,iterations = 1)
	return image
def GetPointLeft(mask,test):
	left = mask[h1:h2, 0:int(width/2)]
	keypoint = np.nonzero(left)
	Row,Col=keypoint
	
	if len(Col)==0:
		x_left=0
		print('preLeft ', x_left)
		cv2.putText(test,'NOT LEFT',(30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),2,cv2.LINE_AA)
	else:
		x_left=max(Col)
	
	cv2.imshow('L ', left)

	return x_left

def GetPointRight(mask,test):

	right = mask[h1:h2, int(width/2):width]
	keypoint = np.nonzero(right)
	Row,Col=keypoint
	if len(Col)==0 :
		x_right=320
		print('preRight : ', x_right)
		cv2.putText(test,'NOT RIGHT',(30,200), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),2,cv2.LINE_AA)
	else:
		x_right =min(Col)+int(width/2)
	cv2.imshow('R',right)
	return x_right


def GetCenterPoint(img,test):
            

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	mask=filter(mask,1,11)
	x_left=GetPointLeft(mask,test)
	x_right=GetPointRight(mask,test)
	if x_left>100 or x_right<200:
		x_right=320

	print('L: ', x_left , '		R: ',x_right)


	cv2.circle(test,(x_left,y_point), 10, (0,0,255), -1)
	cv2.circle(test,(x_right,y_point), 10, (0,0,255), -1)
	centerPoint=((int((x_right - x_left)/2)+x_left),y_point)
	# cv2.imshow('mask', mask)
	return centerPoint

def GetAngle(img,test):
	
	centerPoint=GetCenterPoint(img,test)
	cv2.line(test, centerPoint, carPos, (0,255,0), 2)
	if (centerPoint[0] == carPos[0]):
		return 0
	if (centerPoint[1] == carPos[1]):
		if centerPoint[0] <carPos[0]:
			return -90
		else:
			return 90
	pi = math.acos(-1.0);
	dx = centerPoint[0] - carPos[0]
	dy = centerPoint[1] - carPos[1] 
	if (dx < 0): 
		return math.atan(-dx / dy) * 180 / pi
	return -math.atan(dx / dy) * 180 / pi


# folder_lance="D:\\Project\\CuocDuaSo2018\\lane_detect\\src\\ImageLane\\"


# for i in os.listdir(folder_lance):
# 	im=folder_lance+i
# 	img=cv2.imread(im)
# 	print(GetAngle(img))
# 	cv2.waitKey()
#  