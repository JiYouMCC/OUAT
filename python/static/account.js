//denpendency: Cookies Jquery
// 账号相关
// 前有抓鬼， 后有ouat， 谁知到会不会还有其他的要重用这套
// 关于token，主要是给socket的时候用的
var account = {
  handleError: function(error) {
    console.log(error);
  },
  user: {
    uid: {
      _uid: null,
      get: function() {
        return account.user.uid._uid;
      }
    },
    get: function(callback) {
      $.ajax('/account/get_status/', {
        type: 'POST',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        success: function(data, status, xhr) {
          if (data.result) {
            account.user.nickname._nickname = data.nickname;
            account.user.uid._uid = data.uid;
          }
          callback(data);
        },
        error: function(jqXhr, textStatus, errorMessage) {
          account.user.nickname._nickname = null;
          account.user.uid._uid = null;
          account.handleError(errorMessage);
          callback(undefined);
        }
      });
    },
    login: function(username, password, callback) {
      $.ajax('/account/login/', {
        type: 'POST',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
          username: username,
          password: password,
        },
        success: function(data, status, xhr) {
          if (data.result) {
            account.user.nickname._nickname = data.nickname;
            account.user.uid._uid = data.uid;
          }
          callback(data);
        },
        error: function(jqXhr, textStatus, errorMessage) {
          account.user.nickname._nickname = null;
          account.user.uid._uid = null;
          account.handleError(errorMessage)
          callback(undefined);
        }
      });
    },
    logout: function(callback) {
      $.ajax('/account/logout/', {
        type: 'POST',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        success: function(data, status, xhr) {
          account.user.nickname._nickname = null;
          account.user.uid._uid = null;
          callback(data);
        },
        error: function(jqXhr, textStatus, errorMessage) {
          account.handleError(errorMessage)
          account.user.nickname._nickname = null;
          account.user.uid._uid = null;
          callback(undefined);
        }
      });
    },
    register: function(username, nickname, password, callback) {
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
            account.user.nickname._nickname = data.nickname;
            account.user.uid._uid = data.uid;
          }
          callback(data);
        },
        error: function(jqXhr, textStatus, errorMessage) {
          account.handleError(errorMessage)
          callback(undefined);
        }
      });
    },
    nickname: {
      _nickname: null,
      get: function() {
        return account.user._nickname
      },
      set: function(nickname, callback) {
        $.ajax('/account/change_nickname/', {
          type: 'POST',
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          },
          data: {
            nickname: nickname
          },
          success: function(data, status, xhr) {
            if (data.result) {
              account.user.nickname._nickname = data.nickname;
              account.user.uid._uid = data.uid;
            }
            callback(data);
          },
          error: function(jqXhr, textStatus, errorMessage) {
            account.handleError(errorMessage)
            callback(undefined);
          }
        });
      }
    }
  }
}