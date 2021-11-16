from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RemitoViewSet
from django.urls.conf import include

router = DefaultRouter()
router.register(r'remitos', RemitoViewSet, basename='remitos')

urlpatterns = [
    path('api/', include(router.urls)),
]