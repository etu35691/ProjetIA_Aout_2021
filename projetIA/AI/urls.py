from django.urls import path

from AI import views

urlpatterns = [
    path('train', views.train)    
]