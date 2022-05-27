from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor, Issue, Project, Comments

# TODO trouver un meilleur nom
class IsContributorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if isinstance(obj, Project):
                return Contributor.objects.filter(
                    project_id = obj.id, 
                    user_id = request.user.id
                    )
            if isinstance(obj, Issue):
                return Contributor.objects.filter(
                    project_id = obj.project_id, 
                    user_id = request.user.id
                    )
            if isinstance(obj, Comments):
                related_issue = Issue.objects.get(id = obj.issue_id)
                return Contributor.objects.filter(
                project_id = related_issue.project_id, 
                user_id = request.user.id
                )
        if request.method in ['DELETE','PUT']:
            return request.user == obj.author_user_id