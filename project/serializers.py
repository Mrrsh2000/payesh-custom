from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from payesh.dynamic import api_error_creator
from payesh.dynamic_api import DynamicSerializer
from project.models import Project


class ProjectSerializer(DynamicSerializer):
    """
    برای ایجاد کاربر جدید در سامانه
    """
    remove_field_view = {
        'retrieve': ['password'],
        'self': ['password', 'groups']
    }

    class Meta:
        model = Project
        extra_kwargs = api_error_creator(Project,
                                         ['title', 'description', 'code', 'start_date', 'end_date', 'score',
                                          'teacher', 'user',
                                          'is_ready', 'is_finish', ],
                                         blank_fields=[],
                                         required_fields=[])
        depth = 5
        fields = ['id', 'title', 'description', 'code', 'start_date', 'end_date', 'score', 'teacher', 'user',
                  'is_ready', 'is_finish', ]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, value):
        return make_password(value)

    def validate_username(self, value):
        if self.context['view'].action == 'create':
            if value is None or value == '':
                raise serializers.ValidationError('نام کاربری باید وارد شود')
        return value
