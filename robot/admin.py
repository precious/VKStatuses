from rpk082.robot.models import Status
from rpk082.robot.models import Contact
from rpk082.robot.models import Profile
from rpk082.robot.models import Comment
from django.contrib import admin

class ContactInline(admin.TabularInline):
	model = Contact
	extra = 1

class ProfileAdmin(admin.ModelAdmin):
	fields = ['uid', 'name', 'email', 'password','cookie','cookie_date']
	list_display = ('uid', 'name', 'email', 'password','cookie','cookie_date')
	list_filter = ['name']
	search_fields = ['email']
#	fieldsets = (
#		('ID',	{'fields': ['uid', 'name']}),
#		('Login information',	{'fields': ['email', 'password'], 'classes': ['collapse']}),
#	)
#	inlines = [
#		ContactInline,
#	]

class StatusInline(admin.TabularInline):
	model = Status
	extra = 1

class ContactAdmin(admin.ModelAdmin):
	list_display = ('uid', 'name',)
	search_fields = ['name']
#	fieldsets = (
#		('ID',	{'fields': ['uid', 'name']}),
#	)
	inlines = [
		StatusInline,
	]

class StatusAdmin(admin.ModelAdmin):
	fields = ['text', 'date']
	list_display = ('text', 'date')
	list_filter = ['date']
	search_fields = ['text']
	date_hierarchy = 'date'

class CommentAdmin(admin.ModelAdmin):
	fields = ['text', 'date']
	list_display = ('text', 'date')
	list_filter = ['date']
	search_fields = ['text']
	date_hierarchy = 'date'


admin.site.register(Profile, ProfileAdmin)	
admin.site.register(Contact, ContactAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Comment, CommentAdmin)

