from django.contrib import admin
from .models import Issue, Project, Contributor, Comment
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    list_filter = ("is_staff", "is_superuser")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "description", "type")


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("user_id", "project_id", "permissions", "role")


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project_id", "author")


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "issue",
        "author",
    )
