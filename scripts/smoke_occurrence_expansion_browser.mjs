import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const BASE_URL = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const fixture = {
  lexical: { query: 'acclame', alt: 'acclament', exactRecordCount: 1, expandedRecordCount: 2 },
  noExpansion: 'travers',
  phrase: { query: 'temps vis', recordCount: 1 },
  theme: { query: 'sainte assemblée', recordCount: 4 },
  secondTheme: 'alliance',
  psalmNumber: '105',
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const pageErrors = [];
page.on('pageerror', error => pageErrors.push(String(error)));

const resultIds = () => page.locator('.result-card .result-summary-toggle[data-open]').evaluateAll(nodes => nodes.map(node => node.dataset.open));
async function openAllResults() {
  const toggles = page.locator('.result-card [data-toggle-result]');
  for (let i = 0; i < await toggles.count(); i++) {
    if ((await toggles.nth(i).getAttribute('aria-expanded')) !== 'true') await toggles.nth(i).click();
  }
}

try {
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => {
    const el = document.getElementById('corpusStats');
    return el && !el.textContent.includes('Chargement');
  });

  const primary = page.locator('#primarySearch');
  const themesMode = page.locator('#modeThemes');
  const exactMode = page.locator('#modeExact');
  const secondary = page.locator('#secondaryTools');
  const option = page.locator('#exactExpansionOption');
  const checkbox = page.locator('#includeWordForms');

  // A — The two primary tools are visible and Theme is the default.
  assert.equal(await primary.locator('#modeThemes').count(), 1, 'Theme selector must live in primary search');
  assert.equal(await primary.locator('#modeExact').count(), 1, 'Occurrence selector must live in primary search');
  assert.equal(await secondary.locator('#modeThemes').count(), 0, 'Secondary tools must not duplicate the mode selector');
  assert.equal(await secondary.locator('#modeExact').count(), 0, 'Secondary tools must not duplicate the mode selector');
  assert.equal(await themesMode.isVisible(), true, 'Par thème must be visible');
  assert.equal(await exactMode.isVisible(), true, 'Occurrences de mots must be visible');
  assert.equal((await themesMode.textContent()).trim(), 'Thèmes');
  assert.equal((await exactMode.textContent()).trim(), 'Mots exacts');
  assert.equal(await themesMode.evaluate(el => el.classList.contains('active')), true, 'Theme mode must be selected by default');
  assert.equal(await exactMode.evaluate(el => el.classList.contains('active')), false, 'Occurrence mode must not be default');
  assert.equal(await option.isVisible(), false, 'Lexical expansion must never appear in Theme mode by default');

  // B — "acclame" in Theme mode must not silently become occurrence results.
  await page.locator('#query').fill(fixture.lexical.query);
  await page.locator('#searchButton').click();
  assert.equal(await themesMode.evaluate(el => el.classList.contains('active')), true, 'Theme mode must remain active');
  assert.equal(await page.locator('.result-card').count(), 0, 'Theme mode must not render silent textual occurrence cards');
  assert.match(await page.locator('#results').innerText(), /Aucun thème indexé ne correspond à cette recherche/i);
  const seeOccurrences = page.locator('[data-show-text-search]');
  assert.equal(await seeOccurrences.isVisible(), true, 'Theme fallback must offer an explicit occurrence switch');
  assert.match(await seeOccurrences.textContent(), /Voir les occurrences/i);
  assert.equal(await option.isVisible(), false, 'Expansion must stay hidden until occurrence mode is explicitly selected');

  // Explicit switch to Occurrences must launch the same query.
  await seeOccurrences.click();
  assert.equal(await exactMode.evaluate(el => el.classList.contains('active')), true, 'Explicit switch must activate occurrence mode');
  assert.equal(await themesMode.evaluate(el => el.classList.contains('active')), false, 'Theme mode must deactivate');
  assert.equal(await page.locator('#advancedSearchToggle').isVisible(), false, 'Dual-theme control must not be presented in occurrence mode');
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Exact occurrence result count drifted');
  const exactIds = await resultIds();

  // C — Safe lexical expansion remains opt-in and duplicate-free.
  assert.equal(await option.isVisible(), true, 'Safe word expansion must be visible in occurrence mode');
  assert.equal(await checkbox.isChecked(), false, 'Expansion must be opt-in');
  assert.equal(await checkbox.isEnabled(), true, 'acclame must have a safe expansion');
  await checkbox.check();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.expandedRecordCount, 'Expanded result count mismatch');
  const expandedIds = await resultIds();
  assert.equal(new Set(expandedIds).size, expandedIds.length, 'Exact/expansion result duplication detected');
  assert.ok(expandedIds.some(id => !exactIds.includes(id)), 'Expansion did not add a distinct certified result');
  await openAllResults();
  const highlighted = await page.locator('.result-card .search-hit').allTextContents();
  const normalizedHits = await page.evaluate(values => values.map(globalThis.BiblawThemeEngine.norm), highlighted);
  assert.ok(normalizedHits.includes(fixture.lexical.alt), 'Certified alternative acclament was not visibly rendered');
  await checkbox.uncheck();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Unchecking must restore exact-only results');
  assert.deepEqual(await resultIds(), exactIds, 'Unchecking must restore the exact result set');

  // A word without a safe expansion must not expose the option.
  await page.locator('#query').fill(fixture.noExpansion);
  await page.locator('#searchButton').click();
  assert.equal(await option.isVisible(), false, 'A word without safe expansion must not expose lexical expansion');

  // D — Multi-word expressions remain exact-only.
  await page.locator('#query').fill(fixture.phrase.query);
  await page.locator('#searchButton').click();
  assert.equal(await option.isVisible(), false, 'A multi-word expression must not expose lexical expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.phrase.recordCount, 'Exact phrase result count drifted');

  // Search by Psalm number remains available in Theme mode.
  await themesMode.click();
  await page.locator('#query').fill(fixture.psalmNumber);
  await page.locator('#searchButton').click();
  assert.match(await page.locator('#resultCount').innerText(), /4 psaumes trouvés/i);
  assert.equal(await page.locator('.result-card').count(),4, 'Four canonical Psalms numbered 105 expected');

  // Public source filters are now in the primary search (not in secondary tools).
  assert.equal(await page.locator('#sourceScope [name=sourceType]').count(), 3,
    'Psalm, prayer and note filters must stay available');
  assert.equal(await page.locator('#sourceScope #archangelFilter').count(), 1,
    'Archangel filter must stay available');

  // E — Return to Theme mode and verify the known canonical theme presentation.
  await themesMode.click();
  assert.equal(await page.locator('#addQueryTerm').isVisible(), true,
    'The visible + control must be available');
  await page.locator('#query').fill(fixture.theme.query);
  assert.equal(await page.locator('#query').inputValue(), fixture.theme.query, 'Theme input was unexpectedly modified');
  await page.locator('#searchButton').click();
  console.log('THEME_DEBUG '+JSON.stringify(await page.evaluate(()=>({query:document.getElementById('query').value,mode:document.getElementById('modeThemes').classList.contains('active'),status:document.getElementById('resultCount').textContent,scores:[...document.querySelectorAll('.result-card .result-status .score')].map(x=>x.textContent)}))));
  assert.equal(await page.locator('.result-card').count(), fixture.theme.recordCount,
    'Canonical theme result count drifted');
  assert.equal(await option.isVisible(), false,
    'Theme results must never expose lexical expansion');
  const themeStatuses = await page.locator('.result-card .result-status .score').allTextContents();
  assert.ok(themeStatuses.length > 0 &&
    themeStatuses.every(x => ['Central','Important','Lié','Indexé'].includes(x.trim())),
    'Canonical theme importance presentation drifted: '+JSON.stringify(themeStatuses));

  // F — The current + control builds a second exact word without a second fake field.
  await page.locator('#query').fill('vie');
  await page.locator('#addQueryTerm').click();
  assert.equal(await exactMode.evaluate(el => el.classList.contains('active')), true,
    'Using + must switch to exact-word mode');
  assert.match(await page.locator('#query').inputValue(), /^vie\s*\+\s*$/,
    'Using + must create a visible second-word slot');
  await page.locator('#query').fill('vie + amour');
  await page.locator('#searchButton').click();
  assert.ok((await page.locator('#results').innerText()).trim(),
    'The two-word search must produce an informative result');

  // Popular Questions are intentionally hidden. FAQ, Notes and Index remain reachable.
  assert.equal(await page.locator('#popularQuestionsToggle').isVisible(), false);
  assert.equal(await page.locator('#faqToggle').isVisible(), true);
  assert.equal(await page.locator('#notesLibraryToggle').isVisible(), true);
  await page.locator('#indexToggle').click();
  assert.equal(await page.locator('#indexPanel').isVisible(), true, 'Theme Index must still open');
  await page.locator('#closeIndex').click();

  assert.deepEqual(pageErrors, [], `Browser page errors: ${pageErrors.join(' | ')}`);
  console.log('Primary mode separation browser smoke PASS: theme-default, explicit occurrence switch, acclame→acclament, phrase exact-only, canonical theme, + two-word search, source filters, FAQ, index');
} finally {
  await browser.close();
}
