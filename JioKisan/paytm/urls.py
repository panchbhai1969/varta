from django.conf.urls import include, url
from django.urls import include, path
from . import views

urlpatterns = [
    # Examples:
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    path('response/', views.response, name='response'),
    path('responses', views.responses, name = 'responses')
]
