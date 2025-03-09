from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'users'

#Creating router
router = DefaultRouter()
#registering each viewsets with a route




urlpatterns = [
    path('', include(router.urls)),
    
    
]