from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor, Issue, Project, Comment

class IsContributorOrAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == "POST":
            if isinstance(obj, Project):
                project = obj.id
            if isinstance(obj, Issue):
                project = (obj.project_id,)
            if isinstance(obj, Comment):
                related_issue = Issue.objects.get(id=obj.issue_id)
                project = related_issue.project_id
            return (
                Contributor.objects.filter(project_id=project, user_id=request.user.id)
                or request.user == obj.author
            )
        if request.method in ["DELETE", "PUT"]:
            return request.user == obj.author
        else:
            return False


class ContributorsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return Contributor.objects.filter(project=obj, user=request.user)
        if request.method in ["DELETE", "POST"]:
            return Contributor.objects.filter(
                project_id=obj.id, user_id=request.user.id, permissions="manager"
            )
        else:
            return False
