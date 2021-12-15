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

public enum em状态
{
    None,
    WaitSayStory,
    WaitCheckStory,
    WaitCheckCutStory,
    Agree,
    Complete,
    Dissent
}

/// <summary>
/// Summary description for 游戏状态
/// </summary>
public class 游戏状态
{
	public 游戏状态()
	{
		//
		// TODO: Add constructor logic here
		//
	}

    protected 玩家队列 list;
    public 玩家队列 List
    {
        get
        {
            return list;
        }
        set
        {
            list = value;
            foreach(玩家 player in value.ToArray)
            {
                if (!state.ContainsKey(player))
                {
                    state.Add(player, new 玩家状态());
                }
            }
        }
    }

    protected Dictionary<玩家, 玩家状态> state = new Dictionary<玩家, 玩家状态>();

    public em状态 GetState(玩家 player)
    {
        return state[player].state;
    }

    public em状态 GetState()
    {
        return state[List.Current].state;
    }

    public void SetState(玩家 player, em状态 stats)
    {
        state[player].state = stats;
    }

    public void SetState(em状态 stats)
    {
        state[List.Current].state = stats;
    }
}

public class 说故事状态 : 游戏状态
{
    public string story = string.Empty;
    public int checkNum = 0;
}

public class 中断状态 : 游戏状态
{
    public string card = string.Empty;
    public int checkNum = 0;
}

public class 玩家状态
{
    public 玩家 player;
    public em状态 state = em状态.None;
}
