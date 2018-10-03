import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#read image in gray scale###############################################################
jgray = cv2.imread('jpeg.jpg',0)

#increase contrast###################################################################### 
#255 is divided for clipping the pixel value not to exceed 255 ref.https://stackoverflow.com/questions/49643907/clipping-input-data-to-the-valid-range-for-imshow-with-rgb-data-0-1-for-floa
jcontrast = jgray*1.8/255

#increase brightness 10 units###########################################################
jbright = jgray+20

#inverting############################################################################## 
jinv = (jgray*(-1))+255

#thresholding########################################################################### 
ret,jthresh = cv2.threshold(jgray,127,255,cv2.THRESH_BINARY)

#auto-contrast according to the formula : f^' (a)= a_min+(a-a_low)∙(a_max- a_min)/(a_high- a_low )################################
####define amax / amin 
amaxa = 255
amina = 0
####formula
jautocon = amina + (jgray - np.min(jgray))*(amaxa - amina)/(np.max(jgray) - np.min(jgray))

#modified contrast according to the formula#############################################
####defind amax / amin
aminm = 0
amaxm = 255
####defind q for finding alow / ahigh
#low value of q, the result image will mostly dark
q = 0.3
####calculate cumulative histogram for finding alow and ahigh for the formulation
jhistcu = plt.hist(jgray.ravel(),256,[0,256], cumulative = True)
##finding alow
index = 0 
for i in jhistcu[0]:
	if (i >= (np.size(jgray)*q)):
		alowm = index
		break
	index += 1
##finding ahigh
index = 0 
for i in jhistcu[0]:
	if (i >= (np.size(jgray)*(1-q))):
		ahighm = index-1
		break
	index += 1	
####formula	
jmodcon = aminm + (jgray - alowm)*(amaxm - aminm)/(ahighm - alowm)
u = 0
v = 0
while v <= 449:
	while u <= 363:
		if jgray[u][v] <= alowm:
			jmodcon[u][v] = aminm	
		elif jgray[u][v] >= ahighm:
			jmodcon[u][v] = amaxm
		u += 1		
	v += 1
	u = 0	

##########################################################################################
#show original image#####################################
cv2.imshow("jpeg",jgray)

#show result#############################################
####show contrast increasing result
plt.subplot(231), plt.imshow(jcontrast,'gray'), plt.title("contrast")

####show brightness increase result
plt.subplot(232), plt.imshow(jbright,'gray'), plt.title("brightness")

####show thresholding result
plt.subplot(233), plt.imshow(jthresh,'gray'), plt.title("threshold")

####show auto-contrast result
plt.subplot(234),plt.imshow(jautocon,'gray'), plt.title("auto-contrast")

####show modified contrast result
plt.subplot(235), plt.imshow(jmodcon, "gray"), plt.title("modified contrast")

####show inverting result
plt.subplot(236), plt.imshow(jinv,"gray"), plt.title("inverting")
plt.savefig("point operation.jpg")
plt.show()
