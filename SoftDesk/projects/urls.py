from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProjectViewSet, RegisterView


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    path('signup/', RegisterView.as_view(),),
]