from django.urls import path

from .import views
from .views import *
from MainApp import views

urlpatterns = [
    path('home',views.new,name="h"),
    path('',views.addusers,name="add"),
    path('login',views.userlogin,name="log"),
    path('login1',views.adminlogin,name="login1"),
    path('d1',views.dashboard1,name="dh1"),
    path('adc',views.addcategory,name='adct'),
    path('addcate',views.addcate,name="categ"),
    path('addprod',views.addprogram,name="pro"),
    path('cat',views.cate,name="cate"),
    path('addp',views.getprogram,name="get"),
    path('del<int:userid>',views.delpro,name="del"),
    path('edit<int:userid>',views.update_pro,name="upd"),
    path('user',views.viewuser,name="vuser"),
    path('pur',views.purch,name="pur"),
    path('categor',views.viewcate,name="ca"),
    path('sub<int:pid>,<int:uid>',views.sub,name="sub"),

    
    path('act<int:catid>',views.act,name="acti"),

    path('ord',views.orders,name="ord"),
      
]