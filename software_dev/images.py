import pysrt,os,csv
from decimal import Decimal
from math import sin, cos, sqrt, atan2, radians
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

R_earth = 6373.0 # radius of earth in km

def conv_2_deg(value):			# take the value of latitude/longitude in degrees,minutes and seconds and converts them to degrees
	d0 = value[0][0]	
	d1 = value[0][1]
	d  = float(d0)/float(d1)	# degrees

	m0 = value[1][0]
	m1 = value[1][1]
	m  = float(m0)/float(m1)	# minutes

	s0 = value[2][0]
	s1 = value[2][1]
	s  = float(s0)/float(s1)	# seconds

	return (d+m/60.0+s/3600.0)

def dist_points(lat1,lon1,lat2,lon2):	# computes the distance between two points given in latitude and longitude
	dlon = radians(lon2) - radians(lon1)
	dlat = radians(lat2) - radians(lat1)
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	dist = R_earth * c * 1000
	return dist # in m

video_path = '/home/mayank/Documents/Skylark_Drones_Tasks/software_dev/videos/DJI_0301.SRT'	# video_path(SRT) and its name
video = pysrt.open(video_path)									#opening the srt file
second_dist = 35 # in m
poi_dist = 50 # in m

img_list = os.listdir('images')									# assumed this file is kept just outside the image directory so that I can list inside image directory and get a list of files
img_cord = []											# list to store img name and their coordinates 

i = 0
for img in img_list:										# iterating over all the images
	try:
		img = Image.open('images/'+img)							#loading the image
		coor = [img_list[i]]								# storing the image name
		i = i+1
		info = img._getexif()								# getting meta data of image
		for tag,value in info.items():							# iterating over meta data
			decoded = TAGS.get(tag,tag)
			if decoded == 'GPSInfo':
				for v in value:
					sub_decoded = GPSTAGS.get(v,v)
					if sub_decoded == 'GPSLatitude' or sub_decoded == 'GPSLongitude':	# adding value of latitude and longitude
						coor.append(conv_2_deg(value[v]))
		img_cord.append(coor)								# adding image and its coordinates to the list
	except:
		pass
#print(img_cord[0])	
with open('images.csv', 'wb') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)				
	for frame in video:									# iterating over video frames
		lat_lon = frame.text.split(',')							# seperating time of frame, latitude and longitude
		list_img = [frame.start]							# frame start time
		imgs = []									# list to store images within 35m of this frame
		for iter in img_cord:								# iterating over images
			#print dist_points(Decimal(lat_lon[1]),Decimal(lat_lon[0]),iter[1],iter[2])
			if (dist_points(Decimal(lat_lon[1]),Decimal(lat_lon[0]),iter[1],iter[2])<=35):
				imgs.append(iter[0])
		list_img.append(imgs)
		wr.writerow(list_img)								# writing the frame start and corresponding images to csv file
