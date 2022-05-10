from .models import Comment, Contributor, Project, Issue
from .serializers import ProjectSerializer, RegisterSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer