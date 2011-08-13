import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'

from django.db import connection
from videos.models import Video
import datetime
import re

def format_date(dt):
    """convert a datetime into an RFC 822 formatted date

    """
    # Looks like:
    #   Sat, 07 Sep 2002 00:00:01 GMT
    # Can't use strftime because that's locale dependent
    #
    # Isn't there a standard way to do this for Python?  The
    # rfc822 and email.Utils modules assume a timestamp.  The
    # following is based on the rfc822 module.
    return "%s, %02d %s %04d %02d:%02d:%02d EST" % (
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
            dt.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month-1],
            dt.year, dt.hour, dt.minute, dt.second)

cursor = connection.cursor()

cursor.execute("SELECT id, video_title, video_description, video_published, video_url FROM videos_video WHERE video_part='1' ORDER BY video_published DESC")

rows=cursor.fetchall()


header="""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>

<title>Hacker CS - New Modules RSS Feed</title>
<link>http://www.hackercs.com/</link>
<description>Hacker CS is a free online database of Computer Science video tutorials.</description>
<lastBuildDate>%s</lastBuildDate>
<language>en-us</language>
""" % format_date(datetime.datetime.now())

body=""

for row in rows:
	video=Video.objects.get(pk=row[0])
	#get date
	match=re.match('(\d+)-(\d+)-(\d+)',row[3])
	published=datetime.datetime(int(match.group(1)),int(match.group(2)),int(match.group(3)),0,0,0)
	
	link="http://hackercs.com/videos/"+video.url_friendly()

	item="""
	<item>
	<title>%s</title>
	<description>%s</description>
	<link>%s</link>
	<guid isPermaLink="true">%s</guid>
	<pubDate>%s</pubDate>
	</item>
	""" % (video.module_id.module_title,row[2],link,link, format_date(published))

	body+=item

footer="""
</channel>
</rss>
"""


#only write at the end in case the script fails anywhere above
f=open('/home2/akeelali/public_html/hackercs/static/feed.rss','w')

f.write(header)
f.write(body)
f.write(footer)

f.close()
