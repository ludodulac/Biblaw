(() => {
  const panel = document.getElementById('themeRubricsPanel');
  const list = document.getElementById('themeRubricList');
  if (!panel || !list) return;

  let activeThemeId = null;
  let rubrics = [];

  const hide = () => {
    panel.hidden = true;
    list.innerHTML = '';
  };

  const resultCardFor = recordId => {
    const button = [...document.querySelectorAll('[data-open]')].find(candidate => candidate.dataset.open === recordId);
    return button ? button.closest('.result-card') : null;
  };

  const render = () => {
    if (!activeThemeId || !rubrics.length) return hide();
    const themeRubrics = rubrics.filter(rubric => rubric.themeId === activeThemeId);
    const rendered = [];

    for (const rubric of themeRubrics) {
      const records = rubric.recordIds
        .map(recordId => ({ recordId, card: resultCardFor(recordId) }))
        .filter(entry => entry.card)
        .map(entry => ({
          recordId: entry.recordId,
          title: entry.card.querySelector('h3')?.textContent?.trim() || entry.recordId,
        }));
      if (!records.length) continue;
      rendered.push({ rubric, records });
    }

    if (!rendered.length) return hide();

    list.innerHTML = rendered.map(({ rubric, records }) => `
      <article class="theme-rubric" data-rubric-id="${rubric.rubricId}">
        <div class="theme-rubric-heading">
          <h3>${rubric.label}</h3>
          <span class="muted">${records.length} psaume${records.length > 1 ? 's' : ''}</span>
        </div>
        <div class="theme-rubric-links">
          ${records.map(record => `<button class="theme-rubric-link" data-rubric-record-id="${record.recordId}">${record.title}</button>`).join('')}
        </div>
      </article>
    `).join('');

    list.querySelectorAll('[data-rubric-record-id]').forEach(button => {
      button.onclick = () => {
        const card = resultCardFor(button.dataset.rubricRecordId);
        if (!card) return;
        card.scrollIntoView({ behavior: 'smooth', block: 'start' });
        const sourceButton = card.querySelector('[data-open]');
        if (sourceButton) sourceButton.focus({ preventScroll: true });
      };
    });
    panel.hidden = false;
  };

  document.addEventListener('biblaw:presentation-state', event => {
    const detail = event.detail || {};
    if (detail.kind !== 'canonical-theme' || !detail.theme?.id) {
      activeThemeId = null;
      hide();
      return;
    }
    activeThemeId = detail.theme.id;
    window.setTimeout(render, 0);
  });

  fetch('data/thematic-index/theme-rubrics-public.json')
    .then(response => {
      if (!response.ok) throw Error('theme-rubrics-public');
      return response.json();
    })
    .then(data => {
      rubrics = Array.isArray(data.rubrics) ? data.rubrics : [];
      render();
    })
    .catch(error => {
      console.error(error);
      rubrics = [];
      hide();
    });

  hide();
})();
