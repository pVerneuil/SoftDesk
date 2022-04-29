from django.conf import settings
from django.db import models



class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500, blank=True)
    type_choices = (
        ('back-end','back-end'),
        ('front-end','front-end'),
        ('IOS','IOS'),
        ('Android','Android')
    )
    type = models.CharField(max_length=128,  choices=type_choices)
    # author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE )

class Contributor(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE )  #on delete??
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=128)
    role = models.CharField(max_length=128)

class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    
    priority_choices = (
        ('LOW','FAIBLE'),
        ('MED', 'MOYENNE'),
        ('HIGH','ÉLEVÉE')
    )
    priority = models.CharField(max_length=128, choices=priority_choices)
    
    tag_choices = (
        ('BUG','BUG'),
        ('FEAT','AMÉLIORATION'),
        ('TASK','TÂCHE')
    )
    tag = models.CharField(max_length=128, choices=tag_choices)
    project_id  = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    
    status_choices= (
        ('TODO','Â faire'),
        ('INPROGRESS','En cours'),
        ('COMPLETE','Terminé')
    )
    status = models.CharField(max_length=128, choices = status_choices)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='autor')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, default=author_user_id, on_delete=models.CASCADE, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = models.CharField(max_length=500)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

