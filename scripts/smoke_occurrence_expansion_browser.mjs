import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const BASE_URL = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const fixture = {
  lexical: { query: 'acclame', alt: 'acclament', exactRecordCount: 1, expandedRecordCount: 2 },
  phrase: { query: 'temps vis', recordCount: 1 },
  theme: { query: 'sainte assemblée', recordCount: 3 },
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const pageErrors = [];
page.on('pageerror', error => pageErrors.push(String(error)));

const resultIds = () => page.locator('.result-card [data-open]').evaluateAll(nodes => nodes.map(node => node.dataset.open));
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

  const secondary = page.locator('#secondaryTools');
  const option = page.locator('#exactExpansionOption');
  const checkbox = page.locator('#includeWordForms');

  // Human Android path: stay in the main search, with secondary tools closed.
  assert.equal(await secondary.evaluate(el => el.open), false, 'Secondary tools must start closed');
  await page.locator('#query').fill(fixture.lexical.query);
  await page.locator('#searchButton').click();

  // Main thematic search falls back to literal text and exposes safe expansion directly.
  assert.equal(await secondary.evaluate(el => el.open), false, 'Human fallback must not require opening secondary tools');
  assert.equal(await option.isVisible(), true, 'Safe word expansion must be visible next to results');
  assert.equal(await checkbox.isChecked(), false, 'Expansion must remain opt-in');
  assert.equal(await checkbox.isEnabled(), true, 'acclame must have a safe expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Fallback exact result count drifted');
  const exactIds = await resultIds();

  // Check: certified alternative appears and no exact/expansion duplicate is created.
  await checkbox.check();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.expandedRecordCount, 'Expanded fallback result count mismatch');
  const expandedIds = await resultIds();
  assert.equal(new Set(expandedIds).size, expandedIds.length, 'Exact/expansion duplicate detected');
  assert.ok(expandedIds.some(id => !exactIds.includes(id)), 'Expansion did not add a distinct certified result');
  await openAllResults();
  const highlighted = await page.locator('.result-card .search-hit').allTextContents();
  const normalizedHits = await page.evaluate(values => values.map(globalThis.BiblawThemeEngine.norm), highlighted);
  assert.ok(normalizedHits.includes(fixture.lexical.alt), 'Certified alternative acclament was not visibly rendered');

  // Uncheck: return to exact fallback only.
  await checkbox.uncheck();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Unchecking must restore exact fallback');
  assert.deepEqual(await resultIds(), exactIds, 'Unchecking must restore the original exact result set');
  assert.equal(await option.isVisible(), true, 'Safe option should remain available after returning to exact fallback');

  // Multi-word expressions stay exact-only and never expose expansion.
  await page.locator('#query').fill(fixture.phrase.query);
  await page.locator('#searchButton').click();
  assert.equal(await option.isVisible(), false, 'Phrase must not expose word expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.phrase.recordCount, 'Exact phrase result count drifted');

  // Canonical Themes path stays unchanged and does not expose expansion.
  await page.locator('#query').fill(fixture.theme.query);
  await page.locator('#searchButton').click();
  assert.equal(await option.isVisible(), false, 'Canonical theme search must not expose lexical expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.theme.recordCount, 'Theme result count drifted');

  // Known participles remain blocked in the same main-search fallback path.
  for (const sentinel of ['empli', 'doté']) {
    await page.locator('#query').fill(sentinel);
    await page.locator('#searchButton').click();
    assert.equal(await option.isVisible(), false, `${sentinel} must not expose expansion`);
  }

  assert.equal(await secondary.evaluate(el => el.open), false, 'Smoke test must reproduce the closed-tools human path');
  assert.deepEqual(pageErrors, [], `Browser page errors: ${pageErrors.join(' | ')}`);
  console.log('PR36 UX browser smoke PASS: human-fallback=acclame, alternative=acclament, phrase="temps vis", theme="sainte assemblée"');
} finally {
  await browser.close();
}
