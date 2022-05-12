from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics

from django.contrib.auth.models import User
from .models import Comments, Contributor, Project, Issue
from .serializers import RegisterSerializer, ContributorSerializer, IssueSerializer, CommentSerializer, ProjectSerializer

from .permission import IsContributorPermission

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
# TODO faire en sorte que user id soit rempli par request.user (searchperform_create?)
class ProjectViewSet(ModelViewSet):
    permission_classes = [ IsContributorPermission]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ContributorViewSet(ModelViewSet):
    # TODO: permissions: read/write&delete 
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class IssueViewSet(ModelViewSet):
    permission_classes = [IsContributorPermission]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class CommentViewSet(ModelViewSet):
    permission_classes = [IsContributorPermission]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer