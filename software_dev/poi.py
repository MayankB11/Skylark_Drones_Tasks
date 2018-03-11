import pysrt,os,csv
from decimal import Decimal
from math import sin, cos, sqrt, atan2, radians
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

R_earth = 6373.0 # radius of earth in km

def conv_2_deg(value):
	d0 = value[0][0]
	d1 = value[0][1]
	d  = float(d0)/float(d1)

	m0 = value[1][0]
	m1 = value[1][1]
	m  = float(m0)/float(m1)

	s0 = value[2][0]
	s1 = value[2][1]
	s  = float(s0)/float(s1)

	return (d+m/60.0+s/3600.0)

def dist_points(lat1,lon1,lat2,lon2):
	dlon = radians(lon2) - radians(lon1)
	dlat = radians(lat2) - radians(lat1)
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	dist = R_earth * c * 1000
	return dist # in m

video = pysrt.open('/home/mayank/Documents/Skylark_Drones_Tasks/software_dev/videos/DJI_0301.SRT',encoding='iso-8859-1')
second_dist = 35 # in m
poi_dist = 50 # in m

img_list = os.listdir('images')
img_cord = []

i = 0
for img in img_list:
	try:
		img = Image.open('images/'+img)
		coor = [img_list[i]]
		i = i+1
		info = img._getexif()
		for tag,value in info.items():
			decoded = TAGS.get(tag,tag)
			if decoded == 'GPSInfo':
				for v in value:
					sub_decoded = GPSTAGS.get(v,v)
					if sub_decoded == 'GPSLatitude' or sub_decoded == 'GPSLongitude':
						coor.append(conv_2_deg(value[v]))
		img_cord.append(coor)
	except:
		pass
#print(img_cord[0])	
write = []	
with open('assets.csv') as assets:
	reader = csv.DictReader(assets)			
	for row in reader:
		img_names = []
		for iter in img_cord:
			#print dist_points(Decimal(lat_lon[1]),Decimal(lat_lon[0]),iter[1],iter[2])
			if (dist_points(Decimal(row['latitude']),Decimal(row['longitude']),iter[1],iter[2])<=50):
				img_names.append(iter[0])
		row['image_names'] = img_names
		print(row)
		write.append(row)

with open('assets.csv','w') as assets:
	wr = csv.writer(assets)	
	len(write)
	field_names = write[0].keys()
	wr.writerow(field_names)
	for row in write:
		val = []
		for key,value in row.items():
			val.append(value)
		wr.writerow(val)
assets.close()
