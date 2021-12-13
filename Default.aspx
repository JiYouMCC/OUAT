<%@ Page Language="C#" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="_Default" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>狗狗OUAT在线游戏平台</title>
<script language="javascript" type="text/javascript">
<!--

function OnComplete(result)
{
    alert(result);
}

function OnTimeOut(result)
{
    alert(result);
}

function Button1_onclick() {
    Story.Hellow('abc', OnComplete, OnTimeOut);
}

// -->
</script>
</head>
<body>
    <form id="form1" runat="server">
        <asp:ScriptManager ID="ScriptManager1" runat="server" EnablePartialRendering=true>
            <Services>
                <asp:ServiceReference Path="Story.asmx"/>
            </Services>
        </asp:ScriptManager>
        <br />
        <br />
        <br />
        <div>
            <table align="center">
                <tr>
                    <td style="width: 100px" align="right">
                        用户名</td>
                    <td style="width: 100px">
                        <asp:TextBox ID="edt_name" runat="server"></asp:TextBox></td>
                    <td style="width: 100px">
                    </td>
                </tr>
                <tr>
                    <td style="width: 100px">
                    </td>
                    <td style="width: 100px">
                        <asp:Button ID="btn_Login" runat="server" OnClick="btn_Login_Click" Text="登录" /></td>
                    <td style="width: 100px">
                    </td>
                </tr>
                <tr>
                    <td style="width: 100px">
                    </td>
                    <td style="width: 100px">
                    </td>
                    <td style="width: 100px">
                    </td>
                </tr>
            </table>
        </div>
    </form>
</body>
</html>
