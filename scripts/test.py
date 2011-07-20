
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from videos.models import Stream, Video, Association, Module

video=Video.objects.filter(pk=38)[0]

stream_module=video.next_video_in_stream()
print stream_module[0].module_count()
print stream_module[0]
print stream_module[1]

#if (stream_module):

#	next_association=Association.objects.filter(association_stream_id=stream_module[0],association_part=stream_module[1])[0]
#	next_video=next_association.association_module_id.video_set.all()[0].pk
			
#	print next_video
