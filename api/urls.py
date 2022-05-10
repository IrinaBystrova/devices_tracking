from api.views import ReleaseApiView
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api', ReleaseApiView, basename='api')
urlpatterns = [path('', include(router.urls))]
