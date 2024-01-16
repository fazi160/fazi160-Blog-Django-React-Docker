from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import PasswordGenerator
# router= DefaultRouter()
# router.register(r'', PasswordGenerator, basename='password')

urlpatterns = [
    # path('', include(router.urls)),
    path('', PasswordGenerator.as_view(), name='password')
]
