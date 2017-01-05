/* eslint-disable */

(function() {
  function install(Vue, options) {
    var ws = new WebSocket(options.url);
    var callbacks = {
      message: []
    };

    ws.onmessage = function(event) {
      callbacks.message.forEach(function(callback) {
        var data = JSON.parse(event.data);
        callback(data["action"], data["data"]);
      });
    };

    Vue.prototype.$socket = {
      onMessage: function(callback) {
        callbacks.message.push(callback);
      },

      send: function(action, data) {
        ws.send(
          JSON.stringify({
              action: action,
              data: data
          })
        );
      }
    };
  }

  if (typeof exports == 'object') {
    module.exports = install;
  }
}());
