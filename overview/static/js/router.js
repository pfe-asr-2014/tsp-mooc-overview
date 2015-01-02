// Router

  /**
   * Router Logic
   */
  function Router() {
    this.actions = {};
  }

  Router.prototype.register = function(action, cb) {
    this.actions[action] = cb;
  };

  Router.prototype.route = function (params) {
    var action = params[0].substr(1);
    var serviceId = params[1];

    if(this.actions[action] == undefined) {
      log('Attempt to perform undefined action `'+action+'` on service `'+serviceId+'`')
      return false;
    }

    log('Performing action `' + action + '` on service `' + serviceId + '`');

    this.actions[action](serviceId);
  };

  Router.prototype.onHashChange = function() {
    var params = location.hash.split(':');
    if(params.length != 2) {
      return false;
    }

    this.route(params);
  };
