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
            // �жϹ���
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
            case em״̬.WaitSayStory:
                Timer.Enabled = false;
                PanelSayStory.Visible = true;
                if (player.Ҫ����.Count > 0)
                	ddl_Saycard.DataSource = player.Ҫ����;
                else 
                {
	                string[] three;
	                switch (player.���ξ���)
	                {
		                case 3:
	                		three = new string[]{"�����۵�һ��"};
		                	ddl_Saycard.DataSource = three;
		                	break;
		                case 2:
			               three = new string[]{"�����۵ڶ���"};
				            ddl_Saycard.DataSource = three;
				            break;
				        case 1:
			                three = new string[]{"�����۵�����"};
				            ddl_Saycard.DataSource = three;
				            break;
				        case 0:
					        three = new string[]{"˵����ְ�"};
				            ddl_Saycard.DataSource = three;
				            break;
			    	}
	                //ddl_Saycard.DataSource = three;
            	}
                break;
            case em״̬.WaitCheckStory:
                Timer.Enabled = false;
                PanelAgreeStory.Visible = true;
                ddl_cutcard.DataSource = player.Ҫ����;
                break;
            case em״̬.WaitCheckCutStory:
                Timer.Enabled = false;
                PanelAgreeCutStory.Visible = true;

                break;
        }
		//if (player.Ҫ����.Count > 0)
        	BulletedList1.DataSource = player.Ҫ����;
        //else 
        //	BulletedList1.DataSource = "˵����";
        BulletedList2.DataSource = player.��ֿ�;
        this.DataBind();

        PlayerSession.Value = game.players.IndexOf(player).ToString();
    }

    ��� player
    {
        get
        {
            object obj = Session["player"];
            if (obj == null)
                Response.Redirect("Default.aspx");
            ��� p = obj as ���;
            if (game.players.IndexOf(p) < 0)
                Response.Redirect("Default.aspx");
            return p;
        }
    }

    ��Ϸ game
    {
        get
        {
            return ��Ϸ.Instance;
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

            head.Title = player.����;
        }
    }

    protected void btn_chat_Click(object sender, EventArgs e)
    {
        if (edt_chat.Text.Trim() != string.Empty)
        {
            string str = string.Format("{0}�Դ��˵��<span  style='color:Blue'>{1}</span>", player.����, edt_chat.Text);
            game.Chats.Add(str);
            edt_chat.Text = string.Empty;
        }
    }

}
