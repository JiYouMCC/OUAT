using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;

public partial class _Default : System.Web.UI.Page 
{
    protected void Page_Load(object sender, EventArgs e)
    {

    }

    protected void btn_Login_Click(object sender, EventArgs e)
    {
        string name = edt_name.Text.Trim();
        if (name == string.Empty)
            return;
        玩家 player = 游戏.Instance.players[name];
        if (player == null)
        {
            player = new 玩家();
            player.名字 = name;
            游戏.Instance.players.Add(player);
            Session["player"] = player;
            游戏.Instance.Chats.Add(string.Format("{0}哼着小调进入游戏", name));
        }
        else
        {
            Session["player"] = player;
        }
        this.Response.Redirect("Story.aspx");
    }
}