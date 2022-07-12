from . import views
from django.urls import path
from django.urls import include



app_name = 'videos'

urlpatterns = [
    path('', views.VideoList.as_view(), name='videohome'),
    path('<slug:slug>/', views.video_detail, name='video_detail'),
]
