from django.db import models
from django.conf import settings

class Token(models.Model):
    # 其实可以用djangorestframework里面的token，但是偷懒了，就没有用
    token = models.CharField(
        max_length=32,
        verbose_name="token",
        unique=True,
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token_user',
        null=False
    )
