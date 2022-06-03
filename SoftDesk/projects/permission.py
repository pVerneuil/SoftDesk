from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor, Issue, Project, Comment

#!! remove  debug print later
class IsContributorOrAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("is contributor permission called")
        if request.method in SAFE_METHODS or request.method == "POST":
            print("safe methode")
            if isinstance(obj, Project):
                project = obj.id
                print("instance : Project")
            if isinstance(obj, Issue):
                project = (obj.project_id,)
                print("instance : Issue")
            if isinstance(obj, Comment):
                related_issue = Issue.objects.get(id=obj.issue_id)
                project = related_issue.project_id
                print("instance : Comments")
            return (
                Contributor.objects.filter(project_id=project, user_id=request.user.id)
                or request.user == obj.author
            )
        if request.method in ["DELETE", "PUT"]:
            print("delete or PUT")
            return request.user == obj.author
        else:
            return False


class ContributorsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("contributor permission called")
        if request.method in SAFE_METHODS:
            print("methode safe")
            return Contributor.objects.filter(project=obj, user=request.user)
        if request.method in ["DELETE", "POST"]:
            print("methode post or delete")
            return Contributor.objects.filter(
                project_id=obj.id, user_id=request.user.id, permissions="manager"
            )
        else:
            return False
