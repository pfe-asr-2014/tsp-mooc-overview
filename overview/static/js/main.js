/**
 * Setting up router and api
 */
(function(){
  var router = new Router();
  var api = new Api(location.origin + '/api/v1/')

  router.register('run', function(serviceId){
    api.patch('services/'+serviceId).with({'state':'running'}).now();
  });

  router.register('stop', function(serviceId){
    api.patch('services/'+serviceId).with({'state':'stopped'}).now();
  });

  router.register('install', function(serviceId){
    api.patch('services/'+serviceId).with({'state':'stopped'}).now();
  });

  router.register('uninstall', function(serviceId){
    api.patch('services/'+serviceId).with({'state':'not installed'}).now();
  });

  router.plantOn(window);
})();
