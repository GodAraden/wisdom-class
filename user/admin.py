from django.contrib import admin
from .models import User,TeacherPhone

class TeacherPhoneManager(admin.ModelAdmin):
    list_display = ['phone','used']
    list_display_links = ['phone']
    list_filter = ['used']
    search_fields = ['phone']

admin.site.register(User)
admin.site.register(TeacherPhone,TeacherPhoneManager)
