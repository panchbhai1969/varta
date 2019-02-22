from django.contrib import admin
# from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^paytm/', include('paytm.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^new_reg/',views.new_registration, name='Speech to Text'),
    # url(r'^$',views.ResponsePage,name='Response Page'),
    # url(r'^trade/',include('trade.urls')),
    # url(r'^stt/',views.speechtotext, name='Speech to Text'),

]
