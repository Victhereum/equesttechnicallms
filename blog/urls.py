from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.urls import include



app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='bloghome'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
