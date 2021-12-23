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
                            callback(data);
                        } else {
                            callback(undefined);
                        }
                    },
                    error: function(jqXhr, textStatus, errorMessage) {
                        ouat.handleError(errorMessage)
                        callback(undefined);
                    }
                });
            },
            remove: function() {

            },
            get: function() {

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