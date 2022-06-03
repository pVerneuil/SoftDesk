from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from .models import Comment, Contributor, Project, Issue
from .serializers import (
    RegisterSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
    ProjectSerializer,
)
from .permission import IsContributorOrAuthorPermission, ContributorsPermission


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectViewSet(ModelViewSet):
    permission_classes = [
        IsContributorOrAuthorPermission,
    ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        serializer = ProjectSerializer(context={"request": request}, data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            contributor = Contributor(
                user=self.request.user,
                project=Project.objects.last(),
                permissions="manager",
                role="Project Manager",
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [
        ContributorsPermission,
    ]

    def list(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Contributor.objects.filter(project=project_pk)
        serializer = ContributorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = ContributorSerializer(
            data=request.data, context={"request": request, "project": project_pk}
        )
        if serializer.is_valid():
            serializer.save(project=Project.objects.get(pk=project_pk))
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Contributor.objects.filter(pk=pk, project=project_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(ModelViewSet):

    permission_classes = [IsContributorOrAuthorPermission]
    serializer_class = IssueSerializer

    def list(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Issue.objects.filter(project=project_pk)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = IssueSerializer(
            data=request.data, context={"request": request, "project": project_pk}
        )
        if serializer.is_valid():
            serializer.save(
                author=self.request.user, project=Project.objects.get(pk=project_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(
            issue,
            data=request.data,
            context={"request": request, "project": project_pk},
        )
        if serializer.is_valid():
            serializer.save(
                author=self.request.user, project=Project.objects.get(pk=project_pk)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Issue.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        comments = Comment.objects.filter(issue=pk)
        self.check_object_permissions(request, issue)
        issue.delete()
        for comment in comments:
            comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    permission_classes = [IsContributorOrAuthorPermission]
    serializer_class = CommentSerializer

    def list(self, request, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(pk=issue_pk, project=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Comment.objects.filter(issue__project=project_pk, issue=issue_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(
            pk=pk, issue__project=project_pk, issue=issue_pk
        )
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(pk=issue_pk, project=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        project = Project.objects.get(pk=project_pk)
        self.check_object_permissions(request, project)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user, issue=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(pk=issue_pk, project=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment = get_object_or_404(Comment, pk=pk, issue=issue_pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user, issue=Issue.objects.get(pk=issue_pk)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
        if not Issue.objects.filter(pk=issue_pk, project=project_pk).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment = get_object_or_404(Comment, pk=pk, issue=issue_pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
