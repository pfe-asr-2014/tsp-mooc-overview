// Table hack on narrow screen
(function(){
  if(window.innerWidth <= 767) {
    function forEach(array, func) {
      Array.prototype.forEach.call(array, func);
    }

    var tables = document.getElementsByTagName('table');
    forEach(tables, function(table){
      var headers = [];

      forEach(table.getElementsByTagName('th'), function(th){
        headers.push(th.textContent);
      });

      var i = 0, l = headers.length;
      forEach(table.getElementsByTagName('td'), function(td){
        td.dataset.title = headers[i%l];
        i++;
      });
    });
  }
})();
