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
        ��� player = ��Ϸ.Instance.players[name];
        if (player == null)
        {
            player = new ���();
            player.���� = name;
            ��Ϸ.Instance.players.Add(player);
            Session["player"] = player;
            ��Ϸ.Instance.Chats.Add(string.Format("{0}����С��������Ϸ", name));
        }
        else
        {
            Session["player"] = player;
        }
        this.Response.Redirect("Story.aspx");
    }
}