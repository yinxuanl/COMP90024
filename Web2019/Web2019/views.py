from django.shortcuts import render
from django.views.generic import (TemplateView)

# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'index.html'

class TeamTemplateView(TemplateView):
    template_name = 'TeamMembers.html'

class MarvelTemplateView1(TemplateView):
    template_name = 'Marvel.html'

class MarvelTemplateView2(TemplateView):
    template_name = 'Marvel2.html'

class GotTemplateView1(TemplateView):
    template_name = 'got.html'

class GotTemplateView2(TemplateView):
    template_name = 'got2.html'

class MarvelPicture1(TemplateView):
    template_name = 'marveluser.html'

class MarvelPicture2(TemplateView):
    template_name = 'marvelyear.html'

class GotPicture1(TemplateView):
    template_name = 'gotuser.html'

class GotPicture2(TemplateView):
    template_name = 'gotmonth.html'