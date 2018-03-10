from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS

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

img_path = '/home/mayank/Documents/Skylark_Drones_Tasks/software_dev/images/'
img = Image.open(img_path+'DJI_0375.JPG')
info = img._getexif()
exif_date = {}
for tag,value in info.items():
	decoded = TAGS.get(tag,tag)
	if decoded == 'GPSInfo':
		for v in value:
			sub_decoded = GPSTAGS.get(v,v)
			if sub_decoded == 'GPSLatitude' or sub_decoded == 'GPSLongitude':
				print sub_decoded,conv_2_deg(value[v])
				