from django.urls import path, include
from rest_framework.routers import DefaultRouter

from freelance.advert import views

router = DefaultRouter()
router.register(r'advert', views.AdvertViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]