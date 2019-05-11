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

from django.conf.urls import url
from . import views

app_name = 'Web2019'

urlpatterns = [
    url(r'^$', views.HomeTemplateView.as_view(), name='home_page'),

    url(r'^contactinfo/$', views.TeamTemplateView.as_view(), name='contact_info'),

    url(r'^marvel/$', views.MarvelTemplateView.as_view(), name='analysis_marvel'),

    url(r'^gameofthrones/$', views.GOTTemplateView.as_view(), name='analysis_gameOfThrones'),
]
