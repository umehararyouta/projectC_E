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
        Loopyn = request.POST.get(' loopyn ')
        print(Loopyn)
        if not Loopyn == True:
            total_score = Twitter(Username,Searchcount)
        else:
            
            total_score = Twitter(Username,Searchcount)
                # time.sleep(10)
        negapozi_word = negapozi(negapozi_score=total_score)
        context = {
            'name':Username,
            'searchcount':Searchcount,
            'message':negapozi_word,
            'negapozi':total_score
        }
        
        return render(request,'index.html',context)
    


# Create your views here.
