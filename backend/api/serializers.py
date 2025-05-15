from rest_framework import serializers
from coins.models import Coin
from tags.models import Tag
from favorites.models import Favorite

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ('id', 'name', 'color', 'slug')

class CoinReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags   = TagSerializer(many=True, read_only=True)
    # Явно указываем, что это файл изображения
    image = serializers.ImageField(required=False)

    class Meta:
        model  = Coin
        fields = (
            'id', 'author', 'name', 'description',
            'estimated_value', 'tags', 'image', 'pub_date'
        )

class CoinWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    # Явно указываем, что это файл изображения
    image = serializers.ImageField(required=False)

    class Meta:
        model = Coin
        exclude = ('author', 'pub_date')

    def validate_estimated_value(self, value):
        """Валидация оценочной стоимости"""
        min_value = 1
        max_value = 10_000_000
        
        if value < min_value or value > max_value:
            raise serializers.ValidationError(
                f'Оценочная стоимость должна быть от {min_value} до {max_value} ₽'
            )
        return value
        
    def validate_image(self, value):
        """Валидация изображения"""
        if value:
            # Проверка размера файла (не более 5 МБ)
            if value.size > 5 * 1024 * 1024:
                from api.exceptions import FileTooLargeError
                raise FileTooLargeError('Размер файла не должен превышать 5 МБ')
                
            # Проверка формата файла
            allowed_formats = ['image/jpeg', 'image/png', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in allowed_formats:
                from api.exceptions import InvalidImageError
                raise InvalidImageError('Поддерживаемые форматы: JPEG, PNG, GIF')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        coin = Coin.objects.create(
            **validated_data,
        )
        coin.tags.set(tags)
        return coin

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()
        return instance
    
class FavoriteSerializer(serializers.ModelSerializer):
    coin = serializers.PrimaryKeyRelatedField(queryset=Coin.objects.all(), required=True)
    
    class Meta:
        model = Favorite
        fields = ('id', 'coin')
        
    def create(self, validated_data):
        user = self.context['request'].user
        coin = validated_data.get('coin')
        
        # Проверяем, нет ли уже такой записи
        if Favorite.objects.filter(user=user, coin=coin).exists():
            from api.exceptions import DuplicateFavoriteError
            raise DuplicateFavoriteError()
            
        # Создаем запись в избранном
        return Favorite.objects.create(user=user, coin=coin)