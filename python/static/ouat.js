//依赖项: jquery, cookie,account
var ouat = {
    init: function(messageSocketOnMessage,
        messageSocketOnClose) {
        ouat.hall.message._messageSocket.onmessage = messageSocketOnMessage;
        ouat.hall.message._messageSocket.onclose = messageSocketOnClose;
    },
    handleError: function(error) {
        console.log(error);
    },
    hall: {
        users: {
            add: function(callback) {
                $.ajax('/hall/add_user/', {
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken')
                    },
                    success: function(data, status, xhr) {
                        if (data.result) {
                            if (callback) {
                                callback(data);
                            }
                        } else {
                            if (callback) {
                                callback(undefined);
                            }
                        }
                    },
                    error: function(jqXhr, textStatus, errorMessage) {
                        ouat.handleError(errorMessage)
                        callback(undefined);
                    }
                });
            },
            remove: function(uid, callback) {
                $.ajax('/hall/remove_user/', {
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken')
                    },
                    data: {
                        uid: uid
                    },
                    success: function(data, status, xhr) {
                        if (data.result) {
                            if (callback) {
                                callback(data);
                            }
                        } else {
                            if (callback) {
                                callback(undefined);
                            }
                        }
                    },
                    error: function(jqXhr, textStatus, errorMessage) {
                        ouat.handleError(errorMessage)
                        if (callback) {
                            callback(undefined);
                        }
                    }
                });
            },
            get: function(callback) {
                $.ajax('/hall/users/', {
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken')
                    },
                    success: function(data, status, xhr) {
                        if (data.result) {
                            if (callback) {
                                callback(data);
                            }
                        } else {
                            if (callback) {
                                callback(undefined);
                            }
                        }
                    },
                    error: function(jqXhr, textStatus, errorMessage) {
                        ouat.handleError(errorMessage)
                        if (callback) {
                            callback(undefined);
                        }
                    }
                });
            }
        },
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

    }
}