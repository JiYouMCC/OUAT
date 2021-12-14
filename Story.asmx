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
    /// ���˵����
    /// </summary>
    /// <param name="playerSession">���Session�������ж���Ҷ���</param>
    /// <param name="card">���¿�Ƭ</param>
    /// <param name="story">���Ҫ˵�Ĺ���</param>
    [WebMethod]
    public string SayStory(int playerSession, string card, string stroy)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        return ��Ϸ.Instance.SayStory(player, card, stroy);
    }


    /// <summary>
    /// �ж����˵�Ĺ���
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="card"></param>
    /// <param name="reason"></param>
    [WebMethod]
    public string CutStory(int playerSession, string card, string reason)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        return ��Ϸ.Instance.CutStory(player, card, reason);
    }

    /// <summary>
    /// ͬ�����˵�Ĺ���
    /// ͬ���ͬʱ��ʾ�Լ�û��Ҫ���ƿ��Խ����ж�
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="agree"></param>
    /// <param name="reason">����ʱҪ˵������</param>
    [WebMethod]
    public string AgreeStory(int playerSession, bool agree, string reason)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        return ��Ϸ.Instance.AgreeStory(player, agree, reason);
    }

    /// <summary>
    /// �Ƿ�ͬ��ǰ����ҵ��ж�����
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="agree"></param>
    /// <param name="reason"></param>
    [WebMethod]
    public string AgreeCut(int playerSession, bool agree, string reason)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        return ��Ϸ.Instance.AgreeCutStory(player, agree, reason);
    }

    [WebMethod]
    public string Hellow(string str)
    {
        return str;
    }

    /// <summary>
    /// ��������¼
    /// </summary>
    /// <param name="playerSession"></param>
    /// <param name="charIndex"></param>
    /// <returns></returns>
    [WebMethod]
    public string GetChat(int playerSession)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        StringList ServerChar = ��Ϸ.Instance.Chats;
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
    /// ��ҵ�¼������SessionID
    /// </summary>
    /// <param name="name"></param>
    /// <param name="password"></param>
    /// <returns></returns>
    [WebMethod]
    public int Login(string name, string password)
    {
        ��� player = ��Ϸ.Instance.players[name];
        if (player == null)
        {
            player = new ���();
            player.���� = name;
            ��Ϸ.Instance.players.Add(player);
            ��Ϸ.Instance.Chats.Add(string.Format("���{0}��¼��\r\n", name)); 
        } 
        
        // ����Ѿ���¼����ֱ�ӷ���SessionID
        return ��Ϸ.Instance.players.IndexOf(player);
    }


    [WebMethod]
    public void Logout(string name)
    {
        ��� player = ��Ϸ.Instance.players[name];
        if (player != null)
        {
            ��Ϸ.Instance.players.Remove(player);
        } 
    }
        
    /// <summary>
    /// ��ʼ����Ϸ
    /// </summary>
    [WebMethod]
    public void BeginGame()
    {
        ��Ϸ.Instance.BeginGame(); 
    }


    [WebMethod]
    public string[] GetCard(int playerSession)
    {
        ��� player = ��Ϸ.Instance.players[playerSession];
        if (player == null)
            return new string[0];
        return player.Ҫ����.ToArray(); 
    }

    /// <summary>
    /// ��õ�ǰ������ҵ�״̬
    /// </summary>
    /// <returns></returns>
    [WebMethod]
    public string GetPlayerState()
    {
        StringBuilder sb = new StringBuilder(); 
        foreach (��� player in ��Ϸ.Instance.players.ToArray)
        {
            em״̬ state = ��Ϸ.Instance.GetState(player);
            string format =  "{0}[{1}]<br>";
            if (state == em״̬.WaitCheckCutStory || state == em״̬.WaitCheckStory || state == em״̬.WaitSayStory)
                format = "{0}[{1}]*<br>";  
            sb.AppendLine(string.Format(format, player.����, player.Ҫ����.Count));
        }
        return sb.ToString();
    }     
}

