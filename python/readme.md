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
6. 初始化要素卡和结局卡，如果数据库是空的才能跑，会删除现有的所有要素卡和结局卡

  ```python manage.py shell```

  然后把init.py里面的全贴进去跑一遍
7. http://127.0.0.1:8000 可以搞了

### 消息

#### 大类

| 描述 | 数据库层 | ui层 | socket回传消息 |
| -- | -- | -- | -- |
| 聊天信息     | message_type: CHAT = 'chat' | 啥都不写 |'type': MessageType.CHAT = 'chat' |
| 系统信息     | message_type: SYSTEM = 'system' | 'type':'system' |'type': MessageType.SYSTEM = 'system' |
| 游戏信息     | message_type: GAME = 'game' | 'type':'game' |'type': MessageType.GAME = 'game' |

#### 系统信息

- online
  用户进入（ouat的页面），后端自动把他加入用户列表
- offline
  用户离开（ouat的页面），后端自动把他踢出用户列表
- user_list
  获取当前用户列表

#### 游戏信息和操作

- attend
  （未加入的已在线用户）准备加入（未开始的）游戏
- cancel
  （已加入的已在线用户）取消加入未开始的）游戏
- start
  房主开始游戏
- quit
  游戏中的玩家逃跑
- tell
  游戏中的玩家用要素卡讲故事
- summary
  要素卡用完的玩家进行总结
- break
  其他玩家用要素卡对某个玩家讲的故事或者总结进行中断
- objection
  其他玩家对某个玩家讲的故事或者总结进行连贯性或者逻辑性的质疑
- ending
  总结完毕的玩家用结局卡进行结局陈述
- vote
  对其他玩家的中断或者异议进行同意或者反对

