<%@ WebService Language="C#" Class="Story" %>

using System;
using System.Web;
using System.Web.Services;
using System.Web.Script.Services;
using System.Web.Services.Protocols;
using Common;
using System.Text;
using System.Collections.Generic;

[WebService(Namespace = "http://tempuri.org/")]
[WebServiceBinding(ConformsTo = WsiProfiles.BasicProfile1_1)]
[ScriptService]
public class Story  : System.Web.Services.WebService {

    /// <summary>
    /// 玩家说故事
    /// </summary>
    /// <param name="playerSession">玩家Session，用于判断玩家对象</param>
    /// <param name="card">故事卡片</param>
    /// <param name="story">玩家要说的故事</param>
    [WebMethod]
    public string SayStory(int playerSession, string card, string stroy)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        return 游戏.Instance.SayStory(player, card, stroy);
    }


    /// <summary>
    /// 中断玩家说的故事
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="card"></param>
    /// <param name="reason"></param>
    [WebMethod]
    public string CutStory(int playerSession, string card, string reason)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        return 游戏.Instance.CutStory(player, card, reason);
    }

    /// <summary>
    /// 同意玩家说的故事
    /// 同意的同时表示自己没有要素牌可以进行中断
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="agree"></param>
    /// <param name="reason">反对时要说的理由</param>
    [WebMethod]
    public string AgreeStory(int playerSession, bool agree, string reason)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        return 游戏.Instance.AgreeStory(player, agree, reason);
    }

    /// <summary>
    /// 是否同意前面玩家的中断请求
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="agree"></param>
    /// <param name="reason"></param>
    [WebMethod]
    public string AgreeCut(int playerSession, bool agree, string reason)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        return 游戏.Instance.AgreeCutStory(player, agree, reason);
    }

    [WebMethod]
    public string Hellow(string str)
    {
        return str;
    }

    /// <summary>
    /// 获得聊天记录
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="charIndex"></param>
    /// <returns></returns>
    [WebMethod]
    public string GetChat(int playerSession)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        StringList ServerChar = 游戏.Instance.Chats;
        if (ServerChar.Count > player.charIndex)
        {
            List<string> sl = ServerChar.GetRange(player.charIndex, ServerChar.Count - player.charIndex);
            StringBuilder sb = new StringBuilder();

            foreach (string str in sl)
            {
                sb.AppendLine(" <li>" + str + "</li>");
            }
            player.charIndex = ServerChar.Count; 
            return sb.ToString();
        }
        return string.Empty;
    }

    /// <summary>
    /// 玩家登录，返回SessionID
    /// </summary>
    /// <param name="name"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    [WebMethod]
    public int Login(string name, string password)
    {
        玩家 player = 游戏.Instance.players[name];
        if (player == null)
        {
            player = new 玩家();
            player.名字 = name;
            游戏.Instance.players.Add(player);
            游戏.Instance.Chats.Add(string.Format("玩家{0}登录。\r\n", name)); 
        } 
        
        // 玩家已经登录过，直接返回SessionID
        return 游戏.Instance.players.IndexOf(player);
    }


    [WebMethod]
    public void Logout(string name)
    {
        玩家 player = 游戏.Instance.players[name];
        if (player != null)
        {
            游戏.Instance.players.Remove(player);
        } 
    }
        
    /// <summary>
    /// 开始新游戏
    /// </summary>
    [WebMethod]
    public void BeginGame()
    {
        游戏.Instance.BeginGame(); 
    }


    [WebMethod]
    public string[] GetCard(int playerSession)
    {
        玩家 player = 游戏.Instance.players[playerSession];
        if (player == null)
            return new string[0];
        return player.要素牌.ToArray(); 
    }

    /// <summary>
    /// 获得当前所有玩家的状态
    /// </summary>
    /// <returns></returns>
    [WebMethod]
    public string GetPlayerState()
    {
        StringBuilder sb = new StringBuilder(); 
        foreach (玩家 player in 游戏.Instance.players.ToArray)
        {
            em状态 state = 游戏.Instance.GetState(player);
            string format =  "{0}[{1}]<br>";
            if (state == em状态.WaitCheckCutStory || state == em状态.WaitCheckStory || state == em状态.WaitSayStory)
                format = "{0}[{1}]*<br>";  
            sb.AppendLine(string.Format(format, player.名字, player.要素牌.Count));
        }
        return sb.ToString();
    }     
}

