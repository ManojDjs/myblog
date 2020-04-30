from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
# from .views import SignupForm , index
from accounts import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^login_user',views.login_user, name='login_user'),
    url(r'^logout_user', views.logout_user, name='logout_user'),
    url(r'^index',views.index,name='index'),
    url(r'^register_user',views.register_user, name='register_user'),
    url(r'^profile',views.profile, name='profile'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)