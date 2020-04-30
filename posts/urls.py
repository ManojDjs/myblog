from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    MyCreateView)
from posts import views
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^posts', views.posts, name='posts'),
    url(r'^statistics',views.statistics,name='statistics'),
    url(r'^newplotly', views.newplotly, name='newplotly'),
    url(r'^code',views.code,name='code'),
    url(r'^scan',views.scan,name='scan'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('postslist/',PostListView.as_view(),name='posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    url(r'^loc', MyCreateView.as_view(), name='loc'),

]

urlpatterns += staticfiles_urlpatterns()
