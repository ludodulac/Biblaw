(() => {
  const $ = id => document.getElementById(id);
  const identity = $('themeEntryIdentity');
  const name = $('themeEntryName');
  const count = $('themeEntryCount');
  const heading = $('documentResultsTitle');
  const results = $('results');
  const query = $('query');
  const ambiguityPanel = $('ambiguityPanel');
  const suggestionKicker = $('suggestionKicker');
  if (!identity || !name || !count || !heading || !results || !query) return;

  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae').replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/-/g, ' ').replace(/\s+/g, ' ').trim();
  let ambiguousQuery = '';

  const hideIdentity = () => {
    identity.hidden = true;
    heading.textContent = 'Résultats';
  };

  const canonicalLabelsInCard = card => {
    const marker = card.querySelector('.theme-found');
    if (!marker) return [];
    const text = marker.textContent || '';
    const prefix = 'THÈME INDEXÉ · ';
    if (!text.startsWith(prefix)) return [];
    return text.slice(prefix.length).split(' · ').map(x => x.trim()).filter(Boolean);
  };

  const rememberAmbiguity = () => {
    if (ambiguityPanel && !ambiguityPanel.hidden && suggestionKicker?.textContent.trim() === 'Correspondances multiples') {
      ambiguousQuery = norm(query.value);
    }
  };

  const update = () => {
    rememberAmbiguity();
    const cards = [...results.querySelectorAll('.result-card')];
    const themeCards = cards.filter(card => card.querySelector('.theme-found'));
    const labels = new Set(themeCards.flatMap(canonicalLabelsInCard));
    const isCurrentAmbiguousQuery = Boolean(ambiguousQuery) && norm(query.value) === ambiguousQuery;
    const hasSingleResolvedTheme = cards.length > 0 && themeCards.length === cards.length && labels.size === 1 && !isCurrentAmbiguousQuery;

    if (!hasSingleResolvedTheme) {
      hideIdentity();
      return;
    }

    const canonicalLabel = [...labels][0];
    name.textContent = canonicalLabel;
    count.textContent = `${cards.length} psaume${cards.length > 1 ? 's' : ''} indexé${cards.length > 1 ? 's' : ''}`;
    heading.textContent = 'Textes indexés pour ce thème';
    identity.hidden = false;

    for (const card of themeCards) {
      const sourceButton = card.querySelector('[data-open]');
      if (sourceButton) sourceButton.textContent = 'Voir le psaume source';
    }
  };

  query.addEventListener('input', hideIdentity);
  $('modeExact')?.addEventListener('click', hideIdentity);
  $('searchButton')?.addEventListener('click', () => setTimeout(update, 0));
  query.addEventListener('keydown', event => { if (event.key === 'Enter') setTimeout(update, 0); });
  document.addEventListener('click', event => {
    if (event.target.closest('[data-related-theme], [data-directory-theme], [data-theme-id], [data-validated-theme-id]')) setTimeout(update, 0);
  });

  new MutationObserver(update).observe(results, { childList: true, subtree: true });
  if (ambiguityPanel) new MutationObserver(update).observe(ambiguityPanel, { attributes: true, childList: true, subtree: true });
  update();
})();
