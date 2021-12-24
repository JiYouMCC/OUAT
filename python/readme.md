# python重写版本

## 一些笔记

东西比较多，我先胡乱写一写

### 依赖项和安装

#### python 3.X

我自己本地是Python 3.9.2

#### pip

[安装文档](https://pip.pypa.io/en/stable/installation/)

用来安装其他包的，我自己本地是pip 21.3.1

#### django 4.0

```
pip install django
```
[参考文档](https://www.djangoproject.com/)
#### channels

强制一下版本，其他版本有毛病

```
pip install channels==3.0.4
```
[参考文档](https://channels.readthedocs.io/en/stable/index.html)

#### django rest framework

这个不用装，我用比较笨的自己写的Token代替了

记录下，有空研究

理论上可以用来代替很多自己写的api

```
pip install djangorestframework
```

[参考文档](https://www.django-rest-framework.org/api-guide/authentication/)

#### redis

版本好像不限，能用就行

[在win下面装redis](https://github.com/MicrosoftArchive/redis/releases)

装好以后channels-redis升级一下，不然不太好用

```
pip install channels-redis==2.4.2
```

#### Django自带cache

Mark一下，目前用自己写的Cache module平替，就是比较傻

### 把环境架起来

1. 把数据库（db.sqlite3）删了，如果有的话
2. ```python manage.py makemigrations```

   ```python manage.py makemigrations account```

   ```python manage.py makemigrations game```
3. ```python manage.py migrate```

   ```python manage.py migrate account```

   ```python manage.py migrate game```

   理论上好像不用这样，但是忘了怎么一起弄了

4. 生成超级用户

   ```python manage.py createsuperuser```

   TTY模式：

   ```winpty python manage.py createsuperuser```
5. ```python manage.py runserver```
6. http://127.0.0.1:8000 可以搞了

### 消息

#### 大类

| 描述 | 数据库层 | ui层 | socket回传消息 |
| -- | -- | -- | -- |
| 聊天信息     | message_type: CHAT = 'chat' | 啥都不写 |'type': MessageType.CHAT = 'chat' |
| 系统信息     | message_type: SYSTEM = 'system' | 'type':'system' |'type': MessageType.SYSTEM = 'system' |
| 游戏信息     | message_type: SYSTEM = 'game' | 'type':'game' |'type': MessageType.GAME = 'game' |

#### 系统信息

- online
- offline
- user_list

#### 游戏信息

- attend
- cancel
- start
- quit
- tell
- break
- objection
- summary
- final
- vote

