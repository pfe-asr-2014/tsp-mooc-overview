/**
 * Setting up router and api
 */
(function(){
  var stateInfo = {
    'Running': {
      'class': 'color-green',
      'actions': ['stop', 'uninstall']
    },
    'Stopped': {
      'class': 'color-red',
      'actions': ['run', 'uninstall']
    }
  };
  function stateChanged(serviceId, state) {
    var tr = document.querySelector('#id-'+serviceId);

    var stateNode = tr.children[2];
    stateNode.setAttribute('class', stateInfo[state].class);
    stateNode.innerHTML = state;

    actions = tr.children[3].children;

    // Hide progress bar
    actions[actions.length - 1].setAttribute('class','hide');

    // Select correct actions
    for(var i = 0; i < actions.length - 1; i++) {
      var action = actions[i].getAttribute('data-action');
      if(stateInfo[state].actions.indexOf(action) < 0) {
        actions[i].setAttribute('class', 'hide');
      } else {
        actions[i].setAttribute('class', '');
      }
    }
  }

  function operationInProgress(serviceId) {
    var actions = document.querySelector('#id-'+serviceId+' > td:nth-child(4)').children;

    // Hide all actions
    for(var i = 0; i < actions.length - 1; i++) {
      actions[i].setAttribute('class', 'hide');
    }

    // Show progress bar
    actions[actions.length - 1].setAttribute('class','');
  }

  var router = new Router();
  var api = new Api(location.origin + '/api/v1/')

  router.register('run', function(serviceId){
    operationInProgress(serviceId);
    api.patch('services/'+serviceId).with({'state':'running'}).now(function(status, data){
      if(status == 200){
        stateChanged(serviceId, 'Running');
      }
    });
  });

  router.register('stop', function(serviceId){
    operationInProgress(serviceId);
    api.patch('services/'+serviceId).with({'state':'stopped'}).now(function(status, data){
      if(status == 200){
        stateChanged(serviceId, 'Stopped');
      }
    });
  });

  router.register('install', function(serviceId){
    operationInProgress(serviceId);
    api.patch('services/'+serviceId).with({'state':'stopped'}).now(function(status, data){
      if(status == 200){
        stateChanged(serviceId, 'Stopped');
      }
    });
  });

  router.register('uninstall', function(serviceId){
    operationInProgress(serviceId);
    api.patch('services/'+serviceId).with({'state':'not installed'}).now(function(status, data){
      if(status == 200){
        stateChanged(serviceId, 'Not Installed');
      }
    });
  });

  router.plantOn(window);
})();
