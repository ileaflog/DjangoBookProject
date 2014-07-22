from django.contrib import admin
from polls.models import Poll, Choice

# Create meta models
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    search_fields = ['question']
    list_filter = ['pub_date']
    list_display = ('question', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question', 'priority']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

# Register your models here.
admin.site.register(Poll, PollAdmin)
