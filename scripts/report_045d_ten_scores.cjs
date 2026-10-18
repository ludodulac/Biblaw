'use strict';
// BIBLAW-045F4 - stand-alone read-only measurement of historical 045D ranking.
// Historical scoring rules are from js/biblaw.js at 82c8d30c9e3e1321fe5013a4bc406461df1181f3; only regex escaping was repaired.
// Data blobs are checked against the identical Git objects present at that commit.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const ROOT = path.resolve(__dirname, '..');
const HISTORICAL_COMMIT = '82c8d30c9e3e1321fe5013a4bc406461df1181f3';
const expectedBlobs = [
  ['data/browser-search-catalog.json', '4482b5811c5536cd990cedf995db4c952a5aacad'],
  ['data/thematic-index/theme-directory-public.json', 'e4c8421b6e752005eb2bec9093b5ad0322b4e909'],
];
for (const [relative, expected] of expectedBlobs) {
  assert(fs.existsSync(path.join(ROOT, relative)), 'Missing local data file: ' + relative);
  const actual = execFileSync('git', ['hash-object', relative], {cwd: ROOT, encoding: 'utf8'}).trim();
  assert.equal(actual, expected, 'Historical input Git blob mismatch: ' + relative);
}
const readJson = relative => JSON.parse(fs.readFileSync(path.join(ROOT, relative), 'utf8'));
const catalog = readJson('data/browser-search-catalog.json');
const dir = readJson('data/thematic-index/theme-directory-public.json');
const records = Array.isArray(catalog) ? catalog : (catalog.records || catalog.items || []);
assert(Array.isArray(records) && records.length, 'Expected records array is unavailable');
assert(Array.isArray(dir.themes), 'Expected thematic directory themes array is unavailable');
const theme = dir.themes.find(x => x.id === 'mort');
assert(theme && Array.isArray(theme.occurrences) && theme.occurrences.length >= 161, 'Historical Mort theme is unavailable');
const state = {recordById: new Map(records.map(r => [r.id, r]))};
const selectedTypes = () => new Set(['psalm']);
const $ = () => ({value: ''});
const importanceRank = v => ({central: 0, important: 1, related: 2})[v] ?? 3;

// BEGIN HISTORICAL FUNCTIONS WITH REGEX REPAIR (82c8d30c9e3e1321fe5013a4bc406461df1181f3)
  function thematicQuestionTokens(value) {
    return String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
      .replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).filter(Boolean)
      .filter(word=>word.length>3&&!new Set(['comment','quels','quelles','apres','avant','dans','pour','avec','devient','devenir','homme','archanges','disent','faire','sont','cette','celui','celle']).has(word));
  }
  function thematicQuestionScore(item,question) {
    const words=thematicQuestionTokens(question);
    if(words.length<1)return 0;
    const normalize=text=>String(text||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    const evidences=item.matchedThemes||[];
    const selected=new Set(evidences.flatMap(e=>e.thematic?.verseNumbers||[]));
    const verses=(item.record.verses||[]).filter(v=>selected.has(v.number));
    const passages=[...verses.map(v=>v.text),...evidences.map(e=>e.thematic?.teaching||'')].map(normalize);
    const phrase=normalize(question).replace(/[^a-z0-9]+/g,' ').trim();
    const significant=phrase.split(/\s+/).filter(w=>w.length>3);
    const pair=significant.filter(w=>!new Set(['comment','quels','quelles','devient','devenir','homme']).has(w));
    let score=0;
    for(const passage of passages){
      const tokens=passage.match(/[a-z0-9]+/g)||[];
      const matched=words.filter(w=>tokens.some(t=>t===w||t.startsWith(w)&&w.length>=5));
      score+=matched.length*2;
      if(matched.length>=2)score+=6;
      for(let i=0;i<pair.length-1;i++){
        const a=tokens.indexOf(pair[i]),b=tokens.indexOf(pair[i+1]);
        if(a>=0&&b>a&&b-a<=5)score+=14;
      }
      if(phrase&&passage.includes(phrase))score+=20;
    }
    return score;
  }
  function thematicItems(themes,question='') {
    if (!selectedTypes().has('psalm')) return [];
    const a=$('archangelFilter').value,merged=new Map();
    for (const theme of themes) for (const o of theme.occurrences||[]) {
      if (a&&o.archangel!==a) continue;
      const record=state.recordById.get(o.recordId); if(!record||record.recordType!=='psalm') continue;
      const current=merged.get(record.id)||{record,score:0,thematic:o,matchedThemes:[]};
      const betterImportance=importanceRank(o.importance)<importanceRank(current.thematic?.importance);
      const sameImportance=importanceRank(o.importance)===importanceRank(current.thematic?.importance);
      current.score=Math.max(current.score,o.score||1);
      if(betterImportance||(sameImportance&&(o.score||1)>(current.thematic?.score||0))) current.thematic=o;
      current.matchedThemes.push({id:theme.id,label:theme.label,thematic:o}); merged.set(record.id,current);
    }
    return [...merged.values()].sort((x,y)=>{
      if(question&&question.includes('?')){
        const delta=thematicQuestionScore(y,question)-thematicQuestionScore(x,question);
        if(delta)return delta;
      }
      return importanceRank(x.thematic?.importance)-importanceRank(y.thematic?.importance)||x.record.number-y.record.number||String(x.record.id).localeCompare(String(y.record.id),'fr');
    });
  }
// END HISTORICAL FUNCTIONS WITH REGEX REPAIR

const question = "Que devient l'homme après la mort ?";
const targets = [
  [1, '03/005', 'A', 'book-03-psalm-005'],
  [2, '20/111', 'C', 'book-20-psalm-111'],
  [3, '19/112', 'B', 'book-19-psalm-112'],
  [4, '19/118', 'B', 'book-19-psalm-118'],
  [5, '19/121', 'A', 'book-19-psalm-121'],
  [6, '18/130', 'B', 'book-18-psalm-130'],
  [7, '21/140', 'C', 'book-21-psalm-140'],
  [13, '22/155', 'A', 'book-22-psalm-155'],
  [14, '22/159', 'A', 'book-22-psalm-159'],
  [15, '21/161', 'A', 'book-21-psalm-161'],
];
const baseline = thematicItems([theme]); // Same baseline construction as the 045D diagnostic.
// This instrumentation does not modify the historical scoring weights or ranking.
const separatedWords = question.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  .replace(/[^a-z0-9]+/g, ' ').trim().split(/\s+/).filter(Boolean);
const extractedTokens = thematicQuestionTokens(question);
assert.deepEqual(separatedWords, ['que', 'devient', 'l', 'homme', 'apres', 'la', 'mort'], 'Question word separation failed');
assert.deepEqual(extractedTokens, ['mort'], 'Historical filtered-token extraction failed');

// Inspect exactly the canonical passages that thematicQuestionScore() receives.
const rows = targets.map(([rank, psalm, category, id]) => {
  const item = baseline[rank - 1];
  assert(item && item.record && item.record.id === id,
    'Historical Mort baseline rank mismatch: rank ' + rank + ', expected ' + id +
    ', found ' + (item && item.record && item.record.id));
  const evidences = item.matchedThemes || [];
  const selected = new Set(evidences.flatMap(e => e.thematic?.verseNumbers || []));
  const verses = (item.record.verses || []).filter(v => selected.has(v.number));
  const verseTexts = verses.filter(v => typeof v.text === 'string' && v.text.trim().length > 0);
  const teachings = evidences.map(e => e.thematic?.teaching)
    .filter(t => typeof t === 'string' && t.trim().length > 0);
  return { rank, psalm, category, id, item, verseCount: verseTexts.length, teachingCount: teachings.length };
});
const totalVerseTexts = rows.reduce((n, r) => n + r.verseCount, 0);
const totalTeachings = rows.reduce((n, r) => n + r.teachingCount, 0);
process.stdout.write('WORDS_SEPARATED: ' + JSON.stringify(separatedWords) + '\n');
process.stdout.write('TOKENS_EXTRACTED: ' + JSON.stringify(extractedTokens) + '\n');
for (const r of rows) process.stdout.write(
  'DATA: ' + r.rank + ' | ' + r.psalm + ' | VERSE_TEXTS=' + r.verseCount +
  ' | TEACHING_TEXTS=' + r.teachingCount + '\n');
process.stdout.write('VERSES_PRESENT: ' + (totalVerseTexts > 0) +
  ' | TOTAL_VERSE_TEXTS=' + totalVerseTexts + '\n');
process.stdout.write('TEACHINGS_PRESENT: ' + (totalTeachings > 0) +
  ' | TOTAL_TEACHING_TEXTS=' + totalTeachings + '\n');
// Never publish numeric scores when either entire evidence source is absent,
// or when a target has no actual passage for the historical scorer.
assert(totalVerseTexts > 0 && totalTeachings > 0, 'Missing verse texts or teachings in historical data');
for (const r of rows) assert(r.verseCount + r.teachingCount > 0,
  'Missing all scoring evidence for ' + r.psalm);
const lines = [];
for (const r of rows) {
  const score = thematicQuestionScore(r.item, question); // Original scoring weights unchanged.
  assert(Number.isSafeInteger(score) && score >= 0, 'Invalid score for ' + r.id);
  lines.push(r.rank + ' | ' + r.psalm + ' | ' + r.category + ' | ' + score);
}
process.stdout.write([
  'FUNCTION_SOURCE_COMMIT: ' + HISTORICAL_COMMIT,
  'CATALOG_GIT_BLOB: ' + expectedBlobs[0][1],
  'INDEX_GIT_BLOB: ' + expectedBlobs[1][1],
  'QUESTION: ' + question,
  'RANG | PSAUME | CATÉGORIE | SCORE EXACT',
  ...lines,
].join('\n') + '\n');
