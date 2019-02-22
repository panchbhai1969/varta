# from django.urls import path,include
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('buy',views.BuyPage,name='BuyPage'),
    url('sell',views.SellPage,name='SellPage'),
    url('',views.TradePage,name='TradePage'),
]
