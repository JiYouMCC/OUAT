from django.db import models
from django.conf import settings
from django.utils.timezone import now
import json


class Cache(models.Model):
    cache_key = models.CharField(
        max_length=1024,
        verbose_name="key",
        primary_key=True
    )

    cache_value = models.TextField(
        verbose_name="value",
        blank=True,
        null=False
    )

    def get(cache_key):
        cache_objects = Cache.objects.filter(cache_key=cache_key)
        if cache_objects:
            return json.loads(cache_objects[0].cache_value)
        else:
            return None

    def set(cache_key, cache_value):
        Cache.objects.filter(cache_key=cache_key).delete()
        cache = Cache(cache_key=cache_key, cache_value=json.dumps(cache_value))
        cache.save()


class Message(models.Model):
    class MessageTypes(models.TextChoices):
        SYSTEM = 'SYS'
        CHAT = 'CHA'

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
    message_type = models.CharField(
        max_length=3,
        choices=MessageTypes.choices,
        default=MessageTypes.CHAT
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
