from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import ElementCard, EndingCard
import logging

ELEMENT_CARDS = ["浑水摸鱼",
                 "千杯不醉",
                 "漂移",
                 "晴空霹雳",
                 "讨价还价",
                 "善变的",
                 "会面",
                 "利润",
                 "中性",
                 "睡觉",
                 "有利可图的",
                 "很久不见",
                 "批准",
                 "款待",
                 "八卦",
                 "内疚",
                 "金字塔",
                 "犹抱琵琶半遮面",
                 "维他命C",
                 "三八",
                 "犯罪",
                 "失恋",
                 "耸肩",
                 "程度",
                 "环境",
                 "恳求",
                 "劣等",
                 "梦中见过的地方",
                 "朝向",
                 "耗子",
                 "贼",
                 "雌的",
                 "焊接",
                 "隔离",
                 "乌鸦嘴",
                 "繁殖",
                 "十八罗汉",
                 "途径",
                 "各显神通",
                 "崇高",
                 "激进的",
                 "海选",
                 "徒劳",
                 "慷慨的",
                 "核心",
                 "原野",
                 "知音",
                 "人血馒头",
                 "梗概",
                 "名牌",
                 "仙凡之恋",
                 "牛头不对马嘴",
                 "做爱",
                 "正当的",
                 "哈雷慧星撞地球",
                 "移植",
                 "厚黑学",
                 "围魏救赵",
                 "抑制",
                 "拒绝",
                 "优先",
                 "唯一的",
                 "聋",
                 "秘密的",
                 "各有千秋",
                 "审美疲劳",
                 "无条件的",
                 "狗急跳墙",
                 "贼",
                 "谦虚的",
                 "高尔夫",
                 "中等的",
                 "魔兽",
                 "贱人",
                 "战略",
                 "警惕",
                 "进口",
                 "始终如一",
                 "重复",
                 "憎恨",
                 "抽搐",
                 "忽悠",
                 "假设",
                 "秒杀",
                 "秃顶",
                 "花园",
                 "门",
                 "BT",
                 "哈利波特",
                 "胜任",
                 "储蓄",
                 "比较",
                 "广告",
                 "老气横秋",
                 "青春期",
                 "作弊",
                 "嚣张",
                 "听说",
                 "将军",
                 "立法",
                 "撤销",
                 "插曲",
                 "冒险",
                 "近似",
                 "非常聪明的",
                 "CHECK IT OUT",
                 "High",
                 "指望",
                 "季节变换",
                 "手工做的",
                 "网管",
                 "收养",
                 "朴素",
                 "模糊",
                 "魔戒的诱惑",
                 "现场",
                 "毁灭",
                 "斑点",
                 "考试"]

ENDING_CARDS = ["我以为我在谷底，没料到原来这已是我的颠峰。",
                "他再也没能离开那个世纪，亿万年后，人们在恐龙骨的化石堆里，惊奇地发现了一颗纯金的人类牙齿。",
                "他们合为一体，却无法见到对方，有如一枚硬币的正反两面。",
                "后来，公主的灵魂残念散布到湖泊和水源中，变成了一种小小的生物，它们当中的雌性尤其喜欢亲近人类。 人们叫它“吻子”，但它们还是那么不讨人喜欢，经常被人类一巴掌拍死。",
                "石油从油井里喷射了出来，不，不是石油，喷射的居然是巧克力。他们发现了世界上唯一的巧克力矿。",
                "于是那个魔法被破除了，他们都自由了",
                "斑马的诅咒生效了，从此她再也不能入睡",
                "他们连一片叶子也没有找到。那唯一的一片叶子是藏在那个死女孩的棺材里，而这事情谁也不知道。",
                "他终于走进了结婚礼堂，但是新郎并不是我，我只能在天国慢慢地为你祈福。",
                "天晓得他说的这些都是真话。唯一不为人知的是，其实他并不是故事中那个英勇的主人公，而是那个大家都唾弃的小人。",
                "生物学家看着自己的成果，心满意足地叹了口气：“那么多年，你终于回来了”",
                "女人亲了男人已经没有温度的嘴唇一下，冷冷笑道：“亲爱的，你永远是我的了。”",
                "死者张大着眼睛,那里映着一张巧笑的明眸……",
                "卫斯理去看牙医，医生让他这辈子再也别吃哈根达斯。",
                "也就在此时，天真的塌下来了，一群穷凶极恶的外星人开始入侵，被小宝发现，但没有人相信他说的话。",
                "他们就一直那样跳舞，一直到现在都没结束。",
                "所有人都围着火堆，喝酒，唱着吉祥三烤，吃他们喜欢的白萝卜马肉煲。",
                "就像它出现时候一样，它又神秘地消失了",
                "如果你在哪里见到一个眼角有痣的动物，请代我向她问声好。她叫赫敏，是我爱过的女人。",
                "结尾：十多年就这样过去了，当这些人重聚在一起再次开ouat时，并不知道曾经的斑马和吸血鬼cp还在看不见的角落里凝望着他们。",
                "人在江湖飘，哪能不挨刀，挨刀不可怕，烤马包治疗",
                "命中注定遭受百年孤独的家族在大地上第二次出现。",
                "每件东西都恢复成原有的光芒",
                "罗密欧气喘吁吁地从朱丽叶身上爬下来，拍拍她的屁股说，亲爱的，你跑得真棒，我现在给你换新马掌。",
                "真相就是这样，我猜对了开头，却没猜中这个结尾。",
                "钱员外拿着钱夫人15年前留下的遗书，让人挖开她的坟，从骸骨里取出当年她吞下自杀的那个金印。",
                "最终卡西莫多到停放心爱的人尸首的屋子里，紧紧的抱起她，默默的守在她身旁，直到一同化作灰烬。",
                "从此黑暗笼罩着大地，村里的人都生活在醉生梦死的幻觉里。",
                "吃下第一百三十七头斑马，她终于修炼成了人形。",
                "原来如此，她忍不住笑。起先是微笑，然后大笑，最终她再也不能遏止，歇斯底里地狂笑起来。笑着笑着，却又流下了眼泪。",
                "只要她还活着，它就不能被移除",
                "这时她可以讲话了。她说出了真情，取得了理解，同时也击败了诽谤，最后她赢得了幸福。她终于成了胜利者。",
                "摸金校尉如果不带黑驴蹄子，千万不要随便去挖幕，我不禁想起师傅临死的遗言。",
                "生者为过客，死者为归人。",
                "阿美气喘吁吁的跑到现场一看，才发现原来小全是条狗。",
                "自摸一条清龙，哈哈，给钱！ ",
                "据我所知，他们到现在还在跳舞",
                "破晓时他们可以看到它是完美的",
                "秃驴，竟然敢跟贫道抢尼姑！",
                "就是那一天，他们就坐在那里",
                "好人死了，坏人也死了，只有这个小孩孤独的活了下来，把这个故事传给后人。",
                "从此家家户户都在院子里种上了觉觉花，养起了斑马",
                "喝下最后一口咖啡，当然是冷却的，孙小美终于睁着血红的眼睛把《基础会计学》翻过最后一页。",
                "真相只有一个，杀手就在我们中间。",
                "一个人来，一个人走，这就是一个杀手的结局。",
                "记得……帮我……把……六角钱……交给党……这是我……最后……的党费……",
                "原来死不是结束，被遗忘才是生命的终点",
                "和尚对他说：你终于顿悟了。说罢，他们一起消失在了茫茫青山之中。",
                "他微笑：你想知道为什么吗？天地不仁，以万物为刍狗。这就是答案。受死吧。手起刀落，世上又少了一人。",
                "预言就这样实现了",
                "他又把尸体丢进了井里，但这次尸体没有消失",
                "她永远戴着它以提醒自己",
                "A终于抛弃了自己的自尊讲出了自己的真心话，但也是遗言。",
                "“你已经从我的魔法中释放了，而我们明天就要结婚”",
                "命运之手曾经给了他无上的荣耀，但最终却给了他残酷的诅咒，他必须在孤独，痛苦中活着，直到自己的终点。",
                "音乐会上，维维听得睡着了，梦见自己变成一只猫，躺在钢琴里睡懒觉。",
                "亲爱的，我觉得在野外做，比刚才在床上刺激，下次，我们去野外吧。",
                "当他回到家乡，所有认识他的人都已经不在了。人们像看着个怪物似的看着他。",
                "一缕阳光射穿云层，最坚硬的冰山也轰然倒塌，漫长的冰河期终于结束了。",
                "命案的真凶是那狐狸。",
                "1920年12月25日凌晨，纽约一条狭窄肮脏的街道上发现了他的尸体。身中5弹。一只流浪猫在他身边踱来踱去。没有目击者，警方按意外死亡处理。 ",
                "最后，机器人统治了世界，人类沦为电池。",
                "他们改变了地点，所有的事物都恢复了正常",
                "她看到了自己的倒影。但那不再是一只粗笨的、深灰色的、又丑又令人讨厌的小猪，而却是——一位公主。",
                "看了董永和七仙女、白素贞和许仙的故事，我的思维不再被人仙之恋，人妖之恋所禁锢，勇敢地朝着心爱的花仙小芭跑去。",
                "他将和他的棺材一起坠落，比天国坠落得还要深。只有在隔了一千年以后我才再来找他，使他能有机会再坠落得更深一点，或是升向那颗星——那颗高高地亮着的星！”",
                "由于他们的邪恶和谎言，他们变瞎了，并这样度过余生",
                "十多年就这样过去了，当这些人重聚在一起再次开ouat时，并不知道曾经的斑马和吸血鬼cp还在看不见的角落里凝望着他们。",
                "他终于成功的按照他喜欢的方式死去，到现在都没人见过他的遗体，哪怕一根毛发。",
                "所有人静静的躺在自己家中，等待着世纪末日的到来。",
                "猫捉到老鼠从来不急于把它一口吃掉,而是慢慢的折磨,欣赏他眼中越来越深恐惧,直到最后,被吓死.",
                "一盆鲜嫩欲滴的荔枝能让杨贵妃忘却一切烦恼，一颗珠圆玉润的荔枝核却要了杨贵妃的命。",
                "她说：这下你该吸取教训了吧，以后少看点恐怖电影。",
                "山中的雪地上闪着一丝淡红的光。石匣里每一颗心中也闪着一丝淡红的光：“上帝对我们的安排总是最好的！”",
                "212038214231321。他最后留下的这串数字，到底蕴含着什么意义，已经不会再有人知道了。",
                "他告诉他自己是个王子，然后他们过着幸福的生活",
                "虽然警方已经结案，认定的凶手已经去世多年，但是这本毕业纪念册的秘密依然不被人知晓",
                "土豪斑马啊，据说他再也不用收租了，过起了996的人生",
                "默默一刀捅穿了斑马，然而斑马的衣服依然是恐怖的白色",
                "斑马村终于通了公路，通过网络带货卖出了滞销的兔肉、狐皮等特产，脱掉了贫困村这个大帽子。村里的动物们都过上了幸福的生活。",
                "他因为坐动车睡过头到了封城的武汉，最后进入了隔离病房担任吉祥物，为抗击疫情作出了贡献。",
                "他拼尽全力为父皇的江山赢得盛世繁华，如今天下已定，他可放心实现许她的一世独宠.只是，他不知，她未等他。",
                "他唤她过来。她微笑的跑过去，投入他的怀抱，一把宝剑从她身体穿过！",
                "刘所长走进办公室，桌上放着一份《关于禁止在辖区内饲养宠物的通告》等着他签字。刘所长认真地看完后，伸出右爪，在通告下面摁上了一朵红红的小梅花。",
                "没人知道他大闹天宫的原因是他爱上了观音，就像捣蛋的孩子想要关注。",
                "她忽然有种莫名的悲伤，转过头，眼角缓缓滑落一滴机油。",
                "她叹了口气，我们熊猫过多的干涉人类，是导致人类种族灭亡的根本原因",
                "他从未告诉我，原来我不是人类",
                "我们擦肩而过，手里握着彼此的钱包",
                "惊醒，身边躺着自己的尸体",
                "他犹豫很久，终于对那个号码发了句情人节快乐。\r\n很快便有了答复：“谢谢，你哪位？”"]


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def init(request):
    if request.user and request.user.is_superuser:
        
        # logging.warn("初始化要素卡")
        # ElementCard.objects.all().delete()
        # for word in ELEMENT_CARDS:
        #     new_card = ElementCard(word=word)
        #     new_card.save()

        # logging.warn("初始化结局卡")
        # EndingCard.objects.all().delete()
        # for text in ENDING_CARDS:
        #     new_card = EndingCard(text=text)
        #     new_card.save()
        return HttpResponse('<html><body>初始化完成！</body></html>')

def cards(request):
    template = loader.get_template('cards.html')
    context = {
        'element_cards': ElementCard.objects.all(),
        'ending_cards':EndingCard.objects.all()
    }
    return HttpResponse(template.render(context, request))
