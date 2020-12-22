from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('hello-view/', views.HelloApiView.as_view(), name='helloApiView'),
    path('SensorApiView/', views.SensorApiView.as_view(), name='SensorApiView'),
    path('SensorAccApiView/', views.SensorAccApiView.as_view(), name='SensorAccApiView'),
    path('SensorGyroApiView/', views.SensorGyroApiView.as_view(), name='SensorGyroApiView')
]