(() => {
  const $ = id => document.getElementById(id);
  const panel = $('validatedRelationsPanel');
  const choices = $('validatedRelationChoices');
  if (!panel || !choices) return;
  const norm = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/œ/g, 'oe').replace(/æ/g, 'ae').replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ').replace(/-/g, ' ').replace(/\s+/g, ' ').trim();
  const esc = value => String(value || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  let relationPayload = null;
  let themesById = new Map();
  const relationMeta = (relation, currentThemeId) => {
    const fromSource = currentThemeId === relation.sourceThemeId;
    if (relation.relationType === 'equivalent_to') return 'Relation validée · thème équivalent';
    if (relation.relationType === 'related_to') return 'Relation thématique validée';
    if (relation.relationType === 'variant_of') return fromSource ? 'Relation validée · formulation de référence proche' : 'Relation validée · variante';
    if (relation.relationType === 'broader_than') return fromSource ? 'Relation validée · thème plus précis' : 'Relation validée · thème plus général';
    if (relation.relationType === 'component_of') return fromSource ? 'Relation validée · ensemble auquel ce thème appartient' : 'Relation validée · composante';
    return 'Relation validée';
  };
  const themeIdsForQuery = value => { const query = norm(value); if (!query) return []; const ids = []; for (const theme of themesById.values()) if (query === norm(theme.label) || query === norm(theme.id)) ids.push(theme.id); return ids; };
  const render = () => {
    if (!relationPayload || $('modeExact')?.classList.contains('active') || norm($('query2')?.value)) { panel.hidden = true; return; }
    const currentIds = new Set(themeIdsForQuery($('query')?.value)); if (!currentIds.size) { panel.hidden = true; return; }
    const seen = new Set(), related = [];
    for (const relation of relationPayload.relations || []) {
      let currentThemeId = null, otherThemeId = null;
      if (currentIds.has(relation.sourceThemeId)) { currentThemeId = relation.sourceThemeId; otherThemeId = relation.targetThemeId; }
      else if (currentIds.has(relation.targetThemeId)) { currentThemeId = relation.targetThemeId; otherThemeId = relation.sourceThemeId; }
      if (!otherThemeId || currentIds.has(otherThemeId) || seen.has(`${otherThemeId}:${relation.relationType}`)) continue;
      const theme = themesById.get(otherThemeId); if (!theme) continue;
      seen.add(`${otherThemeId}:${relation.relationType}`); related.push({ theme, meta: relationMeta(relation, currentThemeId) });
    }
    if (!related.length) { panel.hidden = true; return; }
    choices.innerHTML = related.map(({theme, meta}) => `<button class="sense-button" data-validated-theme-id="${esc(theme.id)}"><strong>${esc(theme.label)}</strong><span>${esc(meta)}</span></button>`).join('');
    choices.querySelectorAll('[data-validated-theme-id]').forEach(button => { button.onclick = () => { const theme = themesById.get(button.dataset.validatedThemeId); if (!theme) return; $('query').value = theme.label; $('query2').value = ''; $('modeThemes')?.click(); $('searchButton')?.click(); window.scrollTo({top: 0, behavior: 'smooth'}); }; });
    panel.hidden = false;
  };
  async function load() {
    try {
      const [relations, directory] = await Promise.all([
        fetch('data/thematic-index/theme-relations-public.json').then(r => { if (!r.ok) throw Error('theme-relations-public'); return r.json(); }),
        fetch('data/thematic-index/theme-directory-public.json').then(r => { if (!r.ok) throw Error('theme-directory-public'); return r.json(); })
      ]);
      if (relations.presentationOnly !== true || relations.publicSearchEffect !== false) throw Error('unsafe-theme-relations-public');
      relationPayload = relations; themesById = new Map((directory.themes || []).map(theme => [theme.id, theme])); render();
    } catch (error) { console.error(error); panel.hidden = true; }
  }
  $('searchButton')?.addEventListener('click', () => setTimeout(render, 0));
  $('query')?.addEventListener('keydown', event => { if (event.key === 'Enter') setTimeout(render, 0); });
  $('query2')?.addEventListener('keydown', event => { if (event.key === 'Enter') setTimeout(render, 0); });
  $('modeThemes')?.addEventListener('click', () => setTimeout(render, 0));
  $('modeExact')?.addEventListener('click', () => setTimeout(render, 0));
  document.addEventListener('click', event => { if (event.target.closest('[data-related-theme], [data-directory-theme], [data-transverse-theme]')) setTimeout(render, 0); });
  load();
})();
