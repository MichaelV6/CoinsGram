from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.plumbing import build_basic_type
from rest_framework import serializers
from django.conf import settings

class UserSerializerExtension(OpenApiSerializerExtension):
    target_class = 'users.serializers.UserSerializer'

    def map_serializer(self, auto_schema, direction):
        result = auto_schema.resolve_serializer(self.target, direction, bypass_extensions=True)
        

        if 'avatar' in result['properties']:
            result['properties']['avatar'] = {
                'type': 'string',
                'format': 'binary',
                'description': 'Аватар пользователя (изображение)'
            }
        
        return result