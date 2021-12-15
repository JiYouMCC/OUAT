<%@ Page Language="C#" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<script runat="server">

    protected void btn_login_Click(object sender, EventArgs e)
    {
        if (TextBox1.Text == "123")
        {
            Panel2.Visible = true;
            Panel1.Visible = false; 
        }
    }

    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
        	Panel3.Visible = false;
            Panel2.Visible = true;
            Panel1.Visible = true;             
        } 
    }

    protected void btn_BeginGame_Click(object sender, EventArgs e)
    {
        游戏.Instance.BeginGame();
        Response.Redirect("Story.aspx");
    }
    protected void btn_ResetGame_Click(object sender, EventArgs e)
    {
        游戏.Instance.ResetGame();
        Response.Redirect("Story.aspx");
    }
</script>

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title>狗狗OUAT在线平台</title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <table align=center width="600px">
            <tr>
                <td align=center>
                    <asp:Panel ID="Panel3" runat="server" Height="50px" Width="125px">
                        &nbsp;<asp:TextBox ID="TextBox1" runat="server"></asp:TextBox>
                        <asp:Button ID="btn_login" runat="server" Text="密码" OnClick="btn_login_Click" />
                    </asp:Panel>
                </td>
            </tr>
            <tr>
            	<td align=center>
                    <asp:Panel ID="Panel1" runat="server" Height="50px" Width="125px">
                        <asp:Button ID="btn_ResetGame" runat="server" Text="重置游戏" OnClick="btn_ResetGame_Click" />
                    </asp:Panel>
                </td>
                <td align=center>
                    <asp:Panel ID="Panel2" runat="server" Height="50px" Width="125px">
                        <asp:Button ID="btn_BeginGame" runat="server" Text="开始游戏" OnClick="btn_BeginGame_Click" /></asp:Panel>
                </td>
            </tr>
            <tr>
                <td align=center>
                    <asp:HyperLink ID="HyperLink1" runat="server" EnableTheming="False" EnableViewState="False"
                        NavigateUrl="~/Story.aspx">回到游戏页面</asp:HyperLink></td>
            </tr>
        </table>
    
    </div>
    </form>
</body>
</html>
