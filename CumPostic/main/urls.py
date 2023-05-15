from django.urls import path, re_path, include
from . import views
from .views import Register

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('type/<slug:url>/', views.index_type, name='index_type'),
    path('category/<slug:url>/', views.index_category, name='index_category'),
    re_path(r'^post/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.post, name='post'),
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
]