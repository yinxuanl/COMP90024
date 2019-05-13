"""Web2019 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import url
from . import views

app_name = 'Web2019'

urlpatterns = [
    url(r'^$', views.HomeTemplateView.as_view(), name='home_page'),

    url(r'^contactinfo/$', views.TeamTemplateView.as_view(), name='contact_info'),

    url(r'^marvel_topic1/$', views.MarvelTemplateView1.as_view(), name='analysis_marvel_user'),

    url(r'^marvel_topic2/$', views.MarvelTemplateView2.as_view(), name='analysis_marvel_year'),

    url(r'^marvel_topic1/marveluser.html$', views.MarvelPicture1.as_view(), name='analysis_marvel_user_picture'),

    url(r'^marvel_topic2/marvelyear.html$', views.MarvelPicture2.as_view(), name='analysis_marvel_year_picture'),

    url(r'^got_topic1/$', views.GotTemplateView1.as_view(), name='analysis_gameOfThrones_user'),

    url(r'^got_topic2/$', views.GotTemplateView2.as_view(), name='analysis_gameOfThrones_month'),

    url(r'^got_topic1/gotuser.html$', views.GotPicture1.as_view(), name='analysis_gameOfThrones_user_picture'),

    url(r'^got_topic2/gotmonth.html$', views.GotPicture2.as_view(), name='analysis_gameOfThrones_month_picture'),

]

urlpatterns += staticfiles_urlpatterns()
