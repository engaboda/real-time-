from django.urls import path

from . import views

app_name = 'like'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.update, name='update'),
    path('signup/', views.signup, name='signup'),
    path('counter/', views.counter, name='users'),
]