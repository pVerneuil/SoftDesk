from django.contrib import admin
from .models import Issue, Project, Contributor, Comments

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id",'author_user_id' ,"title","description" ,"type")

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'project_id','permissions','role')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title','desc','project_id','priority','tag','status')
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('description','issue_id','author_user_id','created_time')