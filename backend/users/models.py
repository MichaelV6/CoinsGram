import uuid
from os.path import splitext

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Если у тебя нет foodgram.constants — замени на число, например:
MAX_USER_NAME = 150

# Если нет утилиты image_compress, закомментируй её или добавь stub:
# from your_project.utils import image_compress

class User(AbstractUser):
    def upload_to(self, filename):
        file_root, ext = splitext(filename)
        new_name = f"{uuid.uuid4().hex}{ext}"
        return f"users/{self.username}/{new_name}"

    username = models.CharField(
        "имя пользователя",
        max_length=MAX_USER_NAME,
        unique=True,
        validators=[RegexValidator(r"^[\w.@+-]+$")],
    )
    email = models.EmailField("почта", unique=True)
    first_name = models.CharField("имя", max_length=MAX_USER_NAME)
    last_name = models.CharField("фамилия", max_length=MAX_USER_NAME)
    avatar = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        verbose_name="аватар",
    )

    REQUIRED_FIELDS = ("username", "first_name", "last_name", "password")
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("email",)

    def __str__(self):
        return f"{self.email}"

class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="кто подписался",
    )
    subscribed_to = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="на кого подписались",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscribed_to"],
                name="unique_subscription_users",)
                ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("user", "subscribed_to")

    def __str__(self):
        return f"{self.user} → {self.subscribed_to}"
