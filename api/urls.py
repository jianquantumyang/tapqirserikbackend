from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('chat/',views.chat),
    path('image/generate/',views.gen_image),
    path('audio/tts/',views.tts)
]
