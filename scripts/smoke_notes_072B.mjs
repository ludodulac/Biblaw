import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const browser=await chromium.launch({headless:true});
const views=[{width:1280,height:840,mobile:false},{width:390,height:844,mobile:true},{width:320,height:760,mobile:true}];
const url=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
for(const size of views) {
 const page=await browser.newPage({viewport:{width:size.width,height:size.height},isMobile:size.mobile,hasTouch:size.mobile});
 page.setDefaultTimeout(30000);
 const privateFetch=[],errors=[];
 page.on('request',r=>{if(r.url().includes('/data/notes/')||r.url().includes('/data/note-themes-working'))privateFetch.push(r.url());});
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
 await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('1158 psaumes'),null,{timeout:90000});
 const index=await page.evaluate(async()=>{const r=await fetch('data/note-themes-public-072B.json');if(!r.ok)throw Error('Missing note themes');return r.json();});
 assert.equal(index.publicNoteCount,11);
 assert.ok(index.themes.length>0,'Public note themes generated');
 const publicRecords=await page.evaluate(async()=>{const r=await fetch('data/browser-search-catalog.json');return (await r.json()).records.filter(r=>r.recordType==='note').map(r=>r.id);});
 assert.equal(publicRecords.length,11);
 const allowed=new Set(publicRecords);
 for(const theme of index.themes){assert.ok(theme.label);assert.ok(theme.noteIds.length>0);for(const id of theme.noteIds)assert.ok(allowed.has(id),'Unpublished note leaked '+id);}
 await page.locator('#secondaryTools summary').click();
 await page.locator('[data-browse-type="note"]').click();
 assert.ok(await page.locator('#browseNoteThemes').isVisible(),'Notes theme picker open');
 assert.equal(await page.locator('#textBrowser').getAttribute('data-total-records'),'11');
 const labels=await page.locator('.browse-note-theme-item').allTextContents();
 const actual=labels.slice(1).map(x=>x.replace(/\s+\(\d+\)$/,''));
 const sorted=[...actual].sort((a,b)=>a.localeCompare(b,'fr',{sensitivity:'base'}));
 assert.deepEqual(actual,sorted,'Alphabetical French themes');
 // Multiple notes per theme, if the actual 11 include such a theme.
 const grouped=index.themes.find(t=>t.noteIds.length>=2);
 assert.ok(grouped,'Public themes should include a theme grouping >=2 notes');
 const selector=page.locator('.browse-note-theme-item[data-note-theme="'+grouped.label+'"]');
 await selector.click();
 assert.equal(await page.locator('#textBrowser').getAttribute('data-total-records'),String(grouped.noteIds.length));
 const ids=await page.locator('[data-browse-record]').evaluateAll(items=>items.map(e=>e.dataset.browseRecord));
 assert.deepEqual([...ids].sort(),[...grouped.noteIds].sort(),'Theme shows only authorized notes');
 await page.locator('#browseNoteThemeFilter').fill(grouped.label.slice(0,4));
 const filtered=await page.locator('.browse-note-theme-item:not([data-note-theme=""])').allTextContents();
 assert.ok(filtered.length>=1);
 for(const text of filtered)assert.ok(text.toLocaleLowerCase('fr').includes(grouped.label.slice(0,4).toLocaleLowerCase('fr')));
 await page.locator('#browseNoteThemeFilter').fill('');
 // Cross-list: one note may legitimately belong to several themes.
 const byNote=new Map();for(const t of index.themes)for(const id of t.noteIds){const a=byNote.get(id)||[];a.push(t.label);byNote.set(id,a);}
 const multi=[...byNote].find(([id,topics])=>topics.length>=2);
 assert.ok(multi,'A public note should appear under two independently evidenced themes');
 for(const theme of multi[1].slice(0,2)){
   await page.locator('.browse-note-theme-item[data-note-theme="'+theme+'"]').click();
   assert.equal(await page.locator('[data-browse-record="'+multi[0]+'"]').count(),1,'One note in two themes');
 }
 await page.locator('[data-browse-record="'+multi[0]+'"]').click();
 assert.ok(await page.locator('#recordDialog').isVisible());
 assert.ok((await page.locator('#dialogEyebrow').textContent()).includes('Note'));
 assert.equal(await page.locator('#dialogContent [data-note-auth]').count(),1,'Authentication provenance preserved');
 await page.locator('#browseBack').click();
 await page.locator('[data-browse-type="note"]').click();
 assert.ok(!(await page.locator('#textBrowser').isVisible()),'Note picker closes');
 await page.locator('[data-browse-type="note"]').click();
 assert.equal(await page.locator('#textBrowser').getAttribute('data-total-records'),'11','Opening resets to all notes');
 await page.locator('[data-browse-type="note"]').click();
 // Existing word search across public notes, distinct from thematic chooser.
 await page.locator('input[name=sourceType][value=psalm]').uncheck();
 await page.locator('input[name=sourceType][value=note]').check();
 await page.locator('#modeExact').click();
 await page.locator('#query').fill('Nom de la Mère');
 await page.locator('#searchButton').click();
 const resultIds=await page.locator('#results [data-open]').evaluateAll(nodes=>nodes.map(el=>el.dataset.open));
 assert.deepEqual(resultIds,['book-17-psalm-109-note-001','book-17-psalm-122-note-001'],'Text search in historic public notes');
 const target=page.locator('#results [data-open="book-17-psalm-109-note-001"]');
 await target.locator('xpath=ancestor::article').locator('[data-toggle-result]').click();
 await target.click();
 assert.equal(await page.locator('#recordDialog [data-note-auth="not-human"]').count(),1);
 await page.locator('#browseBack').click();
 await page.locator('input[name=sourceType][value=note]').uncheck();
 await page.locator('input[name=sourceType][value=psalm]').check();
 await page.locator('#query').fill('105');
 await page.locator('#searchButton').click();
 const psalm=page.locator('#results [data-open="book-17-psalm-105"]');
 await psalm.locator('xpath=ancestor::article').locator('[data-toggle-result]').click();
 await psalm.click();
 assert.equal(await page.locator('#recordDialog [data-verified-note]').count(),1);
 await page.locator('#browseBack').click();
 assert.deepEqual(privateFetch,[],'No historical notes fetched');
 assert.deepEqual(errors,[],'No JS browser runtime errors');
 console.log('BIBLAW-072B CHROMIUM PASS '+JSON.stringify({width:size.width,topics:index.themes.length,
   grouping:grouped.noteIds.length,multiThemes:multi[1].length,wordResults:resultIds.length,privateFetch:0}));
 await page.close();
}
await browser.close();
