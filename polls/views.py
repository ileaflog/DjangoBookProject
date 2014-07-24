from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Poll

# Create your views here.

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    return HttpResponse("Hello, world.  You're at the poll index.")

def detail(request, poll_id):
    return HttpResponse("You're looking at the details for poll %s" % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s" % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s" % poll_id)