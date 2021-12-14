using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using System.Collections.Generic;
using Common;

/// <summary>
/// 游戏的运行时的控制对象
/// </summary>
public class 游戏
{
	public bool GameStart = false;
    public 游戏()
    {
        //
        // TODO: Add constructor logic here
        //
    }

    static 游戏 instance = new 游戏();

    public static 游戏 Instance
    {
        get
        {
            return instance;
        }
    }

    /// <summary>
    /// 游戏中的玩家队列
    /// </summary>
    public 玩家队列 players = new 玩家队列();
    public 旁观队列 noplayers = new 旁观队列();

    public Stack<游戏状态> states = new Stack<游戏状态>();

    public em状态 GetState(玩家 player)
    {
        try
        {
            游戏状态 s = states.Peek();
            return s.GetState(player);
        }
        catch
        {
            return em状态.None;
        }
    }

    /// <summary>
    /// 聊天记录
    /// </summary>
    public StringList Chats = new StringList();

	/// <summary>
    /// 重置游戏
    /// </summary>
    public void ResetGame()
    {
        GameStart = false;
    }

    /// <summary>
    /// 开始新游戏
    /// </summary>
    public void BeginGame()
    {
	    GameStart = true;
        states.Clear();
        players.MoveFirst();
        BeginSayStory(players.Current);
        foreach (玩家 pl in players.ToArray)
        {
            pl.要素牌.Clear();
            pl.要素牌.AddRange(卡片.Get要素牌(5));
            pl.结局卡.Clear();
            pl.结局卡.AddRange(卡片.Get结局卡(1));
            pl.三段剧情 = 3;            
        }
        //游戏.Instance.Chats.Clear();
        this.Chats.Clear();
        this.Chats.Add("大家请注意，游戏现在开始!");
        //this.Chats.RemoveRange(0,this.Chats.Count-1);
    }

    /// <summary>
    /// 玩家说一句故事
    /// </summary>
    /// <param name="player"></param>
    /// <param name="card"></param>
    /// <param name="story"></param>
    public string SayStory(玩家 player, string card, string story)
    {
        if (states.Peek() is 说故事状态)
        {
	        if (player.要素牌.Count > 0)
	        {
            	if (player.要素牌.IndexOf(card) < 0)
                	return "非法要素牌";
            	if (story.IndexOf(card) < 0)
                	return "故事里没有包含要素信息";
                else story = story.Replace(card,"【"+card+"】");
			}
			else 
			{
				if (player.三段剧情 <= 0 && story.IndexOf(player.结局卡[0]) < 0)
					return "故事里没有包含结局卡信息";
			}
            说故事状态 sayState = states.Peek() as 说故事状态;
            if (sayState.GetState(player) != em状态.WaitSayStory)
                return "现在还轮不到你说故事";

            string str = "{0}说:<span  style='color:Red'>{1}</span>";
            str = string.Format(str, player.名字, story);
            this.Chats.Add(str);
            sayState.SetState(player, em状态.Complete);
            if (player.要素牌.Count > 0)
            {
            	player.要素牌.Remove(card);
            	sayState.List.MoveNext();
            	玩家 next = sayState.List.Current;
            	sayState.SetState(next, em状态.WaitCheckStory);
            	sayState.story = story;
            	return string.Empty;
        	}
            else
            {
				if (player.三段剧情 > 0)
				{
					player.三段剧情 = player.三段剧情-1;
					sayState.List.MoveNext();
            		玩家 next = sayState.List.Current;
            		sayState.SetState(next, em状态.WaitCheckStory);
            		sayState.story = story;
            		return string.Empty;
				}
				else
				{
					str = "<span  style='color:Green'>游戏结束！</span>";
            		this.Chats.Add(str);
            		return string.Empty;
				}
			}	
        }
        else
        {
            return "现在还不是说故事的时候";
        }
    }

    /// <summary>
    /// 是否同意玩家说的故事
    /// </summary>
    /// <param name="player"></param>
    /// <param name="isAngree"></param>
    /// <param name="reason"></param>
    /// <returns></returns>
    public string AgreeStory(玩家 player, bool isAngree, string reason)
    {
        if (states.Peek() is 说故事状态)
        {

            说故事状态 sayState = states.Peek() as 说故事状态;
            if (sayState.GetState(player) != em状态.WaitCheckStory)
                return "确认失败";

            if (isAngree)
            {
                //  同意故事有效
                string str = "{0}认为故事合理";
                str = string.Format(str, player.名字);
                Chats.Add(str);

                sayState.SetState(player, em状态.Agree);
            }
            else
            {
                // 玩家认为故事无效

                string str = "{0}认为故事不合理，原因：<span  style='color:Lime'>{1}</span>";
                str = string.Format(str, player.名字, reason);
                Chats.Add(str);

                sayState.SetState(player, em状态.Dissent);
            }

            玩家 next = sayState.List.MoveNext();


            if (sayState.GetState(next) == em状态.Complete)
            {
                // 没有人能打断第一玩家说的故事，玩家可以继续接着再说故事

                bool unagree = true;
                bool agree = false;
                foreach (玩家 p in sayState.List.ToArray)
                {
                    if (sayState.GetState(p) == em状态.Dissent)
                        unagree = false;
                    if (sayState.GetState(p) == em状态.Agree)
                        agree = true;
                }

                if (agree && unagree)
                {
                    // 大家都同意
                    string str = "所有人都认为{0}说的故事合理,请{0}接着往下说";
                    str = string.Format(str, next.名字);
                    Chats.Add(str);

                    goto _故事有效;
                }
                else if (!unagree && !agree)
                {
                    // 大家都不同意
                    string str2 = "所有人都认为{0}说的故事不合理,请{0}重新说一个故事";
                    str2 = string.Format(str2, next.名字);
                    Chats.Add(str2);

                    goto _故事无效;
                }
                else
                {
                    // 有人反对中断的有效性
                    if (sayState.checkNum == 0)
                    {
                        Chats.Add("现在大家意见不统一，请大家慎重投票，如果投票 (故事有效 >= 认为故事无效) 则通过");
                        next = sayState.List.MoveNext();
                        sayState.checkNum++;

                        sayState.SetState(next, em状态.WaitCheckStory);
                        return string.Empty;
                    }
                    else if (sayState.checkNum >= 1)
                    {
                        int a = 0; int u = 0;
                        foreach (玩家 p in sayState.List.ToArray)
                        {
                            if (sayState.GetState(p) == em状态.Dissent)
                                u++;
                            if (sayState.GetState(p) == em状态.Agree)
                                a++;
                        }

                        if (a >= u)
                        {
                            // 大家同意故事有效
                            string str = "大部分人认为{0}说的故事合理,请{0}接着往下说";
                            str = string.Format(str, next.名字);
                            Chats.Add(str);

                            goto _故事有效;

                        }
                        else
                        {
                            string str2 = "大部分人认为{0}说的故事不合理,请{0}重新说一个故事";
                            str2 = string.Format(str2, next.名字);
                            Chats.Add(str2);

                            goto _故事无效;
                        }
                    }
                }
            _故事有效:

                states.Pop();
                players.Current = next;
                BeginSayStory(players.Current);
                return string.Empty;

            _故事无效:

                玩家 first = sayState.List.First;
                first.要素牌.AddRange(卡片.Get要素牌(2) as List<string>);
                first.三段剧情 = 3;
                states.Pop();
                players.Current = first;
                BeginSayStory(players.Current);

                return string.Empty;          
            }

            sayState.SetState(next, em状态.WaitCheckStory);
            return string.Empty;
        }
        else
        {
            return "现在还不是确认故事的时候";
        }
        return string.Empty;
    }

    /// <summary>
    /// 玩家进行中断
    /// </summary>
    /// <param name="player"></param>
    /// <param name="card"></param>
    /// <param name="reason"></param>
    /// <returns></returns>
    public string CutStory(玩家 player, string card, string reason)
    {
        if (states.Peek() is 说故事状态)
        {
            if (player.要素牌.IndexOf(card) < 0)
                return "非法要素牌";

            说故事状态 sayState = states.Peek() as 说故事状态;
            if (sayState.GetState(player) != em状态.WaitCheckStory)
                return "现在还轮不到你中断";

            string str = "{0}用【<span style='color:Red'>{1}</span>】中断故事，原因：<span  style='color:Lime'>{2}</span>";
            str = string.Format(str, player.名字, card, reason);
            this.Chats.Add(str);

            中断状态 cut = new 中断状态();
            cut.List = players.GetPlayList(player);
            cut.SetState(player, em状态.Complete);
            cut.List.MoveNext();
            cut.SetState(em状态.WaitCheckCutStory);
            cut.card = card;

            states.Push(cut);
            return string.Empty;
        }
        else
        {
            return "现在还不是中断时候";
        }
    }

    /// <summary>
    /// 判断玩家的中断是否合适
    /// </summary>
    /// <param name="player"></param>
    /// <param name="isAngree"></param>
    /// <param name="reason"></param>
    /// <returns></returns>
    public string AgreeCutStory(玩家 player, bool isAngree, string reason)
    {
        if (states.Peek() is 中断状态)
        {
            中断状态 cutState = states.Peek() as 中断状态;
            if (cutState.GetState(player) != em状态.WaitCheckCutStory)
                return "确认失败";

            if (isAngree)
            {
                //  同意中断有效
                string str;
                if (reason == string.Empty)
                {
                    str = "{0}认为中断理由合适。{1}";
                }
                else
                {
                    str = "{0}认为中断理由合适。理由：<span  style='color:Lime'>{1}</span>";
                }
                str = string.Format(str, player.名字, reason);
                Chats.Add(str);

                cutState.SetState(player, em状态.Agree);

            }
            else
            {
                // 玩家认为中断无效

                string str = "{0}认为【<span  style='color:Red'>{2}</span>】要素卡片中断理由不合适。理由：<span  style='color:Lime'>{1}</span>";
                str = string.Format(str, player.名字, reason, cutState.card);
                Chats.Add(str);

                cutState.SetState(player, em状态.Dissent);

            }

            玩家 next = cutState.List.MoveNext();    //  取得下一位玩家

            if (cutState.GetState(next) == em状态.Complete)
            {
                // 已经轮完一圈，判断中断是否有效

                bool unagree = true;
                bool agree = false;
                foreach (玩家 p in cutState.List.ToArray)
                {
                    if (cutState.GetState(p) == em状态.Dissent)
                        unagree = false;
                    if (cutState.GetState(p) == em状态.Agree)
                        agree = true;
                }
                if (agree && unagree)
                {
                    // 大家都同意
                    return 中断有效处理(cutState, next, true);
                }
                else if (!unagree && !agree)
                {
                    // 大家都不同意                    
                    Chats.Add(string.Format("所有人都认为{0}用【<span  style='color:Red'>{1}</span>】中断不合适", next.名字, cutState.card));
                    next.要素牌.AddRange(卡片.Get要素牌(2));
                    //cutState.SetState(next, em状态.Agree);
                    return 中断无效处理(cutState, next);
                }
                else
                {
                    // 有人反对中断的有效性
                    if (cutState.checkNum == 0)
                    {
                        Chats.Add("现在大家意见不统一，请大家慎重投票，如果 (同意中断 >= 反对中断) 则中断合理");
                        next = cutState.List.MoveNext();
                        cutState.checkNum++;
                    }
                    else if (cutState.checkNum >= 1)
                    {
                        int a = 0; int u = 0;
                        foreach (玩家 p in cutState.List.ToArray)
                        {
                            if (cutState.GetState(p) == em状态.Dissent)
                                u++;
                            if (cutState.GetState(p) == em状态.Agree)
                                a++;
                        }

                        if (a >= u)
                        {
                            return 中断有效处理(cutState, next, false);
                        }
                        else
                        {
                            Chats.Add(string.Format("大部分人同意{0}用【<span  style='color:Red'>{1}</span>】中断不合适", next.名字, cutState.card));
                            next.要素牌.AddRange(卡片.Get要素牌(2));
							cutState.SetState(next, em状态.Agree);
                            return 中断无效处理(cutState, next);
                        }
                    }
                }

            }
            // 下一个玩家进行确认
            cutState.SetState(next, em状态.WaitCheckCutStory);

            return string.Empty;
        }
        else
        {
            return "现在还不是确认中断的时候";
        }
    }

    private string 中断无效处理(中断状态 cutState, 玩家 next)
    {
	    //大部分人认为中断无效
        states.Pop();
        说故事状态 sayState = states.Peek() as 说故事状态;
        next = sayState.List.Current;
        sayState.SetState(next, em状态.Agree);
        next = sayState.List.MoveNext();
        sayState.SetState(next, em状态.WaitCheckStory);
		//cutState.SetState(next, em状态.Agree);
        return string.Empty;
    }

    private string 中断有效处理(中断状态 cutState, 玩家 next, bool isAll)
    {
        // 大家都认为中断有效
        states.Pop();
        说故事状态 sayState = states.Pop() as 说故事状态;
        玩家 sayPlayer = sayState.List.First;
        sayPlayer.三段剧情 = 3;// 被中断的玩家要重新三段论
        sayPlayer.要素牌.AddRange(卡片.Get要素牌(2) as List<string>); //  原来说故事的玩家受到惩罚
        next.要素牌.Remove(cutState.card);    // 中断玩家的要素牌可以被回收

        if (isAll)
        {
            string str = "所有人都同意{0}用【<span  style='color:Red'>{2}</span>】中断合适,现在有请{0}接着“<span  style='color:Red'>{1}</span>”往下说故事";
            str = string.Format(str, next.名字, sayState.story, cutState.card);
            Chats.Add(str);
        }
        else
        {
            string str = "大部分人同意{0}用【<span  style='color:Red'>{2}</span>】中断合适,现在有请{0}接着“<span  style='color:Red'>{1}</span>”往下说故事";
            str = string.Format(str, next.名字, sayState.story, cutState.card);
            Chats.Add(str);
        }

        players.Current = next;
        BeginSayStory(players.Current);


        return string.Empty;
    }

    /// <summary>
    /// 玩家开始说故事
    /// </summary>
    /// <param name="player"></param>
    private void BeginSayStory(玩家 player)
    {
        说故事状态 story = new 说故事状态();
        story.List = players.GetPlayList(player);
        story.SetState(player, em状态.WaitSayStory);
        states.Push(story);
    }
}
