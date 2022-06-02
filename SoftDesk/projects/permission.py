from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contributor, Issue, Project, Comments

#!! remove  debug print later
class IsContributorOrAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        print('permission called')
        if request.method in SAFE_METHODS:
            if isinstance(obj, Project):
                project = obj.id
                print('instance : Project')
            if isinstance(obj, Issue):
                project = obj.project_id, 
                print('instance : Issue')
            if isinstance(obj, Comments):
                related_issue = Issue.objects.get(id = obj.issue_id)
                project = related_issue.project_id
                print('instance : Comments')
            return Contributor.objects.filter(
                    project_id = project ,user_id = request.user.id
                    ) or request.user == obj.author_user_id
        if request.method in ['DELETE','PUT']:
            return request.user == obj.author_user_id
