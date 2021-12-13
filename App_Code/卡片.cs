using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using Common;
using System.IO;

/// <summary>
/// Summary description for 卡片
/// </summary>
public class 卡片
{
    static string cards_file
    {
        get
        {
            return System.Web.HttpContext.Current.Server.MapPath("card.txt");
        }
    }
    static string ends_file
    {
        get
        {
            return System.Web.HttpContext.Current.Server.MapPath("end.txt");
        }
    }

    static StringList cards = new StringList();
    static 卡片()
    {
        if (!File.Exists(cards_file))
            File.CreateText(cards_file).Close();
        StreamReader sr_cards =  File.OpenText(cards_file);
        while (!sr_cards.EndOfStream)
        {
            string str = sr_cards.ReadLine().Trim();
            if (str != string.Empty)
                cards.Add(str);
        }
        if (!File.Exists(ends_file))
            File.CreateText(ends_file).Close();
        StreamReader sr_ends =  File.OpenText(ends_file);
        while (!sr_ends.EndOfStream)
        {
            string str = sr_ends.ReadLine().Trim();
            if (str != string.Empty)
                ends.Add(str);
        }
    }
    static StringList ends = new StringList();
    /*static 结局()
    {
        if (!File.Exists(ends_file))
            File.CreateText(ends_file).Close();
        StreamReader sr =  File.OpenText(ends_file);
        while (!sr.EndOfStream)
        {
            string str = sr.ReadLine().Trim();
            if (str != string.Empty)
                ends.Add(str);
        }
    }*/

    /// <summary>
    /// 已经用过的卡片
    /// </summary>
    static StringList useCards = new StringList();
    static StringList useEnds = new StringList();

    static int index_cards = 0;
    public static StringList Get要素牌(int num)
    {
        StringList ret = new StringList();
        for (int i = 0; i < num; i++)
        {
            ret.Add(GetCards());
        }
        return ret;
    }

    static public string GetCards()
    {
        string ret = string.Empty;
        while (true)
        {
            System.Random ran = new Random((int)DateTime.Now.Ticks);
            index_cards += ran.Next(cards.Count);
            if (index_cards >= cards.Count)
                index_cards -= cards.Count;
            ret = cards[index_cards];
            if (useCards.IndexOf(ret) == -1)
                break;
        }
        useCards.Add(ret);
        return ret;
    }
    
	static int index_ends = 0;
    public static StringList Get结局卡(int num)
    {
        StringList ret = new StringList();
        for (int i = 0; i < num; i++)
        {
            ret.Add(GetEnds());
        }
        return ret;
    }

    static public string GetEnds()
    {
        string ret = string.Empty;
        while (true)
        {
            System.Random ran = new Random((int)DateTime.Now.Ticks);
            index_ends += ran.Next(ends.Count);
            if (index_ends >= ends.Count)
                index_ends -= ends.Count;
            ret = ends[index_ends];
            if (useEnds.IndexOf(ret) == -1)
                break;
        }
        useEnds.Add(ret);
        return ret;
    }

}
