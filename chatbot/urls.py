from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('chatbot/', homeBot, name='chatbot'),
    path('new-chat/', newChat, name='newChat'),
    path('chat/<str:search>/', loadChat, name='loadChat'),
]
