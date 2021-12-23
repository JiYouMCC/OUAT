//依赖项: jquery, cookie,account
var ouat = {
    init: function(messageSocketOnMessage,messageSocketOnClose) {
        ouat.hall.message._messageSocket.onmessage = messageSocketOnMessage;
        ouat.hall.message._messageSocket.onclose = messageSocketOnClose;
    },
    handleError: function(error) {
        console.log(error);
    },
    hall: {
        message: {
            _messageSocket: new WebSocket('ws://' + window.location.host + '/ws/chat/'),
            sendChat: function(from, to, message, color, callback) {
                ouat.hall.message._messageSocket.send(JSON.stringify({
                    'sender': from,
                    'receiver': to,
                    'text': message,
                    'color': color
                }));
                if (callback) {
                    callback();
                }
            },
            sendSystem: function(user, system, callback) {
                ouat.hall.message._messageSocket.send(JSON.stringify({
                    'sender': user,
                    'text': system,
                    'type':'system'
                }));
                if (callback) {
                    callback();
                }
            },
            sendGame: function() {

            }
        }
    },
    game: {
        players: {
            add:function(){},
            remove:function(){},
            get:function(){}
        },
    }
}