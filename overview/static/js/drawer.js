// Side drawer
(function(){
  var drawer = document.getElementById('side-drawer');
  var mask = document.getElementById('mask-modal');

  function toggleDrawer() {
    drawer.classList.toggle('open');
    mask.classList.toggle('mask-visible');
  }

  mask.addEventListener('click', toggleDrawer);
  document.querySelector('.app-bar .hamburger').addEventListener('click', toggleDrawer);
})();
