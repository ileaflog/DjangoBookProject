from django.contrib import admin
from polls.models import Poll, Choice

# Create meta models
class PollAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question']
    fieldsets = [
        (None, {'fields': ['question', 'priority']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

# Register your models here.
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)