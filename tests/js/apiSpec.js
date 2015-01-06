describe('Api', function() {
  var api;

  beforeEach(function(){
    api = new Api('base');
  });

  it('set the base url in contructor', function() {
    expect(api.base).toBe('base');
  });

  describe('#with', function(){
    it('has a fluent API', function(){
      expect(api.with(null)).toBe(api);
    });

    it('store the given params', function(){
      expect(api.with('params').params).toBe('params');
    });
  });

  describe('#patch', function(){
    it('has a fluent API', function(){
      expect(api.patch()).toBe(api);
    });

    it('set the method as PATCH', function(){
      expect(api.patch().method).toBe('PATCH');
    });

    it('store the given resource (URL)', function(){
      expect(api.patch('res/1').resource).toBe('res/1');
    });
  });

  describe('#now', function(){
    beforeEach(function() {
      jasmine.Ajax.install();
      spyOn(window, 'log');
    });

    afterEach(function() {
      jasmine.Ajax.uninstall();
    });

    it('log the request', function(){
      api.patch('/res/1').with('params').now();
      expect(window.log).toHaveBeenCalledWith('`PATCH base/res/1` with', 'params');

      lastRequest().respondWith({'status':200});
      expect(window.log).toHaveBeenCalledWith('response received:', '');
    });

    it('make the request', function(){
      api.patch('/res/1').with('params').now();
      var req = lastRequest();

      expect(req.url).toBe('base/res/1');
      expect(req.method).toBe('PATCH');
      expect(req.params).toBe('"params"');
      expect(req.requestHeaders['Content-Type']).toBe('application/json');
    });

    it('call the given callback with the response', function(){
      var callback = jasmine.createSpy("success");

      api.patch('/res/1').with('params').now(callback);

      lastRequest().respondWith({
        "status": 200,
        "contentType": 'application/json',
        "responseText": 'awesome response'
      });
      expect(callback).toHaveBeenCalledWith('awesome response');
    });
  });
});
