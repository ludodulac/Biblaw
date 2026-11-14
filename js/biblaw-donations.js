/* Ouverture de la fenêtre de soutien ; les paiements sont pris en charge par Stripe. */
(() => {
  const button = document.getElementById('donateToggle');
  const dialog = document.getElementById('donateDialog');
  const closeButton = document.getElementById('donateClose');
  if (!button || !dialog || !closeButton) return;

  button.addEventListener('click', () => {
    if (!dialog.open) dialog.showModal();
  });
  closeButton.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => button.focus());

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
