describe('Router', function(){
  var router;

  beforeEach(function(){
    router = new Router();
  });

  describe('#plantOn', function(){
    it('listen on hashchange', function(){
      var win = jasmine.createSpyObj('window', ['addEventListener'])

      var router = new Router();
      router.plantOn(win);
      expect(win.addEventListener).toHaveBeenCalled();
    });
  });

  describe('#register', function(){
    it('is possible to associate a function to an url', function(){
      var callback = jasmine.createSpy("success");

      router.register('route', callback);

      expect(router.actions['route']).toBe(callback);
    });
  });

  describe('#route', function(){
    it('log errors in case of an unknown action', function(){
      var logSpied = spyOn(window, 'log');
      router.route(['run','serviceId']);

      expect(logSpied).toHaveBeenCalledWith(
        'Attempt to perform undefined action `run` on service `serviceId`'
      );
    });
    it('return false if the action is unknown', function(){
      expect(router.route(['run', 'serviceId'])).toBe(false);
    });
    it('return the results of the corresponding action', function(){
      var cb = jasmine.createSpy('cb').and.returnValue(true);
      router.register('route', cb);

      expect(router.route(['route', 'serviceId'])).toBe(true);
      expect(cb).toHaveBeenCalledWith('serviceId');
    });
  });

  describe('#onHashChange', function(){
    it('parse correctly a hash of format param1:param2', function(){
      var route = spyOn(router, 'route');
      location.hash = 'run:serviceId';

      router.onHashChange();
      expect(route).toHaveBeenCalledWith(['run', 'serviceId']);
    });
    it('return the routing result if the hash format is correct', function(){
      spyOn(router, 'route').and.returnValue(true);
      location.hash = 'run:serviceId';

      expect(router.onHashChange()).toBe(true);
    });
    it('return false if the hash format is incorrect', function(){
      spyOn(router, 'route').and.returnValue(true);
      location.hash = 'malformedHash';

      expect(router.onHashChange()).toBe(false);
    });
  });
});
