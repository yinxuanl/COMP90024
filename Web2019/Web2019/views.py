from django.shortcuts import render
from django.views.generic import (TemplateView)

# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'index.html'


class TeamTemplateView(TemplateView):
    template_name = 'TeamMembers.html'

class MarvelTemplateView(TemplateView):
    template_name = 'Marvel.html'

class GOTTemplateView(TemplateView):
    template_name = 'got.html'