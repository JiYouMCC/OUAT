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
using System.Collections;
using Common;


/// <summary>
/// Summary description for 玩家
/// </summary>
public class 玩家
{
	public 玩家()
	{
		//
		// TODO: Add constructor logic here
		//
	}

    StringList _要素牌 = new StringList();

    public StringList 要素牌
    {
        get
        {
            return _要素牌;
        }
    }

    public string 名字 = string.Empty;

    public int 三段剧情 = 3; 

    public StringList _结局卡 = new StringList();
    
    public StringList 结局卡
    {
        get
        {
            return _结局卡;
        }
    }

    /// <summary>
    /// 聊天记录里的位置
    /// </summary>
    public int charIndex = 0;

}

/// <summary>
/// 玩家列表
/// </summary>
public class 玩家队列 : Cirque<玩家>
{
    public 玩家 this[int index]
    {
        get
        {
            return list[index];
        }
    }

    public 玩家 this[string name]
    {
        get
        {
            foreach (玩家 player in list)
            {
                if (player.名字.ToLower() == name.ToLower())
                    return player;
            }
            return null;
        }
    }

    public int IndexOf(玩家 player)
    {
        return list.IndexOf(player);
    }

    /// <summary>
    /// 获得玩家列表
    /// 以传入玩家玩家为起始位置的列表
    /// </summary>
    /// <param name="player"></param>
    /// <returns></returns>
    public 玩家队列 GetPlayList(玩家 player)
    {
        玩家队列 result = new 玩家队列();
        int index = list.IndexOf(player);
        result.list.AddRange(list.GetRange(index, list.Count - index));
        result.list.AddRange(list.GetRange(0, index));
        return result;
    }

}

