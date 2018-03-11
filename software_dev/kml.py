import pysrt,simplekml,csv

video_path = '/home/mayank/Documents/Skylark_Drones_Tasks/software_dev/videos/DJI_0301.SRT'	# video_path(SRT) and its name
video = pysrt.open(video_path)	

kml=simplekml.Kml()

for frame in video:
	lat_lon = frame.text.split(',')					# seperating time of frame, latitude and longitude
	kml.newpoint(name = str(frame.start), coords = [(lat_lon[0],lat_lon[1])])

kml.save('drone.kml')