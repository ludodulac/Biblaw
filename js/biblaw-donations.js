/* Amélioration progressive : le sélecteur natif <details> fonctionne sans JS. */
(() => {
  const details = document.getElementById('donateDetails');
  const toggle = document.getElementById('donateToggle');
  if (details) {
    document.addEventListener('click', (event) => {
      if (details.open && !details.contains(event.target)) details.open = false;
    });
    document.addEventListener('keydown', (event) => {
      if (details.open && event.key === 'Escape') {
        details.open = false;
        toggle?.focus();
      }
    });
  }

  const params = new URLSearchParams(window.location.search);
  const thanks = document.getElementById('donateThanks');
  if (thanks && params.get('merci') === 'don') {
    thanks.hidden = false;
    params.delete('merci');
    const query = params.toString();
    window.history.replaceState(window.history.state, '',
      window.location.pathname + (query ? '?' + query : '') + window.location.hash);
  }
})();
