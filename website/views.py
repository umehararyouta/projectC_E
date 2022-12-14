from multiprocessing import context
from pipes import Template
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from itertools import count
from pickle import APPEND
from tkinter.tix import TCL_WINDOW_EVENTS
from unittest import result
import tweepy
import pandas as pd
import numpy as np
import re
import MeCab
import csv
import time

from website.TwitterAPIreply import Twitter
from website.TwitterAPIreply import negapozi


pd.set_option('display.unicode.east_asian_width', True)

class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        Username = request.POST['name']
        Searchcount = request.POST['searchcount']
        total_score = Twitter(Username,Searchcount)
        negapozi_word = negapozi(negapozi_score=total_score)
        context = {
            'name':Username,
            'searchcount':Searchcount,
            'message':negapozi_word,
            'negapozi':total_score
        }
        if 'loop' in request.POST:
            return render(request,'loop.html',context)
        elif 'notloop' in request.POST:
            return render(request,'notloop.html',context)

class LoopView(TemplateView):
    template_name = 'loop.html'

    def get(self, request, *args, **kwargs):
        Username = request.POST['name']
        Searchcount = request.POST['searchcount']
        total_score = Twitter(Username,Searchcount)
        negapozi_word = negapozi(negapozi_score=total_score)
        context = {
            'name':Username,
            'searchcount':Searchcount,
            'message':negapozi_word,
            'negapozi':total_score
        }
        return 'loop.html'

class NotLoopView(TemplateView):
    template_name = 'notloop.html'

class AccessView(TemplateView):
    template_name = 'access.html'

class CareView(TemplateView):
    template_name = 'care.html'

class FireView(TemplateView):
    template_name = 'fire.html'

class SystemView(TemplateView):
    template_name = 'system.html'
    
class HowtouseView(TemplateView):
    template_name = 'howtouse.html'
# Create your views here.
