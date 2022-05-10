from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import IssueViewSet, ProjectViewSet, RegisterView, ContributorViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'users', ContributorViewSet, basename='users')
project_router.register(r'issues', IssueViewSet, basename='issues')

issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', RegisterView.as_view(),),   
    path('login/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    path('',include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]