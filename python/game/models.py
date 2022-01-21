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


class ElementCard(models.Model):
    word = models.CharField(
        primary_key=True,
        max_length=128,
        verbose_name="词",
        blank=False
    )

    enable = models.BooleanField(
        verbose_name="可用",
        blank=False,
        default=True
    )

    usage_count = models.IntegerField(
        verbose_name="抽取次数",
        blank=False,
        null=False,
        default=0
    )

    break_count = models.IntegerField(
        verbose_name="中断次数",
        blank=False,
        null=False,
        default=0
    )

    break_succeed_count = models.IntegerField(
        verbose_name="中断成功次数",
        blank=False,
        null=False,
        default=0
    )


class EndingCard(models.Model):
    text = models.TextField(
        primary_key=True,
        max_length=1024,
        verbose_name="结局",
        blank=False
    )

    enable = models.BooleanField(
        verbose_name="可用",
        blank=False,
        default=True
    )

    usage_count = models.IntegerField(
        verbose_name="抽取次数",
        blank=False,
        null=False,
        default=0
    )


class Message(models.Model):
    class MessageTypes(models.TextChoices):
        SYSTEM = 'system'
        CHAT = 'chat'
        GAME = 'game'

    class SystemMessageCommand:
        ONLINE = 'online'
        OFFLINE = 'offline'

    class GameMessageCommand:
        ATTEND = 'attend'
        CANCEL = 'cancel'
        QUIT = 'quit'
        BREAK = 'break'
        TELL = 'tell'
        SUMMARY = 'summary'
        ENDING = 'ending'

    text = models.TextField(
        max_length=1024,
        verbose_name="内容",
        blank=True,
        null=False
    )

    command = models.TextField(
        max_length=1024,
        verbose_name="命令",
        blank=False,
        null=True
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
        max_length=20,
        choices=MessageTypes.choices,
        default=MessageTypes.CHAT
    )

    element_card = models.ForeignKey(
        ElementCard,
        on_delete=models.CASCADE,
        verbose_name="要素卡",
        related_name='element_card',
        blank=False,
        null=True
    )

    ending_card = models.ForeignKey(
        EndingCard,
        on_delete=models.CASCADE,
        verbose_name="结局卡",
        related_name='ending_card',
        blank=False,
        null=True
    )

# class Game(models.Model):
#     status
#     players
#     start time
#     element cards
#     final cards
