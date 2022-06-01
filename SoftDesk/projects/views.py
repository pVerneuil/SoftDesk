from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from .models import Comments, Contributor, Project, Issue
from .serializers import RegisterSerializer, ContributorSerializer, IssueSerializer, CommentSerializer, ProjectSerializer
from .permission import IsContributorOrAuthorPermission

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
# TODO faire en sorte que user id soit rempli par request.user (search perform_create?)
        # return chain(projects_user_is_contibutor_of, Project.objects.filter(author_user_id=self.request.user))
#! https://github.com/alanjds/drf-nested-routers/blob/master/README.md solve the urls problem
class ProjectViewSet(ModelViewSet):
    permission_classes = [ IsContributorOrAuthorPermission,]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def list(self, request, ):
        queryset = Project.objects.filter()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.filter()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(client)
        return Response(serializer.data)


class ContributorViewSet(ModelViewSet):


    serializer_class = ContributorSerializer
    
    def list(self, request, projects_pk=None):
        queryset = Contributor.objects.filter(project_id=projects_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, projects_pk=None):
        queryset = Contributor.objects.filter(pk=pk, project_id=projects_pk)
        contributors = get_object_or_404(queryset, pk=pk)
        serializer = ContributorSerializer(contributors)
        return Response(serializer.data)


class IssueViewSet(ModelViewSet):

    permission_classes = [IsContributorOrAuthorPermission]
    serializer_class = IssueSerializer
    
    def list(self, request, projects_pk=None):
        queryset = Issue.objects.filter(project_id=projects_pk)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, projects_pk=None):
        queryset = Issue.objects.filter(pk=pk, project_id=projects_pk)
        issues = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(issues)
        return Response(serializer.data)

class CommentViewSet(ModelViewSet): #!verify issue_id_id
    permission_classes = [IsContributorOrAuthorPermission]
    serializer_class = CommentSerializer 
    
    def list(self, request, projects_pk=None, issue_pk=None):
        queryset = Comments.objects.filter(issue_id_id=projects_pk, issue_id=issue_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, projects_pk=None, issue_pk=None):
        queryset = Comments.objects.filter(pk=pk, issue_id=issue_pk, issue_id_id=projects_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
