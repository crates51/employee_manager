from django.urls import path, include
from app import urls as employee_urls
from rest_framework import routers
from app.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('employee/', include(employee_urls)),
]
