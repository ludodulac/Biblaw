/* Menora: two documentary directories, without unverified verse attributions. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = {items: null, loading: null, current: null};
  const modes = {
    virtues: {toggle: 'menoraVirtuesToggle', panel: 'menoraVirtuesLibrary', title: 'Les sept vertus de la menora'},
    contrary: {toggle: 'menoraContraryToggle', panel: 'menoraContraryLibrary', title: 'Les sept contre-vertus de la menora'}
  };
  function close() {
    for (const mode of Object.values(modes)) {
      $(mode.panel).hidden = true;
      $(mode.toggle).setAttribute('aria-expanded', 'false');
    }
    document.body.classList.remove('view-menora');
    state.current = null;
  }
  async function load() {
    if (state.items) return state.items;
    if (!state.loading) state.loading = fetch('data/menora-editorial-draft.json?v=001')
      .then(response => {
        if (!response.ok) throw new Error('Dossier de la menora indisponible.');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data.items) || data.items.length !== 7) throw new Error('Dossier incomplet.');
        return (state.items = data.items);
      }).finally(() => {state.loading = null;});
    return state.loading;
  }
  function render(kind, items) {
    const mode = modes[kind];
    const panel = $(mode.panel);
    const container = panel.querySelector('.menora-entries');
    container.replaceChildren();
    for (const item of items) {
      const article = document.createElement('article');
      article.className = 'menora-entry';
      const heading = document.createElement('h3');
      const dot = document.createElement('span');
      dot.className = 'menora-color';
      dot.style.backgroundColor = item.color;
      dot.setAttribute('aria-hidden', 'true');
      heading.append(dot, document.createTextNode(kind === 'virtues' ? item.virtue : item.counterVirtue));
      const summary = document.createElement('p');
      summary.textContent = kind === 'virtues' ? item.virtueSummary : item.counterSummary;
      article.append(heading, summary);
      const selectedRefs = kind === 'virtues' ? item.virtueReferences : item.counterReferences;
      if (Array.isArray(selectedRefs) && selectedRefs.length) {
        const references = document.createElement('div');
        references.className = 'menora-references';
        for (const ref of selectedRefs) {
          const link = document.createElement('button');
          link.type = 'button';
          link.className = 'faq-psalm-link';
          link.textContent = 'Lire ' + ref.recordId + ' · verset ' + ref.verses.join(', ');
          link.addEventListener('click', () => {
            if (typeof state.openPsalm === 'function') state.openPsalm(ref);
          });
          references.append(link);
        }
        article.append(references);
      }
      container.append(article);
    }
  }
  async function open(kind) {
    close();
    const mode = modes[kind];
    const panel = $(mode.panel);
    panel.hidden = false;
    document.body.classList.add('view-menora');
    $(mode.toggle).setAttribute('aria-expanded', 'true');
    state.current = kind;
    const status = panel.querySelector('.menora-status');
    status.textContent = 'Chargement…';
    try {
      const items = await load();
      if (state.current !== kind) return;
      render(kind, items);
      status.textContent = 'Premières références vérifiées dans les psaumes ; recherche documentaire encore en cours.';
    } catch (error) {
      if (state.current === kind) status.textContent = error.message;
    }
    window.scrollTo({top: 0, behavior: 'instant'});
  }
  for (const [kind, mode] of Object.entries(modes)) {
    $(mode.toggle).addEventListener('click', () => open(kind));
    $(mode.panel).querySelector('.menora-back').addEventListener('click', () => {
      close();
      window.scrollTo({top: 0, behavior: 'instant'});
      $(mode.toggle).focus({preventScroll: true});
    });
  }
  globalThis.BiblawMenora = Object.freeze({
    open, close,
    setOpenPsalm(callback) {state.openPsalm = callback;},
  });
})();
