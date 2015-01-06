/**
 * API abstraction
 */
function Api(base) {
  this.base = base;
}

Api.prototype.patch = function(resource) {
  this.resource = resource;
  this.method = 'PATCH';
  return this;
};

Api.prototype.with = function(params) {
  this.params = params;
  return this;
};

Api.prototype.now = function(cb) {
  log('`'+this.method+' '+this.base+this.resource+'` with', this.params);

  var request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (request.readyState === 4) {
      log('response received:', request.response);
      if(cb) {
        cb(request.response);
      }
    }
  };

  request.open(this.method, this.base + this.resource);
  request.setRequestHeader('Content-Type', 'application/json');
  request.send(JSON.stringify(this.params));
};
