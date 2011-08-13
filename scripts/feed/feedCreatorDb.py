import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'

from django.db import connection
from videos.models import Video

#todo later
def rss_time_now():
	from datetime import datetime
	now=datetime.now()
	return now


cursor = connection.cursor()

cursor.execute("SELECT id, video_title, video_description, video_published, video_url FROM videos_video WHERE video_part='1' ORDER BY video_published DESC")

rows=cursor.fetchall()

f=open('/home2/akeelali/public_html/hackercs/static/feed.rss','w')

header="""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>

<title>Hacker CS - New Modules RSS Feed</title>
<link>http://www.hackercs.com/</link>
<description>Hacker CS is a free online database of Computer Science video tutorials.</description>
<language>en-us</language>
""" 

body=""

for row in rows:
	video=Video.objects.get(pk=row[0])
	
	item="""
	<item>
	<title>%s</title>
	<description>%s</description>
	<link>%s</link>
	</item>
	""" % (video.module_id.module_title,row[2],"http://hackercs.com/videos/"+video.url_friendly())

	body+=item

footer="""
</channel>
</rss>
"""


f.write(header)
f.write(body)
f.write(footer)

f.close()
