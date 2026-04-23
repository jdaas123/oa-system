from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.urls import path
app_name = 'inform'

router = DefaultRouter(trailing_slash=False)
# router = DefaultRouter()

router.register('inform',InformViewSet,basename='inform')

urlpatterns = [
    path('inform/read',ReadInformView.as_view(),name= "inform_read")
] + router.urls