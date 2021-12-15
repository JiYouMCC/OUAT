// 配置CSRF
var csrftoken = Cookies.get('csrftoken');

$('[data-toggle="tooltip"]').tooltip();

// 默认输入颜色
var inputColor = Cookies.get('input_color');
if (inputColor) {
    $("#input_color").val(inputColor);
}

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

// 回车代表输入
$("#chat").keydown(function(event) {
    if (event.keyCode == 13) {
        $("#button_chat").click();
    }
});

$("#button_register").click(function() {
    var email = $("#register_email").val();
    var password = $("#register_password").val();
    var password_rp = $("#register_password_rp").val();
    if (password != password_rp) {
        alert("两次密码输入不一样");
        return;
    }
    findghost.user.register(email, password, function(user) {
        $("#button_register").button('reset');
        if (user) {
            $("#menu_update_display_name").text(findghost.user.displayName.get());
            $("#modal_register").modal('hide');
        }
    });
});

$("#menu_logout").click(function() {
    $.ajax('/logout/',{
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        success: function(data, status, xhr) {
            $("#button_logout").hide();
            $("#menu_online").show();
        },
        error: function(jqXhr, textStatus, errorMessage) {
            
        }
    });
});


$("#menu_update_display_name").click(function() {
    $("#modal_update").modal('show');
});


$("#menu_register").click(function() {
    if (!findghost.user.get()) {
        $("#modal_register").modal('show');
    }
});


$("#menu_login").click(function() {
    $("#modal_login").modal('show');
});

$("#button_login").click(function() {
    $("#button_login").button('loading');
    $.ajax('/login/',{
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            username: $("#login_username").val(),
            password: $("#login_password").val()
        },
        success: function(data, status, xhr) {
            $("#button_login").button('reset');
            $("#modal_login").modal('hide');
            $("#menu_online").hide();
            $("#menu_update_display_name").text(data.nickname);
            $("#button_logout").show()
        },
        error: function(jqXhr, textStatus, errorMessage) {
            $("#button_login").button('reset');
            console.log(errorMessage);
        }
    }
    );
});

$("#button_update_display_name").click(function() {
    $("#button_update").button('loading');
    $.ajax('/change_nickname/',{
        type: 'POST',
        headers: {'X-CSRFToken': csrftoken},
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