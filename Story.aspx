<%@ Page Language="C#" AutoEventWireup="true" CodeFile="Story.aspx.cs" Inherits="StoryPage" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<script language="javascript">

var showSayStory; 
var showCutStory;
var showAgreeCut;

function CallPlayer()
{
       //  轮到玩家的时候，将IE设置为焦点，提醒玩家
       var panelSayStory = document.all['PanelSayStory'];
       if (panelSayStory == undefined)
      {
           showSayStory = false;
      }
      else
      {
            if (!showSayStory)
            {
               window.focus();
               window.parent.focus();
               showSayStory = true; 
            }
      }
  
      var panelCutStory = document.all['PanelAngreeStory'];
      if (panelCutStory == undefined)
      {
            showCutStory = false;
      }
      else
      {
            if (!showCutStory)
            {
                window.focus();
                showCutStory = true; 
            }
      }
      
      var panelAgreeCut = document.all['panelCutStory'];
      if (panelAgreeCut == undefined)
      {
            showAgreeCut = false;
      }
      else
      {
            if (!showAgreeCut)
            {
                window.focus();
                showAgreeCut = true; 
            }
      }
  
}


function OnGetPlayerState(ret)
{
    var msg = document.all['DivPlayer'];
    msg.innerHTML = ret; 
   window.setTimeout(GetPlayerState, 1000*2); 
}

function OnGetPlayerStateTimeout(ret)
{
    window.setTimeout(GetPlayerState, 1000*2);
}

function GetPlayerState()
{
    Story.GetPlayerState(OnGetPlayerState, OnGetPlayerStateTimeout);
}
 
  function OnGetChatComplete(ret)
  {
    var msg = document.all['uiMsg'];
    
    if (ret != '') 
   { 
        msg.innerHTML += ret;
        document.all['DivMsg'].scrollTop = msg.scrollHeight+5000; 
    }
   
   CallPlayer();  
   window.setTimeout(GetChat, 1000*1);
  }
  
  function OnGetChatTimeOut(ret)
  {
    window.setTimeout(GetChat, 1000*1);
  }
  
  function GetChat()
  {
    var ps = document.all['PlayerSession'].value;
    Story.GetChat(ps, OnGetChatComplete, OnGetChatTimeOut);
  }
  
  function page_load()
  {
    GetChat();
    GetPlayerState(); 
  }

</script>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server" id="head">
    <title>狗狗OUAT在线游戏平台</title>
</head>
<body onload="page_load()">
    <form id="form1" runat="server">
        
            <asp:ScriptManager ID="ScriptManager1" runat="server">
            <Services>
            <asp:ServiceReference  Path="Story.asmx"/> 
            </Services> 
            </asp:ScriptManager>
            <table style="width: 100%;">
                <tr>
                    <td style="width: 200px; height: 453px; background-color:#ffccff;">
                        <div style="width: 100%; height: 100%; background-color: #ffccff; font-size:18px;" id="DivPlayer"></div>
                        &nbsp;<!--<a href="Manage.aspx">管理</a> -->
                            
                    </td>
                    <td style="height: 453px;background-color: #ffff99;" >
                        <div style="width: 100%; height: 100%; background-color: #ffff99; overflow:auto; word-wrap:break-word;word-break:break-all;font-size:18px;" id="DivMsg" >
                        <ul id="uiMsg">
                        </ul>
                        </div>
            <asp:UpdatePanel ID="UpdatePanel1" runat="server" UpdateMode="Conditional">
                <ContentTemplate>
                    <asp:Panel ID="Panel1" runat="server" Height="50px">
                        <asp:TextBox ID="edt_chat" runat="server" Width="400px"></asp:TextBox>
                        <asp:Button ID="btn_chat" runat="server" Text="聊天" OnClick="btn_chat_Click" /></asp:Panel>
                </ContentTemplate>
            </asp:UpdatePanel>                           
                    </td>
                </tr>
            </table>            
        <asp:UpdatePanel ID="UpdatePanelMain" runat="server" UpdateMode="Conditional">
            <ContentTemplate>
            <asp:HiddenField ID="PlayerSession" runat="server" Value="0" />
                <table>
                	<tr>
                		<td style="width: 800px">
                			<asp:Panel id="PanelEnd" runat="server" >结局卡：
                    			<asp:BulletedList ID="BulletedList2" runat="server" style="direction: ltr; text-indent: 20px; line-height: normal; text-align: left" BulletStyle="Square">
                    			</asp:BulletedList>
           					</asp:Panel>
                		</td>
                	</tr>
                    <tr>
                        <td style="width: 200px">
           					<asp:Panel id="PanelCard" runat="server" >要素牌：
                    			<asp:BulletedList ID="BulletedList1" runat="server" style="direction: ltr; text-indent: 20px; line-height: normal; text-align: left" BulletStyle="Square">
                    			</asp:BulletedList>
           					</asp:Panel>              
                        </td>
                    </tr>
                </table>

                <table align="left">
                    <tr>
                        <td style="width: 600px">
                        <asp:Panel ID="PanelSayStory" runat="server" Width="600px">说故事：</td></tr>
                    <tr>                     
                            <td style="width: 460px">
                                <asp:TextBox ID="edt_Story" runat="server" Height="75px" Width="460px" TextMode="MultiLine"></asp:TextBox></td></tr>
                    <tr>
                            <td style="width: 200px">
                            	<asp:DropDownList ID="ddl_Saycard" runat="server"></asp:DropDownList>
                            	<asp:Button ID="btn_SayStory" runat="server" Text="确认" OnClick="btn_SayStory_Click" /></asp:Panel>
                            </td>
                    </tr>                   
                </table>                
                <asp:Panel ID="PanelAgreeStory" runat="server" Height="100px" Width="600px">
                    中断故事<br />
                    <table>
                        <tr>
                            <td style="width: 63px">
                                <asp:RadioButton ID="rb_AgreeStory" runat="server" Checked="True" Text="有效" GroupName="StoryAgree" /></td>
                            <td style="width: 67px">
                                <asp:RadioButton ID="rb_cut" runat="server" Text="中断" GroupName="StoryAgree" />
                            </td>
                            <td style="width: 67px">
                                <asp:RadioButton ID="rb_UnAgreeStory" runat="server" Text="无效" GroupName="StoryAgree" /></td>
                            <td style="width: 100px">
                            </td>
                        </tr>
                        <tr>
                            <td colspan="3" rowspan="2">
                                <asp:TextBox ID="edt_CutStory" runat="server" Height="75px" Width="460px" TextMode="MultiLine"></asp:TextBox></td>
                            <td align="left" rowspan="2" style="width: 100px">
                                <asp:DropDownList ID="ddl_cutcard" runat="server">
                                </asp:DropDownList><asp:Button ID="btn_cutStory" runat="server" Text="确认" OnClick="btn_cutStory_Click" /></td>
                        </tr>
                        <tr>
                        </tr>
                    </table>
                </asp:Panel>
                <asp:Panel ID="PanelAgreeCutStory" runat="server" Height="100px" Width="600px">
                    中断确认<br />
                    <table>
                        <tr>
                            <td style="width: 100px">
                                <asp:RadioButton ID="rb_Cutagree" runat="server" Checked="True" Text="有效" GroupName="cutagree" /></td>
                            <td style="width: 100px">
                                <asp:RadioButton ID="rb_UnCutAngree" runat="server" Text="无效" GroupName="cutagree" /></td>
                            <td style="width: 100px">
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2" rowspan="2">
                                <asp:TextBox ID="edt_UnArgeeCutStory" runat="server" Height="75px" Width="460px" TextMode="MultiLine"></asp:TextBox></td>
                            <td align="left" rowspan="2" style="width: 100px">
                                <asp:Button ID="btn_AgreeCut" runat="server" Text="确认" OnClick="btn_AgreeCut_Click" /></td>
                        </tr>
                        <tr>
                        </tr>
                    </table>
                </asp:Panel>
                        </td>
                    </tr>
                </table>
                <asp:Timer ID="Timer" runat="server" Interval="2000" OnTick="Timer_Tick">
                </asp:Timer>
            </ContentTemplate>
        </asp:UpdatePanel>
    </form>
</body>
</html>
