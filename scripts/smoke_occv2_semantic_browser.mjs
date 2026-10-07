import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const BASE_URL = process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const semanticRuntime = await fetch(new URL('data/linguistic-sense-browser-runtime.json', BASE_URL)).then(r => {
  if (!r.ok) throw new Error(`semantic browser runtime ${r.status}`);
  return r.json();
});
const browserCatalog = await fetch(new URL('data/browser-search-catalog.json', BASE_URL)).then(r => {
  if (!r.ok) throw new Error(`browser catalog ${r.status}`);
  return r.json();
});
const lexicalRuntime = await fetch(new URL('data/lexical-expansion-runtime.json', BASE_URL)).then(r => {
  if (!r.ok) throw new Error(`lexical runtime ${r.status}`);
  return r.json();
});

const target = semanticRuntime.targets?.[0];
assert.ok(target, 'Semantic browser smoke requires at least one runtime target');
const positiveSenses = (target.senses || []).filter(sense => sense.occurrenceCount > 0);
assert.ok(positiveSenses.length, 'First semantic target must expose at least one validated sense');
const semanticForms = new Set((semanticRuntime.targets || []).map(item => item.normalizedForm));
const recordsById = new Map((browserCatalog.records || []).map(record => [record.id, record]));
const browserType = record => record?.recordType === 'master-prayer' ? 'prayer' : record?.recordType;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const pageErrors = [];
page.on('pageerror', error => pageErrors.push(String(error)));

const resultIds = () => page.locator('.result-card [data-open]').evaluateAll(nodes => nodes.map(node => node.dataset.open));
async function resultOccurrenceTotal() {
  const labels = await page.locator('.result-card .result-status .score').allTextContents();
  return labels.reduce((sum, text) => sum + Number((text.match(/\d+/) || ['0'])[0]), 0);
}
async function currentFilters() {
  return {
    types: new Set(await page.locator('[name=sourceType]:checked').evaluateAll(nodes => nodes.map(node => node.value))),
    archangel: await page.locator('#archangelFilter').inputValue(),
  };
}
function expectedRows(sense, filters) {
  return (sense.records || []).filter(([recordId]) => {
    const record = recordsById.get(recordId);
    return record && filters.types.has(browserType(record)) && (!filters.archangel || record.archangel === filters.archangel);
  });
}
async function assertSenseResults(sense) {
  const filters = await currentFilters();
  const expected = expectedRows(sense, filters);
  const expectedIds = expected.map(row => row[0]).sort();
  const actualIds = (await resultIds()).sort();
  assert.deepEqual(actualIds, expectedIds, `Record set drift for ${sense.senseId}`);
  assert.equal(await resultOccurrenceTotal(), expected.reduce((sum, row) => sum + row[1], 0), `Occurrence total drift for ${sense.senseId}`);
  assert.equal(await page.locator('#includeWordForms').isChecked(), false, 'Expansion must be unchecked while a sense is selected');
  assert.equal(await page.locator('#includeWordForms').isEnabled(), false, 'Expansion must be disabled while a sense is selected');
  assert.equal(await page.locator('#exactExpansionOption').isVisible(), false, 'Expansion option must be hidden while a sense is selected');

  const psalmRow = expected.find(([recordId,,verseNumbers]) => browserType(recordsById.get(recordId)) === 'psalm' && verseNumbers.length);
  if (psalmRow) {
    const card = page.locator(`.result-card:has([data-open="${psalmRow[0]}"])`);
    const toggle = card.locator('[data-toggle-result]');
    if ((await toggle.getAttribute('aria-expanded')) !== 'true') await toggle.click();
    const shown = (await card.locator('.exact-context .context-verse strong').allTextContents()).map(Number);
    assert.deepEqual(shown, psalmRow[2].slice(0, 4).map(Number), `Semantic verse projection drift for ${psalmRow[0]}`);
  }
}

try {
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => {
    const el = document.getElementById('corpusStats');
    return el && !el.textContent.includes('Chargement');
  });

  await page.locator('#modeExact').click();
  await page.locator('#query').fill(target.normalizedForm);
  await page.locator('#searchButton').click();
  assert.ok(await page.locator('.result-card').count() > 0, 'Default exact results must exist for the first semantic target');
  const initialIds = (await resultIds()).sort();
  assert.equal(await page.locator('#ambiguityPanel').isVisible(), true, 'Semantic precision panel must be visible');
  assert.equal(await page.locator('[data-semantic-all]').count(), 1, 'All occurrences choice must exist');
  assert.equal(await page.locator('[data-semantic-sense-id]').count(), positiveSenses.length, 'Sense choice count must come from runtime');
  assert.equal(await page.locator('[data-semantic-sense-id="UNCERTAIN"]').count(), 0, 'UNCERTAIN must never be exposed as a sense');

  for (const sense of positiveSenses) {
    const button = page.locator(`[data-semantic-sense-id="${sense.senseId}"]`);
    assert.equal(await button.count(), 1, `Missing semantic choice for ${sense.senseId}`);
    await button.click();
    await assertSenseResults(sense);
  }

  const firstSense = positiveSenses[0];
  await page.locator(`[data-semantic-sense-id="${firstSense.senseId}"]`).click();
  await page.locator('#secondaryTools').evaluate(el => { el.open = true; });
  const sourceTypes = [...new Set((firstSense.records || []).map(([recordId]) => browserType(recordsById.get(recordId))).filter(Boolean))];
  const alternateType = sourceTypes.find(type => type !== 'psalm' && ['prayer','note','annex'].includes(type));
  if (alternateType) {
    const boxes = page.locator('[name=sourceType]');
    for (let i = 0; i < await boxes.count(); i++) {
      const box = boxes.nth(i);
      const value = await box.getAttribute('value');
      if (value === alternateType) {
        if (!(await box.isChecked())) await box.check();
      } else if (await box.isChecked()) {
        await box.uncheck();
      }
    }
    await assertSenseResults(firstSense);
    for (let i = 0; i < await boxes.count(); i++) {
      const box = boxes.nth(i);
      const value = await box.getAttribute('value');
      if (value === 'psalm') {
        if (!(await box.isChecked())) await box.check();
      } else if (await box.isChecked()) {
        await box.uncheck();
      }
    }
  }

  const filters = await currentFilters();
  const archangel = (firstSense.records || [])
    .map(([recordId]) => recordsById.get(recordId))
    .find(record => record && filters.types.has(browserType(record)) && record.archangel)?.archangel;
  if (archangel) {
    await page.locator('#archangelFilter').selectOption(archangel);
    await assertSenseResults(firstSense);
    await page.locator('#archangelFilter').selectOption('');
  }

  await page.locator('[data-semantic-all]').click();
  assert.deepEqual((await resultIds()).sort(), initialIds, 'All occurrences must restore the initial exact result set');

  const nonTarget = (lexicalRuntime.g || []).flat().find(form => !semanticForms.has(form));
  assert.ok(nonTarget, 'Could not derive a deterministic non-semantic form');
  await page.locator('#query').fill(nonTarget);
  await page.locator('#searchButton').click();
  assert.equal(await page.locator('#ambiguityPanel').isVisible(), false, 'Changing query must clear the semantic panel/selection');

  await page.locator('#modeThemes').click();
  assert.equal(await page.locator('#modeThemes').evaluate(el => el.classList.contains('active')), true, 'Theme mode must remain functional');
  assert.equal(await page.locator('#ambiguityPanel').isVisible(), false, 'Theme mode must clear semantic selection');

  assert.deepEqual(pageErrors, [], `Browser page errors: ${pageErrors.join(' | ')}`);
  console.log(`OCCV2 semantic browser smoke PASS: ${positiveSenses.length} sense(s), filters, verses, restore, query/mode reset`);
} finally {
  await browser.close();
}
