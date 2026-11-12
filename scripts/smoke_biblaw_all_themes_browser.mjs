#!/usr/bin/env node
// 106 - all canonical Bible themes, A-Z to ranked Psalms to the existing reader.
// No deployment: tested against a local build of the public site.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {chromium} from 'playwright';

const base=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const dir=JSON.parse(await readFile('_site/data/thematic-index/theme-directory-public.json','utf8'));
const catalog=JSON.parse(await readFile('_site/data/browser-search-catalog.json','utf8'));
const themes=dir.themes;
const records=new Map(catalog.records.map(r=>[r.id,r]));
assert.equal(themes.length,1267,'Unexpected indexed-theme count');
const collator=new Intl.Collator('fr',{sensitivity:'base',numeric:true});
const rank=importance=>({central:0,important:1,related:2}[importance]??3);
const expectedFor=theme=>{
  const byId=new Map();
  for(const occ of theme.occurrences||[]){
    const rec=records.get(occ.recordId);
    if(rec?.recordType!=='psalm')continue;
    const prev=byId.get(rec.id);
    if(!prev||rank(occ.importance)<rank(prev.occ.importance)||
       (rank(occ.importance)===rank(prev.occ.importance)&&(occ.score||1)>(prev.occ.score||1)))
      byId.set(rec.id,{rec,occ});
  }
  return [...byId.values()].sort((a,b)=>rank(a.occ.importance)-rank(b.occ.importance)||
    (b.occ.score||0)-(a.occ.score||0)||
    Number(a.rec.number)-Number(b.rec.number)||
    a.rec.id.localeCompare(b.rec.id,'fr')).map(x=>x.rec.id);
};
const browser=await chromium.launch({headless:true});
try{
  for(const width of [390,1366]){
    const page=await browser.newPage({viewport:{width,height:844},acceptDownloads:true});
    const errors=[],heavy=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{
      if(/\/data\/(?:browser-search-catalog|thematic-index\/theme-directory-public)\.json/.test(r.url()))
        heavy.push(new URL(r.url()).pathname);
    });
    try{
      await page.goto(base,{waitUntil:'networkidle'});
      assert.deepEqual(heavy,[],'The large theme/corpus files should stay deferred at startup');
      assert.equal(await page.getByRole('button',{name:'Index des thèmes',exact:true}).count(),1,
        'There must be exactly one index button on the homepage');
      assert.equal(await page.locator('#indexPanel,#indexToggle,#bibleThemesShortcut').count(),0,
        'The redundant theme index and footer shortcut must be gone');
      assert.equal(await page.locator('#bibleThemesToggle').innerText(),'Index des thèmes');
      await page.locator('#bibleThemesToggle').click();
      assert.equal(await page.locator('#bibleThemesTitle').innerText(),'Index des thèmes');
      await page.locator('#bibleThemesDirectory [data-bible-theme-id]').first().waitFor({timeout:60000});
      assert.equal(await page.locator('#bibleThemesDirectory [data-bible-theme-id]').count(),themes.length);
      assert.equal(await page.locator('#bibleThemesLibrary').isVisible(),true);
      assert.equal(await page.locator('#bibleThemesIndex').isVisible(),true);
      const actualNames=await page.locator('#bibleThemesDirectory [data-bible-theme-id] strong').allTextContents();
      const expectedNames=themes.map(t=>t.label).sort(collator.compare);
      assert.deepEqual(actualNames,expectedNames,'The full directory must be in French A-Z order');
      assert.equal(new Set(actualNames).size,actualNames.length,'Unexpected duplicate theme label');
      assert.ok(await page.locator('#bibleThemesLetters button').count()>15,
        'A-Z jump navigation was not shown');
      const firstLetter=await page.locator('.bible-themes-letter').first().textContent();
      assert.match(firstLetter,/^[A-Z]|0–9$/);
      assert.equal(heavy.filter(p=>p.endsWith('browser-search-catalog.json')).length,1);
      assert.equal(heavy.filter(p=>p.endsWith('theme-directory-public.json')).length,1);

      await page.locator('#bibleThemesFilter').fill('amour');
      assert.ok(await page.locator('#bibleThemesDirectory [data-bible-theme-id]').count()>0);
      // Deliberately switch main-search filters. The public theme directory
      // must still return ALL recorded Psalms, never an accidental subset.
      await page.evaluate(()=>{
        document.querySelector('input[name=sourceType][value=psalm]').checked=false;
        document.getElementById('archangelFilter').value='michael';
      });
      const candidate=page.locator('#bibleThemesDirectory [data-bible-theme-id]').first();
      const selectedId=await candidate.getAttribute('data-bible-theme-id');
      const theme=themes.find(t=>t.id===selectedId);
      assert.ok(theme);
      const expectedPsalms=expectedFor(theme);
      assert.ok(expectedPsalms.length>1,'The test theme must have several Psalms');
      await candidate.click();
      assert.equal(await page.locator('#bibleThemeSelected').innerText(),theme.label);
      assert.equal(await page.locator('#bibleThemesIndex').isVisible(),false);
      const actualPsalms=await page.locator('#bibleThemePsalmList [data-bible-theme-psalm]')
        .evaluateAll(nodes=>nodes.map(n=>n.dataset.bibleThemePsalm));
      assert.deepEqual(actualPsalms,expectedPsalms,
        'Theme results must contain every indexed Psalm in relevance order, without duplicates or main-search filters');
      const ranks=await page.locator('#bibleThemePsalmList .bible-theme-group-heading').allTextContents();
      const order=ranks.map(s=>s.split(' — ')[0]);
      const sorted=[...order].sort((a,b)=>rank({Central:'central',Important:'important',Lié:'related'}[a])-
        rank({Central:'central',Important:'important',Lié:'related'}[b]));
      assert.deepEqual(order,sorted,'Theme-group relevance order is incorrect');

      await page.locator('#bibleThemePsalmList [data-bible-theme-psalm]').first().click();
      await page.locator('#recordDialog').waitFor({state:'visible'});
      assert.ok(await page.locator('#dialogContent .verse').count()>0);
      const pdfEvent=page.waitForEvent('download');
      await page.locator('#downloadRecord').click();
      const file=await pdfEvent;
      assert.match(file.suggestedFilename(),/\.pdf$/);
      await page.locator('#closeDialog').click();
      assert.equal(await page.locator('#bibleThemeResults').isVisible(),true,
        'Closing a Psalm must return to the ranked list');
      await page.locator('#bibleThemesBack').click();
      assert.equal(await page.locator('#bibleThemesIndex').isVisible(),true);
      assert.equal(await page.locator('#bibleThemesFilter').inputValue(),'amour');
      await page.locator('#bibleThemesFilter').fill('terme-inexistant-xyz');
      assert.equal(await page.locator('#bibleThemesDirectory [data-bible-theme-id]').count(),0);
      await page.locator('#bibleThemesFilter').fill('');
      assert.equal(await page.locator('#bibleThemesDirectory [data-bible-theme-id]').count(),1267);
      await page.locator('#bibleThemesLetters button').last().click();
      await page.locator('#bibleThemesBack').click();
      assert.equal(await page.locator('#bibleThemesLibrary').isVisible(),false);
      assert.equal(await page.locator('#bibleThemesToggle').getAttribute('aria-expanded'),'false');
      await page.locator('#bibleThemesToggle').click();
      assert.equal(await page.locator('#bibleThemesDirectory [data-bible-theme-id]').count(),1267);
      assert.equal(heavy.filter(p=>p.endsWith('browser-search-catalog.json')).length,1,
        'Reopening must not download the same huge corpus twice');
      await page.locator('#bibleThemesBack').click();
      assert.deepEqual(errors,[],'Browser exceptions: '+errors.join(' / '));
      console.log('BIBLAW 106 '+width+'px PASS: '+themes.length+
        ' themes sorted A-Z; all Psalms ranked by canonical importance and score; no filter leakage; '+
        'reader, PDF, return, letter jump, keyword filter and cache.');
    }finally{await page.close();}
  }
}finally{await browser.close();}
