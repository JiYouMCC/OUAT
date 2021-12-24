// 【界面相关】
// 调整窗口大小
$(window).resize(function() {
  $("#left_pannel").height(window.innerHeight - 94);
  $("#messages").height(window.innerHeight - 265);
  $("#history_message").height(window.innerHeight - 265);
  $("#history_menu").height(window.innerHeight - 265);
});
$(window).load(function() {
  $(window).resize();
});

// 【账号相关】
// 自动登录
function updateStatus() {
  account.user.get(function(data) {
    if (data && data.result) {
      $("#button_login").button('reset');
      $("#modal_login").modal('hide');
      $("#menu_online").hide();
      $("#menu_update_display_name").text(data.nickname);
      $("#button_logout").show();
      $("#change_nickname").val(data.nickname);
      ouat.hall.message.sendSystem(account.user.uid.get(), 'online', null);
      $("#button_ready_play").show();
    }
  });
}
updateStatus();

//检测在线玩家
//TODO

//检测游戏卡片
//TODO

//检测游戏状态
//TODO

// 注册
$("#menu_register").click(function() {
  $("#modal_register").modal('show');
});

$("#button_register").click(function() {
  var username = $("#register_username").val();
  var password = $("#register_password").val();
  var password_rp = $("#register_password_rp").val();
  if (password != password_rp) {
    alert("两次密码输入不一样");
    $("#button_register").button('reset');
    return;
  }
  var nickname = $("#register_nickname").val();
  account.user.register(username, nickname, password, function(data) {
    if (data && data.result) {
      $("#button_register").button('reset');
      $("#modal_register").modal('hide');
      $("#menu_online").hide();
      $("#menu_update_display_name").text(data.nickname);
      $("#button_logout").show();
      $("#change_nickname").val(data.nickname);
      ouat.hall.message.sendSystem(account.user.uid.get(), 'online', null);
    } else {
      alert("注册失败！");
      $("#button_register").button('reset');
    }
  })
});

// 登录
$("#menu_login").click(function() {
  $("#modal_login").modal('show');
});

$("#button_login").click(function() {
  $("#button_login").button('loading');
  account.user.login(
    $("#login_username").val(),
    $("#login_password").val(),
    function(data) {
      if (data && data.result) {
        $("#button_login").button('reset');
        $("#modal_login").modal('hide');
        $("#menu_online").hide();
        $("#menu_update_display_name").text(data.nickname);
        $("#button_logout").show();
        $("#change_nickname").val(data.nickname);
        ouat.hall.message.sendSystem(account.user.uid.get(), 'online', null);
      } else {
        alert("登录失败！");
        $("#button_login").button('reset');
      }
    }
  );
});

// 登出
$("#menu_logout").click(function() {
  account.user.logout(function(data) {
    if (data && data.result) {
      console.log(data)
      $("#button_logout").hide();
      $("#menu_online").show();
      ouat.hall.message.sendSystem(data.uid, 'offline', null);
    }
  });
});

// 修改昵称
$("#menu_update_display_name").click(function() {
  $("#modal_update").modal('show');
});

$("#button_update_display_name").click(function() {
  $("#button_update").button('loading');
  account.user.nickname.set($("#change_nickname").val(), function(data) {
    if (data && data.result) {
      $("#button_update").button('reset');
      $("#menu_update_display_name").text(data.nickname);
      $('#modal_update').modal('hide');
    } else {
      alert("修改失败！");
      $("#modal_update").button('reset');
    }
  });
});

// 回车代表输入
$("#chat").keydown(function(event) {
  if (event.keyCode == 13) {
    $("#button_chat").click();
  }
});

$("#button_ready_play").click(function() {
  ouat.game.players.add()
});
// ------------------------编辑分割线-----------------

ouat.init(
  function(messagedata) {
    messagedata = JSON.parse(messagedata.data);
    if (messagedata.users) {
      updateUserList(messagedata.users);
    }
    if (messagedata.players) {
      updatePlayerList(messagedata.players);
    }
    if (messagedata.text != "user_list" ) {
      addMessage(messagedata, "#messages")
    }
  },
  function(e) {
    console.error('Chat socket closed unexpectedly');
  }
);

$("#button_chat").click(function() {
  ouat.hall.message.sendChat(
    account.user.uid.get(),
    null,
    $("#chat").val(),
    $("#input_color").val(),
    function() {
      $("#chat").val("");
      $("#chat").focus();
    }
  )

});

function formatDate(date) {
  return ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2) + ":" + ("0" + date.getSeconds()).slice(-2) + " ";
}

function updateUserList(users) {
  $("#user_list").text("");
  var count = 0;
  for (index in users) {
    user = users[index];
    var displayName = user.nickname;
    var li = $("<li></li>").addClass("list-group-item").text(displayName);
    $("#user_list").append(li);
    count += 1;
  }
  $("#online_count").text(count);
}

function updatePlayerList(users) {
  $("#gamer_list").text("");
  var count = 0;
  for (index in users) {
    user = users[index];
    var displayName = user.nickname;
    var li = $("<li></li>").addClass("list-group-item").text(displayName);
    $("#gamer_list").append(li);
    count += 1;
  }
  $("#online_count").text(count);
}

function addMessage(messageInfo, elementId) {
  console.log(messageInfo)
  var date = new Date(messageInfo.datetime);
  var message = messageInfo.text;
  var dateTime = new Date(date);
  var userDisplay = null;
  if (messageInfo.sender) {
    userDisplay = messageInfo.sender.nickname
  }
  var color = messageInfo.color;
  var messageType = messageInfo.type;
  var commandText = ''
  if (messageType == "system" || messageType == 'game') {
    if (messageInfo.users) {
      updateUserList(messageInfo.users);
    }
    if (messageInfo.players) {
      updatePlayerList(messageInfo.players);
    }
    if (message == "online") {
      commandText = userDisplay + "来了。"
    } else if (message == "offline") {
      commandText = userDisplay + "离开了。"
    } else if (message == "attend") {
      commandText = userDisplay + "举手要玩游戏。"
    }
    $(elementId).append(
      $("<div></div>").addClass("text-danger").append(
        $("<span></span>").text("【系统消息】").append(
          $("<span></span>").text(commandText)
        )
      )
    );
  } else {
    $(elementId).append($("<div></div>").append($("<span></span>").text(formatDate(dateTime) + " ")).append($("<span></span>").attr("style", "color:" + color).text(userDisplay + "：")).append($("<span></span>").attr("style", "color:" + color).text(message)));
  }
}


// ------------------------重构分割线-------------------------------
$('[data-toggle="tooltip"]').tooltip();

// 默认输入颜色
var inputColor = Cookies.get('input_color');
if (inputColor) {
  $("#input_color").val(inputColor);
}

$("#button_cancel").click(function() {
  findghost.game.out();
});

$("#button_ready_white").click(function() {
  findghost.game.role.white.ready();
});

$("#button_ready_owner").click(function() {
  $("#modal_owner").modal('show');
});

$("#button_owner_commit").click(function() {
  var manWord = $("#word_man").val();
  var ghostWord = $("#word_ghost").val();
  var error = findghost.game.words.check(manWord, ghostWord);
  if (error) {
    findghost.handleError(error);
  } else {
    findghost.game.role.owner.ready(manWord, ghostWord, function(result) {
      if (result) {
        $("#modal_owner").modal('hide');
      }
    });
  }
});

$("#button_white").click(function() {
  $("#modal_white").modal('show');
});


var playersListener = undefined;
var whitesListener = undefined;

$("#menu_rule").click(function() {
  $("#modal_rule").modal('show');
});

$("#menu_history").click(function() {
  $("#modal_history").modal('show');
  $("#history_list").text("");
  findghost.history.list(null, 500, function(list) {
    for (index in list) {
      var info = list[index];
      $("#history_list").append($("<a></a>").attr("id", "history_" + index).attr('history_id', index).addClass("list-group-item").text(info.manWord + " | " + info.ghostWord))
    }
    $("#history_list").append($("<a></a>").addClass("list-group-item").text("更多..."));
    enableHistoryClick();
  });
});

$("#button_vote").click(function() {
  findghost.game.vote.set($("#select_vote").val(), $("#select_vote option:selected").text(), function() {
    findghost.game.vote.result();
  });
});

$("#button_white_commit").click(function() {
  $("#button_white_commit").button('loading');
  findghost.game.words.guess($("#word_white").val(), function() {
    $("#button_white_commit").button('reset');
    $('#modal_white').modal('hide');
    findghost.game.status.get(function(gameStatus) {
      findghost.game.role.get(undefined, function(gameRole) {
        formStatusSetting(findghost.user.get(), gameRole, gameStatus);
      });
    });
  })
});

$("#input_color").change(function() {
  Cookies.set("input_color", $(this).val());
})