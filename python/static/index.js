var user_token = null;

var MESSAGES = {
    TYPE: {
        SYSTEM: 0,
        CHAT: 1,
        GAME: 2,
        PLAYER: 3,
    },
    SYSTEM_MESSAGE: {
        LEAVE: 0,
        RENAME: 1,
        REGISTER: 2,
        LOGIN: 3
    },
    SYSTEM_MESSAGE_TXT: [
        "“{0}”离开了。",
        "“{0}”改名为“{1}”。",
        "“{0}”加入了游戏。",
        "“{0}”回来了。"
    ],
    GAME_MESSAGE: {
        START: 0,
        END: 1,
        MAN_WORD: 2,
        GHOST_WORD: 3,
        MEN: 4,
        GHOST: 5,
        READY_PLAY: 6,
        READY_WHITE: 7,
        READY_OWNER: 8,
        GUESS_WORD: 9,
        GUESS_FAIL: 10,
        EXPOSE: 11,
        CONTINUE: 12,
        VOTE: 13,
        VOTE_RESULT: 14,
        VOTE_CONTINUE: 15,
        OWNER_GIVE_UP: 16,
        PLAYER_GIVE_UP: 17,
        WHITE_GIVE_UP: 18,
        OWNER_LEAVE: 19,
        PLAYER_RUN: 20,
        PLAYER_LEAVE: 21,
        WHITE_RUN: 22,
        WHITE_LEAVE: 23,
        VOTE_EARLY_KILL: 24
    },
    GAME_MESSAGE_TXT: [
        "游戏开始了，请大家确认自己发到的词！现在场上出现了{0}个鬼，它们和{1}个人混在一起，但是谁都不知道自己是人还是鬼，大家加油把它们抓出来吧！",
        "游戏结束, {0}赢了！",
        "人词：{0}",
        "鬼词：{0}",
        "人：{0}",
        "鬼：{0}",
        "“{0}”要抓鬼！",
        "“{0}”要当小白！",
        "“{0}”已经提交了词，要当法官。",
        "小白“{0}”猜人词是“{1}”。",
        "天雷滚滚，一道闪电把小白“{0}”劈死了……",
        "“{0}”发出了一声嚎叫，筋脉尽断，自爆而亡！",
        "游戏继续进行。",
        "“{0}”指认“{1}”是鬼！",
        "“{0}”就这么被投死了，那么问题来了，Ta到底是不是鬼呢？",
        "大家争吵很激烈，不能确定谁是鬼，本次投票作废。",
        "“{0}”不当法官了。",
        "“{0}”不玩了。",
        "“{0}”不当小白了。",
        "法官“{0}”很无聊，走了。",
        "玩家“{0}”逃跑了，Ta在逃跑的路上被活活呸死~~",
        "玩家“{0}”拖着自己的尸体走了……",
        "小白“{0}”放弃了……",
        "小白“{0}”拖着自己的尸体走了……",
        "“{0}”已经被超过半数的人指认为鬼了，本着人/鬼道主义减轻Ta的痛苦，提前让Ta上路了……",
    ]
}

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

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


$.ajax('/account/get_status/', {
    type: 'POST',
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
    },
    success: function(data, status, xhr) {
        if (data.result) {
            $("#button_login").button('reset');
            $("#modal_login").modal('hide');
            $("#menu_online").hide();
            $("#menu_update_display_name").text(data.nickname);
            $("#button_logout").show();
            $("#change_nickname").val(data.nickname);
            user_token = data.token;
            chatSocket.send(JSON.stringify({
                'sender': $("#change_nickname").val(),
                'text': 'login',
                'type': 'system',
                'token': user_token
            }));
        }
    },
    error: function(jqXhr, textStatus, errorMessage) {
        $("#button_login").button('reset');
        console.log(errorMessage);
    }
});

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
        return;
    }
    var nickname = $("#register_nickname").val();
    $.ajax('/account/register/', {
        type: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            username: username,
            password: password,
            nickname: nickname
        },
        success: function(data, status, xhr) {
            if (data.result) {
                $("#button_register").button('reset');
                $("#modal_register").modal('hide');
                $("#menu_online").hide();
                $("#menu_update_display_name").text(data.nickname);
                $("#button_logout").show();
                $("#change_nickname").val(data.nickname);
                user_token = data.token;
            } else {
                alert("注册失败！");
            }
        },
        error: function(jqXhr, textStatus, errorMessage) {

        }
    });
});

// 登录
$("#menu_login").click(function() {
    $("#modal_login").modal('show');
});

$("#button_login").click(function() {
    $("#button_login").button('loading');
    $.ajax('/account/login/', {
        type: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            username: $("#login_username").val(),
            password: $("#login_password").val()
        },
        success: function(data, status, xhr) {
            if (data.result) {
                $("#button_login").button('reset');
                $("#modal_login").modal('hide');
                $("#menu_online").hide();
                $("#menu_update_display_name").text(data.nickname);
                $("#button_logout").show();
                $("#change_nickname").val(data.nickname);
                user_token = data.token;
                chatSocket.send(JSON.stringify({
                    'sender': $("#change_nickname").val(),
                    'text': 'login',
                    'type': 'system',
                    'token': user_token
                }));
            } else {
                alert("登录失败！");
            }
        },
        error: function(jqXhr, textStatus, errorMessage) {
            $("#button_login").button('reset');
            console.log(errorMessage);
        }
    });
});

// 登出
$("#menu_logout").click(function() {
    $.ajax('/account/logout/', {
        type: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        success: function(data, status, xhr) {
            if (data.result) {
                $("#button_logout").hide();
                $("#menu_online").show();
                chatSocket.send(JSON.stringify({
                    'sender': $("#change_nickname").val(),
                    'text': 'logout',
                    'type': 'system',
                    'uid': data.uid
                }));
            }
        },
        error: function(jqXhr, textStatus, errorMessage) {

        }
    });
});

// 修改昵称
$("#menu_update_display_name").click(function() {
    $("#modal_update").modal('show');
});

$("#button_update_display_name").click(function() {
    $("#button_update").button('loading');
    $.ajax('/account/change_nickname/', {
        type: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            nickname: $("#change_nickname").val()
        },
        success: function(data, status, xhr) {
            $("#button_update").button('reset');
            $("#menu_update_display_name").text(data.nickname);
            $('#modal_update').modal('hide');
        },
        error: function(jqXhr, textStatus, errorMessage) {
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

// ------------------------编辑分割线-----------------



chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    addMessage(data, "#messages")
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

$("#button_chat").click(function() {
    chatSocket.send(JSON.stringify({
        'sender': $("#change_nickname").val(),
        'text': $("#chat").val(),
        'color': $("#input_color").val(),
        'token': user_token
    }));
    $("#chat").val("");
    $("#chat").focus();
});

function formatDate(date) {
    return ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2) + ":" + ("0" + date.getSeconds()).slice(-2) + " ";
}

function addMessage(messageInfo, elementId) {
    var date = messageInfo.datetime;
    var message = messageInfo.text;
    var dateTime = new Date(parseInt(date));
    var userDisplay = messageInfo.sender;
    var color = messageInfo.color;
    var messageType = messageInfo.type;
    var commandText = ''
    if (messageType == "system") {
        if (message == "login") {
            commandText = userDisplay + "加入了游戏。"
        } else {
            commandText = userDisplay + "离开了。"
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