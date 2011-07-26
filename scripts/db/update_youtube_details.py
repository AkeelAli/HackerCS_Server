import MySQLdb
import gdata.youtube
import gdata.youtube.service
import re

yt_service=gdata.youtube.service.YouTubeService()

#videos dictionary holding the tuples read at the beginning from the database
videos={}
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django.db import connection
cursor = connection.cursor()

cursor.execute ("SELECT id, video_url FROM videos_video")
while(1):
	row = cursor.fetchone ()
	if row==None:
		break
	videos[row[0]]=row[1]	

#update video details
for id in videos:
	#get video_id
	match=re.search("v=(.*)$",videos[id])
	if match:
		vid=match.group(1)
		entry=yt_service.GetYouTubeVideoEntry(video_id=vid)
		secs=int(entry.media.duration.seconds)
		
		#other info
		if (entry.rating):
			rating=entry.rating.average
			raters=entry.rating.num_raters
		else:
			rating='null'
			raters='null'
		views=entry.statistics.view_count
		published=entry.published.text
		description=entry.media.description.text
		
		lengthStr=str(secs/60)+":%02d" % (secs%60)
		
		if (rating=='null'):
			cursor.execute("""
				UPDATE videos_video SET video_length=%s,
				video_rating=null,video_raters=null,video_views=%s,video_published=%s,
				video_description=%s WHERE id=%s
				""",
				(lengthStr, views, published, description, id)
			)		
		else:
			cursor.execute("""
				UPDATE videos_video SET video_length=%s,
				video_rating=%s,video_raters=%s,video_views=%s,video_published=%s,
				video_description=%s WHERE id=%s
				""",
				(lengthStr,rating, raters, views, published, description, id)
			)
			
		

#update stream length
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from videos.models import Stream, Video, Association, Module

for stream in Stream.objects.all():
	length_strs=[]
	time=0
	for association in stream.association_set.all():
		module=association.association_module_id
		for video in module.video_set.all():
			length_strs.append(video.video_length)
		
	for string in length_strs:
		match=re.match(r'^(\d+):(\d+)$',string)
		time=time+int(match.group(1))*60
		time=time+int(match.group(2))
	
	if (time/3600>0):
		hrs=time/3600
		mins=(time%3600)/60
		secs=(time%3600)%60
		stream.stream_length=( str(hrs)+":%02d:%02d" % (mins,secs)  )	
	else:
		stream.stream_length=(str(time/60)+":%02d" % (time%60))
	
	stream.save()

#update module info	
for module in Module.objects.all():
	total_views=0
	total_raters=0
	#to calculate new avg rating
	total_rating=0
	rating_counts=0
	
	for video in module.video_set.all():
		total_views=total_views+int(video.video_views)
		if (video.video_rating):
			total_rating=total_rating+float(video.video_rating)
			total_raters=total_raters+int(video.video_raters)
			rating_counts=rating_counts+1
	
	module.module_views=str(total_views)
	if (total_raters!=0):
		module.module_raters=str(total_raters)
		module.module_rating=str(total_rating/rating_counts)
	else:
		module.module_raters=None
		module.module_rating=None
	#just take any date
	if (module.video_set.all()):
		module.module_published=module.video_set.all()[0].video_published
	
	module.save()

cursor.close ()
