from django.db import models

class Tag(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#FFFFFF')
    slug  = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name