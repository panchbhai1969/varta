
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trade/',include('trade.urls')),
    path('',views.ResponsePage,name='Response Page'),
    path('stt/',views.speechtotext, name='Speech to Text'),
    path('new_reg/',views.new_registration, name='Speech to Text'),
]
