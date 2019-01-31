from django.urls import path
from . import views

app_name = 'dialogflow'

urlpatterns = [
    path('', views.index, name='index'),
    path('fulfillment/', views.fulfillment, name='fulfillment'),
    path('aduino/ksy', views.aduino_ksy, name='aduino_ksy'),
    path('aduino/yhc', views.aduino_yhc, name='aduino_yhc'),
    path('aduino/kkh', views.aduino_kkh, name='aduino_kkh'),
    path('message/ksy', views.message_ksy, name='message_ksy'),
    path('message/yhc', views.message_yhc, name='message_yhc'),
    path('message/kkh', views.message_kkh, name='message_kkh'),
]