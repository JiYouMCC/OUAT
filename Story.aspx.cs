using System;
using System.Data;
using System.Configuration;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;

/// <summary>
/// Summary description for Story
/// </summary>
public partial class StoryPage: System.Web.UI.Page 
{
    public StoryPage()
	{
		//
		// TODO: Add constructor logic here
		//
	}

    protected void btn_SayStory_Click(object sender, EventArgs e)
    {
        string str = game.SayStory(player, ddl_Saycard.SelectedItem.Text, edt_Story.Text);
        if (str != string.Empty)
            throw new Exception(str);
        edt_Story.Text = string.Empty;
        Timer.Enabled = true;
        PanelSayStory.Visible = false;
        Timer_Tick(null, null);
    }

    protected void btn_cutStory_Click(object sender, EventArgs e)
    {
        string ret = string.Empty;
        if (rb_cut.Checked)
        {
            // 中断故事
            ret = game.CutStory(player, ddl_cutcard.SelectedItem.Text, edt_CutStory.Text);
        }
        else
        {
            ret = game.AgreeStroy(player, !rb_UnAgreeStory.Checked, edt_CutStory.Text);
        }
        if (ret  != string.Empty)
            throw new Exception(ret);

        rb_AgreeStory.Checked = true;
        rb_UnAgreeStory.Checked = false;
        rb_cut.Checked = false;

        edt_CutStory.Text = string.Empty;
        Timer.Enabled = true;
        PanelAgreeStory.Visible = false;
        Timer_Tick(null, null);
    }

    protected void btn_AgreeCut_Click(object sender, EventArgs e)
    {
        string ret = game.AgreeCutStory(player, rb_Cutagree.Checked, edt_UnArgeeCutStory.Text);
        if (ret != string.Empty)
            throw new Exception(ret);

        rb_Cutagree.Checked = true;
        rb_UnCutAngree.Checked = false;

        edt_UnArgeeCutStory.Text = string.Empty;
        Timer.Enabled = true;
        PanelAgreeCutStory.Visible = false;
        Timer_Tick(null, null);
    }
    protected void Timer_Tick(object sender, EventArgs e)
    {
        switch (game.GetState(player))
        {
            case em状态.WaitSayStory:
                Timer.Enabled = false;
                PanelSayStory.Visible = true;
                if (player.要素牌.Count > 0)
                	ddl_Saycard.DataSource = player.要素牌;
                else 
                {
	                string[] three;
	                switch (player.三段剧情)
	                {
		                case 3:
	                		three = new string[]{"三段论第一段"};
		                	ddl_Saycard.DataSource = three;
		                	break;
		                case 2:
			               three = new string[]{"三段论第二段"};
				            ddl_Saycard.DataSource = three;
				            break;
				        case 1:
			                three = new string[]{"三段论第三段"};
				            ddl_Saycard.DataSource = three;
				            break;
				        case 0:
					        three = new string[]{"说出结局吧"};
				            ddl_Saycard.DataSource = three;
				            break;
			    	}
	                //ddl_Saycard.DataSource = three;
            	}
                break;
            case em状态.WaitCheckStory:
                Timer.Enabled = false;
                PanelAgreeStory.Visible = true;
                ddl_cutcard.DataSource = player.要素牌;
                break;
            case em状态.WaitCheckCutStory:
                Timer.Enabled = false;
                PanelAgreeCutStory.Visible = true;

                break;
        }
		//if (player.要素牌.Count > 0)
        	BulletedList1.DataSource = player.要素牌;
        //else 
        //	BulletedList1.DataSource = "说三段";
        BulletedList2.DataSource = player.结局卡;
        this.DataBind();

        PlayerSession.Value = game.players.IndexOf(player).ToString();
    }

    玩家 player
    {
        get
        {
            object obj = Session["player"];
            if (obj == null)
                Response.Redirect("Default.aspx");
            玩家 p = obj as 玩家;
            if (game.players.IndexOf(p) < 0)
                Response.Redirect("Default.aspx");
            return p;
        }
    }

    游戏 game
    {
        get
        {
            return 游戏.Instance;
        }
    }
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            PanelAgreeStory.Visible = false;
            PanelAgreeCutStory.Visible = false;
            PanelSayStory.Visible = false;

            PlayerSession.Value = game.players.IndexOf(player).ToString();
            player.charIndex = 0;

            head.Title = player.名字;
        }
    }

    protected void btn_chat_Click(object sender, EventArgs e)
    {
        if (edt_chat.Text.Trim() != string.Empty)
        {
            string str = string.Format("{0}对大家说：<span  style='color:Blue'>{1}</span>", player.名字, edt_chat.Text);
            game.Chats.Add(str);
            edt_chat.Text = string.Empty;
        }
    }

}
