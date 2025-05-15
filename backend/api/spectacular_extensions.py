from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.plumbing import build_basic_type
from rest_framework import serializers
from django.conf import settings

class CoinWriteSerializerExtension(OpenApiSerializerExtension):
    target_class = 'api.serializers.CoinWriteSerializer'

    def map_serializer(self, auto_schema, direction):
        result = auto_schema.resolve_serializer(self.target, direction, bypass_extensions=True)
        
        # Явно указываем, что image это поле для загрузки файла в формате OpenAPI
        if 'image' in result['properties']:
            result['properties']['image'] = {
                'type': 'string',
                'format': 'binary',
                'description': 'Изображение монеты'
            }
        
        return result