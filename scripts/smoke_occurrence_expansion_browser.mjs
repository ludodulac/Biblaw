import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const BASE_URL = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const pageErrors = [];
page.on('pageerror', error => pageErrors.push(String(error)));

try {
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => {
    const el = document.getElementById('corpusStats');
    return el && !el.textContent.includes('Chargement');
  });

  const fixture = await page.evaluate(async () => {
    const [lexical, bundle, directory, themeRuntime] = await Promise.all([
      fetch('data/lexical-expansion-runtime.json').then(r => r.json()),
      fetch('data/browser-search-catalog.json').then(r => r.json()),
      fetch('data/thematic-index/theme-directory-public.json').then(r => r.json()),
      fetch('data/thematic-index/theme-search-runtime.json').then(r => r.json()),
    ]);
    const norm = globalThis.BiblawThemeEngine.norm;
    const psalms = (bundle.records || []).filter(r => r.recordType === 'psalm');
    const fragments = new Map(psalms.map(r => [r.id, [r.title, ...(r.verses || []).map(v => v.text)].filter(Boolean).map(norm)]));
    const count = (record, query) => {
      const needle = norm(query);
      if (!needle) return 0;
      const bounded = ` ${needle} `;
      let total = 0;
      for (const fragment of fragments.get(record.id) || []) {
        const haystack = ` ${fragment} `;
        let from = 0;
        while (true) {
          const index = haystack.indexOf(bounded, from);
          if (index === -1) break;
          total += 1;
          from = index + bounded.length;
        }
      }
      return total;
    };

    let best = null;
    for (const group of lexical.g || []) {
      if (!Array.isArray(group) || group.length < 2) continue;
      for (const query of group) {
        if (!query || query.includes(' ') || query.length < 3) continue;
        const exactRows = [];
        const expandedRows = [];
        for (const record of psalms) {
          const exact = count(record, query);
          const expanded = group.reduce((sum, form) => sum + count(record, form), 0);
          if (exact) exactRows.push({ id: record.id, count: exact });
          if (expanded) expandedRows.push({ id: record.id, count: expanded });
        }
        if (!exactRows.length || expandedRows.length <= exactRows.length || expandedRows.length > 12) continue;
        const exactIds = new Set(exactRows.map(x => x.id));
        const alt = group.find(form => form !== query && psalms.some(record => !exactIds.has(record.id) && count(record, form) > 0));
        if (!alt) continue;
        const candidate = {
          query,
          alt,
          group,
          exactRecordCount: exactRows.length,
          exactOccurrenceCount: exactRows.reduce((sum, x) => sum + x.count, 0),
          expandedRecordCount: expandedRows.length,
          expandedOccurrenceCount: expandedRows.reduce((sum, x) => sum + x.count, 0),
        };
        if (!best || candidate.expandedRecordCount < best.expandedRecordCount ||
            (candidate.expandedRecordCount === best.expandedRecordCount && candidate.expandedOccurrenceCount < best.expandedOccurrenceCount)) {
          best = candidate;
        }
      }
    }
    if (!best) throw new Error('No compact safe expansion fixture found');

    let phrase = null;
    for (const record of psalms) {
      for (const verse of record.verses || []) {
        const words = norm(verse.text).split(' ').filter(Boolean);
        if (words.length < 2) continue;
        for (let i = 0; i < words.length - 1; i++) {
          const q = `${words[i]} ${words[i + 1]}`;
          const rows = psalms.map(r => ({ id: r.id, count: count(r, q) })).filter(x => x.count > 0);
          if (rows.length && rows.length <= 12) {
            phrase = {
              query: q,
              recordCount: rows.length,
              occurrenceCount: rows.reduce((sum, x) => sum + x.count, 0),
            };
            break;
          }
        }
        if (phrase) break;
      }
      if (phrase) break;
    }
    if (!phrase) throw new Error('No compact exact phrase fixture found');

    const themes = directory.themes || [];
    const theme = themes.find(t => {
      const alias = themeRuntime.aliases?.[norm(t.label)];
      const count = t.occurrenceCount || t.occurrences?.length || 0;
      return count > 0 && count <= 12 && alias?.themeIds?.length === 1 && alias.themeIds[0] === t.id;
    });
    if (!theme) throw new Error('No compact unique theme fixture found');

    return {
      lexical: best,
      phrase,
      theme: { label: theme.label, recordCount: theme.occurrenceCount || theme.occurrences.length },
    };
  });

  const secondary = page.locator('#secondaryTools');
  await secondary.evaluate(el => { el.open = true; });
  await page.locator('#modeExact').click();

  // 1. Exact word search unchanged.
  await page.locator('#query').fill(fixture.lexical.query);
  await page.locator('#searchButton').click();
  const option = page.locator('#exactExpansionOption');
  const checkbox = page.locator('#includeWordForms');
  assert.equal(await option.isVisible(), true, 'Exact-mode expansion control must be visible');
  assert.equal(await checkbox.isChecked(), false, 'Expansion must be opt-in');
  assert.equal(await checkbox.isEnabled(), true, 'Certified single-word fixture should allow expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Exact record count drifted');
  const exactBadges = await page.locator('.result-card .result-status .score').allTextContents();
  const exactSum = exactBadges.reduce((sum, text) => sum + Number.parseInt(text, 10), 0);
  assert.equal(exactSum, fixture.lexical.exactOccurrenceCount, 'Exact occurrence count drifted');

  // 2-4. Opt-in expansion adds a certified alternative and never duplicates a record.
  await checkbox.check();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.expandedRecordCount, 'Expanded record count mismatch');
  const expandedBadges = await page.locator('.result-card .result-status .score').allTextContents();
  const expandedSum = expandedBadges.reduce((sum, text) => sum + Number.parseInt(text, 10), 0);
  assert.equal(expandedSum, fixture.lexical.expandedOccurrenceCount, 'Expanded occurrence count mismatch');
  const ids = await page.locator('.result-card [data-open]').evaluateAll(nodes => nodes.map(node => node.dataset.open));
  assert.equal(new Set(ids).size, ids.length, 'Exact/expansion result duplication detected');

  const toggles = page.locator('.result-card [data-toggle-result]');
  for (let i = 0; i < await toggles.count(); i++) await toggles.nth(i).click();
  const highlighted = await page.locator('.result-card .search-hit').allTextContents();
  const normalizedHits = await page.evaluate(values => values.map(globalThis.BiblawThemeEngine.norm), highlighted);
  assert.ok(normalizedHits.includes(fixture.lexical.alt), `Certified alternative ${fixture.lexical.alt} was not visibly rendered`);

  // 5. Multi-word expressions remain exact-only.
  await page.locator('#query').fill(fixture.phrase.query);
  assert.equal(await checkbox.isEnabled(), false, 'Phrase must not enable lexical expansion');
  assert.equal(await checkbox.isChecked(), false, 'Phrase must clear lexical expansion');
  await page.locator('#searchButton').click();
  assert.equal(await page.locator('.result-card').count(), fixture.phrase.recordCount, 'Exact phrase record count drifted');
  const phraseBadges = await page.locator('.result-card .result-status .score').allTextContents();
  const phraseSum = phraseBadges.reduce((sum, text) => sum + Number.parseInt(text, 10), 0);
  assert.equal(phraseSum, fixture.phrase.occurrenceCount, 'Exact phrase occurrence count drifted');

  // 6. Theme search remains separate and unchanged by the exact-search option.
  await page.locator('#modeThemes').click();
  assert.equal(await option.isVisible(), false, 'Expansion control must be hidden in Themes mode');
  assert.equal(await checkbox.isChecked(), false, 'Leaving exact mode must clear expansion');
  await page.locator('#query').fill(fixture.theme.label);
  await page.locator('#searchButton').click();
  assert.equal(await page.locator('.result-card').count(), fixture.theme.recordCount, 'Theme result count drifted');

  // 7. Known participles cannot trigger automatic expansion.
  await page.locator('#modeExact').click();
  for (const sentinel of ['empli', 'doté']) {
    await page.locator('#query').fill(sentinel);
    assert.equal(await checkbox.isEnabled(), false, `${sentinel} must not enable expansion`);
    assert.equal(await checkbox.isChecked(), false, `${sentinel} must not retain expansion`);
    await page.locator('#searchButton').click();
  }

  // Previously established lexical/MWE boundary also stays non-expandable.
  await page.locator('#query').fill('travers');
  assert.equal(await checkbox.isEnabled(), false, 'travers must not enable expansion');

  assert.deepEqual(pageErrors, [], `Browser page errors: ${pageErrors.join(' | ')}`);
  console.log(`PR36 browser smoke PASS: exact=${fixture.lexical.query}, alternative=${fixture.lexical.alt}, phrase="${fixture.phrase.query}", theme="${fixture.theme.label}"`);
} finally {
  await browser.close();
}