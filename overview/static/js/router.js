/**
 * Router Logic
 */
function Router() {
  this.actions = {};
}

Router.prototype.plantOn = function(win) {
  win.addEventListener('hashchange', this.onHashChange.bind(this));
}

Router.prototype.register = function(action, cb) {
  this.actions[action] = cb;
};

Router.prototype.route = function (params) {
  var action = params[0];
  var serviceId = params[1];

  if(this.actions[action] == undefined) {
    log('Attempt to perform undefined action `'+action+'` on service `'+serviceId+'`')
    return false;
  }

  return this.actions[action](serviceId);
};

Router.prototype.onHashChange = function() {
  var params = window.location.hash.split(':');
  log(params);
  params[0] = params[0].substr(1);
  if(params.length != 2) {
    return false;
  }

  return this.route(params);
};
