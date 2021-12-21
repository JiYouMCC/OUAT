from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Message(models.Model):
    text = models.TextField(
        max_length=1024,
        verbose_name="内容",
        blank=True,
        null=False
    )
    color = models.CharField(
        max_length=10,
        verbose_name="颜色",
        blank=False,
        null=True
    )
    datetime = models.DateTimeField(
        verbose_name="时间",
        default=now,
        blank=False,
        null=False
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="发送者",
        related_name='sender',
        null=False
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="接收者",
        related_name='receiver',
        blank=True,
        null=True
    )

class Token(models.Model):
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
        related_name='user',
        null=False
    )

# class ElementCard(models.Model):

#     word = models.CharField(
#         primary_key=True,
#         max_length=128,
#         verbose_name="词",
#         blank=False
#     )
#     usage_count = models.IntegerField(
#         verbose_name="使用次数",
#         null=False,
#         blank=False,
#         default=0
#     )
#     interrupt_success_count = models.IntegerField(
#         verbose_name="中断成功次数",
#         null=False,
#         blank=False,
#         default=0
#     )
#     tell_count = models.IntegerField(
#         verbose_name="讲述次数",
#         null=False,
#         blank=False,
#         default=0
#     )

# class EndingCard(models.Model):

#     text = models.TextField(
#         primary_key=True,
#         max_length=1024,
#         verbose_name="结局",
#         blank=False
#     )
#     usage_count = models.IntegerField(
#         verbose_name="使用次数",
#         null=False,
#         blank=False,
#         default=0
#     )

# class Game(models.Model):
#     status
#     players
#     start time
#     element cards
#     final cards


# class GameMessage(Message):
#     game = models.ForeignKey(
#         Game,
#         on_delete=models.CASCADE,
#         verbose_name="游戏",
#         related_name='game',
#         blank=False,
#         null=False
#     )

# class TellMessage(GameMessage):
#     class TellMessageType(models.TextChoices):
#         STORY ='STORY', _('故事')
#         FINAL ='FINAL', _('结局前')
#         ENDING ='ENDING', _('结局')

#     element = models.ForeignKey(
#         ElementCard,
#         on_delete=models.CASCADE,
#         verbose_name="使用要素",
#         related_name='element',
#         blank=False,
#         null=True
#     )
#     message_type = models.CharField(
#         choices=TellMessageType.choices,
#         default=TellMessageType.STORY,
#         blank=False,
#         null=True
#     )

# class InterruptMessage(GameMessage):
#     interrupt_to = models.ForeignKey(
#         ElementCard,
#         on_delete=models.CASCADE,
#         verbose_name="中断对象",
#         related_name='tell_story',
#         blank=False,
#         null=False
#     )

# class FailMessage(GameMessage):
#     fail_to = models.ForeignKey(
#         ElementCard,
#         on_delete=models.CASCADE,
#         verbose_name="不通顺对象",
#         related_name='tell_story',
#         blank=False,
#         null=False
#     )
