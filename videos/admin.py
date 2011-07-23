from videos.models import Faq, Type, Tag, Association, Stream, Module, Video
from django.contrib import admin

########
#inlines
########
class VideoInline(admin.TabularInline):
	model=Video
	extra=4


#######
#admins
#######
class ModuleAdmin(admin.ModelAdmin):
	inlines=[VideoInline]
	search_fields=['module_title']
	list_display=('module_title','stream_titles')

class AssociationAdmin(admin.ModelAdmin):
	list_display=('association_stream_id', 'association_module_id', 'association_part')

class StreamAdmin(admin.ModelAdmin):
	list_display=('stream_title','stream_description','module_titles')

class VideoAdmin(admin.ModelAdmin):
	list_display=('module_title_part','video_url','video_type','video_tags')

class FaqAdmin(admin.ModelAdmin):
	list_display=('faq_question','faq_answer','faq_order')

admin.site.register(Faq, FaqAdmin)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(Association,AssociationAdmin)
admin.site.register(Stream,StreamAdmin)
admin.site.register(Module,ModuleAdmin)
admin.site.register(Video,VideoAdmin)
