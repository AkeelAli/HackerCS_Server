from django.db import models
from django.contrib.auth.models import User
import re


class Tag(models.Model):
	tag_title=models.CharField(max_length=200)

	def __unicode__(self):
		return self.tag_title

class Type(models.Model):
	type_title=models.CharField(max_length=200)

	def __unicode__(self):
		return self.type_title

class Stream(models.Model):
	stream_title=models.CharField(max_length=200)
	stream_description=models.TextField(null=True, blank=True)
	stream_length=models.CharField(max_length=10, null=True, blank=True)
	
	def __unicode__(self):
		return self.stream_title
	
	def module_count(self):
		return len(self.association_set.all())
	
	def module_titles(self):
		module_titles=[]
		for association in self.association_set.all():
			module=association.association_module_id.module_title
			module_titles.append(module)
		return '<br /> '.join(module_titles)
	module_titles.allow_tags=True

	def url_friendly(self):
		import re
		return "%s" % re.sub('\W+','-',self.stream_title)
	
class Module(models.Model):
	module_associations=models.ManyToManyField(Stream, through='Association')
	module_prereqs=models.ManyToManyField("self", symmetrical=False, blank=True, null=True)

	module_title=models.CharField(max_length=200)
	module_description=models.TextField(null=True, blank=True)
	module_rating=models.CharField(max_length=15, blank=True, null=True)
	module_raters=models.CharField(max_length=15, blank=True, null=True)
	module_views=models.CharField(max_length=15, blank=True, null=True)
	module_published=models.CharField(max_length=50, blank=True, null=True)
	
	def __unicode__(self):
		return self.module_title

	def video_count(self):
		return len(self.video_set.all())

	def stream_titles(self):
		stream_titles=[]
		for association in self.association_set.all():
			stream=association.association_stream_id.stream_title
			stream_titles.append(stream)
		return ', '.join(stream_titles)

class Association(models.Model):
	association_stream_id=models.ForeignKey(Stream)
	association_module_id=models.ForeignKey(Module)
	association_part=models.DecimalField(max_digits=5,decimal_places=2)

	def __unicode__(self):
		return "%s: %s (%d)" % (self.association_stream_id.stream_title, self.association_module_id.module_title, self.association_part)


		
class Video(models.Model):
	module_id=models.ForeignKey(Module)
	video_type=models.ForeignKey(Type, null=True, blank=True)
	video_tag=models.ManyToManyField(Tag, blank=True, null=True)

	video_url=models.CharField(max_length=200)
	video_title=models.CharField(max_length=200, blank=True)
	video_part=models.IntegerField()
	video_length=models.CharField(max_length=10, blank=True, null=True)
	video_rating=models.CharField(max_length=15, blank=True, null=True)
	video_raters=models.CharField(max_length=15, blank=True, null=True)
	video_views=models.CharField(max_length=15, blank=True, null=True)
	video_published=models.CharField(max_length=50, blank=True, null=True)
	video_description=models.TextField(null=True, blank=True)
	
	def __unicode__(self):
		return "%s" % self.module_id.module_title + " ("+str(self.video_part)+"/"+str(len(self.module_id.video_set.all()))+")"

	def url_friendly(self):
		import re
		return "%s" % re.sub('\W+','-',self.module_id.module_title) + "-Part-"+str(self.video_part)
		
		
	def module_title_part(self):
		return "%s" % self.module_id.module_title + " ("+str(self.video_part)+"/"+str(len(self.module_id.video_set.all()))+")"
	
	def video_youtube_id(self):
		import re
		match=re.search("v=(.*)$",self.video_url)
		if match:
			return match.group(1)
		else:
			return ''

	def next_video_in_stream(self):
		module=self.module_id
		#even though for loop, current assumptions is that there is only 1 association per module
		for association in module.association_set.all():
			stream=association.association_stream_id
			stream_parts=stream.module_count()
			module_part=association.association_part
			if (module_part<stream_parts):
				l=[stream,module_part+1]
				return l
			else:
				return False
		
		return False
		
	def video_tags(self):
		tags=[]
		for tag in self.video_tag.all():
			tags.append(tag.tag_title)
		return ', '.join(tags)
		
class Faq(models.Model):
	faq_question=models.CharField(max_length=200)
	faq_answer=models.TextField(null=True, blank=True)
	faq_order=models.IntegerField()

	def __unicode__(self):
		return self.faq_question

class UserProfile(models.Model):
	user=models.ForeignKey(User,unique=True)
	completed_videos=models.ManyToManyField(Video, blank=True, null=True)
	
	FORMAT_CHOICES=(
		('H','HTML5'),
		('F','FLASH'),
	)
	format=models.CharField(max_length=1,choices=FORMAT_CHOICES,default='F')

	def get_absolute_url(self):
		return ('profiles_profile_detail', (), { 'username': self.user.username })
	get_absolute_url = models.permalink(get_absolute_url)
