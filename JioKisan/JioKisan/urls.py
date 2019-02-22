from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paytm/', include('paytm.urls')),
    # path(r'^admin/', include(admin.site.urls)),
    path('new_reg/',views.new_registration, name='Speech to Text'),
    path('',views.ResponsePage,name='Response Page'),
    path('trade/',include('trade.urls')),
    path('stt/',views.speechtotext, name='Speech to Text'),
]
