from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import Project

class projectSerializer(ModelSerializer):
    class Meta:
        model = Project
        field = ['title','description','type_choices','type']