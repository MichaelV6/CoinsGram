from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author_username', 'author_email', 'coin_name', 'short_text', 'created_at'
    )
    list_filter = ('coin', 'author', 'created_at')
    search_fields = ('text', 'author__username', 'author__email', 'coin__name')
    readonly_fields = ('created_at',)

    def author_username(self, obj):
        return obj.author.username
    author_username.short_description = 'Автор'

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Email автора'

    def coin_name(self, obj):
        return obj.coin.name
    coin_name.short_description = 'Монета (пост)'

    def short_text(self, obj):
        # Показывает только первые 40 символов
        return (obj.text[:40] + '...') if len(obj.text) > 40 else obj.text
    short_text.short_description = 'Текст комментария'

    # Русский заголовок модели в списке
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['view'] = True
        return perms

    # Если используешь verbose_name/verbose_name_plural в модели — это не нужно
