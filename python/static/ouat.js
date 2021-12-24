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
            sendGame: function(from, to, text, detail, elementCard, EndingCard, callback) {
                ouat.hall.message._messageSocket.send(JSON.stringify({
                    'sender': from,
                    'receiver': to,
                    'text': text,
                    'detail': detail,
                    'elementCard': elementCard,
                    'EndingCard':EndingCard,
                    'type':'game'
                }));
                if (callback) {
                    callback();
                }
            }
        }
    },
    game: {
        players: {
            add:function(callback){
                ouat.hall.message.sendGame(
                    account.user.uid.get(), 
                    null, 
                    'attend', 
                    null, 
                    null, 
                    null, 
                    callback
                );
            },
            remove:function(){},
            get:function(){}
        },
    }
}