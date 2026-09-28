import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const BASE_URL = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const fixture = {
  lexical: {
    query: 'acclame',
    alt: 'acclament',
    exactRecordCount: 1,
    exactOccurrenceCount: 1,
    expandedRecordCount: 2,
    expandedOccurrenceCount: 2,
  },
  phrase: { query: 'temps vis', recordCount: 1, occurrenceCount: 1 },
  theme: { query: '22 arcanas', recordCount: 1 },
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const pageErrors = [];
page.on('pageerror', error => pageErrors.push(String(error)));

const occurrenceSum = async () => {
  const badges = await page.locator('.result-card .result-status .score').allTextContents();
  return badges.reduce((sum, text) => sum + Number.parseInt(text, 10), 0);
};

try {
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => {
    const el = document.getElementById('corpusStats');
    return el && !el.textContent.includes('Chargement');
  });

  const secondary = page.locator('#secondaryTools');
  await secondary.evaluate(el => { el.open = true; });
  await page.locator('#modeExact').click();

  // 1. Exact word search remains unchanged and expansion is opt-in.
  await page.locator('#query').fill(fixture.lexical.query);
  await page.locator('#searchButton').click();
  const option = page.locator('#exactExpansionOption');
  const checkbox = page.locator('#includeWordForms');
  assert.equal(await option.isVisible(), true, 'Exact-mode expansion control must be visible');
  assert.equal(await checkbox.isChecked(), false, 'Expansion must be opt-in');
  assert.equal(await checkbox.isEnabled(), true, 'Certified word must allow expansion');
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.exactRecordCount, 'Exact record count drifted');
  assert.equal(await occurrenceSum(), fixture.lexical.exactOccurrenceCount, 'Exact occurrence count drifted');

  // 2-4. The checkbox adds a certified alternative without duplicating a record.
  await checkbox.check();
  assert.equal(await page.locator('.result-card').count(), fixture.lexical.expandedRecordCount, 'Expanded record count mismatch');
  assert.equal(await occurrenceSum(), fixture.lexical.expandedOccurrenceCount, 'Expanded occurrence count mismatch');
  const ids = await page.locator('.result-card [data-open]').evaluateAll(nodes => nodes.map(node => node.dataset.open));
  assert.equal(new Set(ids).size, ids.length, 'Exact/expansion result duplication detected');
  const toggles = page.locator('.result-card [data-toggle-result]');
  for (let i = 0; i < await toggles.count(); i++) await toggles.nth(i).click();
  const highlighted = await page.locator('.result-card .search-hit').allTextContents();
  const normalizedHits = await page.evaluate(values => values.map(globalThis.BiblawThemeEngine.norm), highlighted);
  assert.ok(normalizedHits.includes(fixture.lexical.alt), 'Certified alternative was not visibly rendered');

  // 5. Multi-word expressions stay exact-only.
  await page.locator('#query').fill(fixture.phrase.query);
  assert.equal(await checkbox.isEnabled(), false, 'Phrase must not enable expansion');
  assert.equal(await checkbox.isChecked(), false, 'Phrase must clear expansion');
  await page.locator('#searchButton').click();
  assert.equal(await page.locator('.result-card').count(), fixture.phrase.recordCount, 'Exact phrase record count drifted');
  assert.equal(await occurrenceSum(), fixture.phrase.occurrenceCount, 'Exact phrase occurrence count drifted');

  // 6. Themes remain a separate search path.
  await page.locator('#modeThemes').click();
  assert.equal(await option.isVisible(), false, 'Expansion control must be hidden in Themes mode');
  assert.equal(await checkbox.isChecked(), false, 'Leaving exact mode must clear expansion');
  await page.locator('#query').fill(fixture.theme.query);
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

  // Established MWE boundary remains non-expandable too.
  await page.locator('#query').fill('travers');
  assert.equal(await checkbox.isEnabled(), false, 'travers must not enable expansion');

  assert.deepEqual(pageErrors, [], `Browser page errors: ${pageErrors.join(' | ')}`);
  console.log('PR36 browser smoke PASS: exact=acclame, alternative=acclament, phrase="temps vis", theme="22 arcanas"');
} finally {
  await browser.close();
}