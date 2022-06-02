from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor, Issue, Project, Comment

#!! remove  debug print later
# TODO do contributors permissions
class IsContributorOrAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("is contributor permission called")
        print(obj)
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


class ContributorsPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #     return Contributor.objects.filter(
        #             project_id = obj.id ,user_id = request.user.id
        #             )
        return False
