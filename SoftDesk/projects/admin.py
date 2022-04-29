from django.contrib import admin
from .models import Issue, Project, Contributor

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id","title","description" ,"type")

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'project_id','permissions','role')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title','desc','project_id','priority','tag','status')