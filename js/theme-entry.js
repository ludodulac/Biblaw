(() => {
  const $ = id => document.getElementById(id);
  const identity = $('themeEntryIdentity');
  const name = $('themeEntryName');
  const count = $('themeEntryCount');
  const heading = $('documentResultsTitle');
  const importanceHelp = $('themeImportanceHelp');
  if (!identity || !name || !count || !heading || !importanceHelp) return;

  const hideIdentity = () => {
    identity.hidden = true;
    importanceHelp.hidden = true;
    importanceHelp.open = false;
    heading.textContent = 'Résultats';
  };

  document.addEventListener('biblaw:presentation-state', event => {
    const detail = event.detail || {};
    if (detail.kind !== 'canonical-theme' || !detail.theme?.id || !detail.theme?.label) {
      hideIdentity();
      return;
    }

    name.textContent = detail.theme.label;
    const psalmCount = Number(detail.psalmCount) || 0;
    count.textContent = `${psalmCount} psaume${psalmCount > 1 ? 's' : ''} indexé${psalmCount > 1 ? 's' : ''}`;
    heading.textContent = 'Textes indexés pour ce thème';
    identity.hidden = false;
    importanceHelp.hidden = false;
  });

  hideIdentity();
})();
