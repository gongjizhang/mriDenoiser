#This file holds all utility functions that might be used in multiple scripts
#It also contains any global constants like the segment size, filter size, number of filters, ect.
#This file may not be used if it is more convient to store variables within their respective classes
import glob
import cv2
import nibabel as nib
import pdb
import numpy as np

segmentHeight = 13
segmentWidth = 13

def loadImages(imagesDirectory, isMNC=True):
	#load images from directory
	images = []
	if isMNC:
		for file in glob.glob(imagesDirectory+'/*.mnc'):
			mnc = nib.load(file)
			data = mnc.get_data()
			data = data/np.std(data) #normalize
			for image in data:
				segments = segmentImage(image)
				images.extend(segments)

	else:
		for file in glob.glob(imagesDirectory+'/*.jpg'):
			image = cv2.imread(file)
			grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			images.append(grayImage)
	return images

def loadImagesAsSegments(imagesDirectory, isMNC=True):
	#load images from directory
	images = []
	if isMNC:
		for file in glob.glob(imagesDirectory+'/*.mnc'):
			mnc = nib.load(file)
			data = mnc.get_data()
			data = data/np.std(data) #normalize
			for image in data:
				segments = segmentImage(image)
				images.extend(segments)
				

	else:
		for file in glob.glob(imagesDirectory+'/*.jpg'):
			image = cv2.imread(file)
			grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			segments = segmentImage(grayImage)
			images.extend(segments)
	return images


def segmentImage(image):
	#divide images into small segments 
	#return segments
	assert(image.shape[0] >= segmentHeight)
	assert(image.shape[1] >= segmentWidth)
	numSegY = image.shape[0]/segmentHeight
	numSegX = image.shape[1]/segmentWidth
	segments = []
	for j in range(0, numSegY*segmentHeight, segmentHeight):
		for i in range(0, numSegX*segmentWidth, segmentWidth):
			segments.append(image[j:j+segmentHeight, i:i+segmentWidth])
	return segments

def batch(iterable, batchSize=1):
    l = len(iterable)
    for ndx in range(0, l, batchSize):
        yield iterable[ndx:min(ndx + batchSize, l)]