from django.contrib import admin
from django.urls import include, path
from . import views
from . import voice

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_page'),
    path('paytm/', include('paytm.urls')),
    #path(r'^admin/', include(admin.site.urls)),
    path('new_reg/',views.new_registration, name='NewRegistrations'),
    path('otp_check/',views.otp_check, name='CheckingOTP'),
    path('login/',views.login, name='NewRegistrations'),
    path('login_check/',views.login_check, name='CheckingOTP'),
    path('',views.ResponsePage,name='Response Page'),
    path('trade/',include('trade.urls')),
    path('stt/',views.speechtotext, name='Speech to Text'),
    path('upload/',views.voice_input, name='upload'),
]
