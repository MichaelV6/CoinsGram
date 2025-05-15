from django.db import models
from django.contrib.auth import get_user_model
from coins.models import Coin

User = get_user_model()

class Favorite(models.Model):
    user     = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    coin     = models.ForeignKey(
        Coin, on_delete=models.CASCADE,
        related_name='in_favorites'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coin')
        ordering = ['-added_at']
        verbose_name = 'Избранная монета'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f"{self.user.username} → {self.coin.name}"