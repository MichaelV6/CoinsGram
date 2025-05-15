import uuid, os
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from tags.models import Tag

User = get_user_model()

def coin_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f"coins/{instance.author_id}/{uuid.uuid4().hex}{ext}"

class Coin(models.Model):
    author          = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='coins'
    )
    name            = models.CharField('Название', max_length=200)
    description     = models.TextField('Описание')
    estimated_value = models.PositiveIntegerField(
        'Оценочная стоимость, ₽',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10_000_000)
        ]
    )
    image           = models.ImageField(
        'Фото монеты', upload_to=coin_image_path
    )
    tags            = models.ManyToManyField(
        Tag, related_name='coins', verbose_name='Теги'
    )
    pub_date        = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Монета'
        verbose_name_plural = 'Монеты'

    def __str__(self):
        return f"{self.name} ({self.estimated_value} ₽)"