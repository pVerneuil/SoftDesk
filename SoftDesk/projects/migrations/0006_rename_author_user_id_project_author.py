# Generated by Django 4.0.4 on 2022-06-02 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_contributor_permissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='author_user_id',
            new_name='author',
        ),
    ]
