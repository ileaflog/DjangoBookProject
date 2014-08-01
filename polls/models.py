import datetime
from django.db import models
from django.utils import timezone
# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    priority = models.BooleanField()
    #
    def __unicode__(self):
        return self.question
    #
    def was_published_recently(self):
        result = False

        now = timezone.now()
        if (self.pub_date >= now - datetime.timedelta(days=1) and
            self.pub_date <= now):
            result = True

        return result

    #
    # What does this dot notation mean?  Do methods really have fields/attributes?
    #
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    #
    def __unicode__(self):
        return self.choice_text
