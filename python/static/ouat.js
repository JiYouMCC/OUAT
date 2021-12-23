var ouat = {
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
            sendChat: function() {

            },
            sendSystem: function() {

            },
            sendGame: function() {

            }
        }
    },
    game: {

    }
}