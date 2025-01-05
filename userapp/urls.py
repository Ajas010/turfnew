from django.urls import path

from userapp.views import *
app_name = 'userapp'
urlpatterns = [
    path('', UserLogin.as_view(), name='userlogin'),
    path('adminhome/', Adminhomeload.as_view(), name='loadadmin'),
    path('loginapi/',UserLoginapi.as_view(),name='userloginapi'),

]
 