#!/usr/bin/env node
// Notes: public archive is visible immediately, original 11 remain separately
// labelled, provisional transcriptions never masquerade as validated notes.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const data=JSON.parse(await readFile('_site/data/notes-extracted-public.json','utf8'));
assert.equal(data.archiveCount,280);
assert.equal(data.alreadyPublishedCount,11);
assert.equal(data.needsReviewCount,269);
assert.equal(data.bookCount,41);
assert.equal(new Set(data.notes.map(x=>x.id)).size,280);
assert.equal(data.notes.filter(x=>x.publicationStatus==='published').length,11);
assert.equal(data.notes.filter(x=>x.publicationStatus==='unverified').length,269);
assert.equal(data.notes.reduce((n,x)=>n+(x.text?.trim()?1:0),0),280);
assert.ok(data.notes.every(x=>x.sourcePdfPage>0));
const bookOne=data.notes.filter(x=>x.bookNumber===1);
const browser=await chromium.launch({headless:true});
try{
 for(const width of [390,1366]){
  const page=await browser.newPage({viewport:{width,height:844},acceptDownloads:true});
  const errors=[],heavy=[],archive=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',request=>{
   const u=request.url();
   if(/browser-search-catalog\.json|theme-directory-public\.json/.test(u))heavy.push(u);
   if(/notes-extracted-public\.json/.test(u))archive.push(u);
  });
  try{
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.locator('#notesLibraryToggle').click();
    await page.locator('#notesArchiveCount').getByText(/280 notes/).waitFor({timeout:20000});
    assert.equal(await page.locator('.notes-archive-book').count(),41);
    assert.equal(await page.locator('#notesAllToggle').getAttribute('aria-pressed'),'true');
    assert.deepEqual(heavy,[],'Notes archive should not load the 23 MB Psalm corpus');
    assert.equal(archive.length,1);
    await page.locator('.notes-archive-book').first().locator('summary').click();
    const notes=page.locator('.notes-archive-book').first().locator('[data-archived-note-id]');
    assert.equal(await notes.count(),bookOne.length);
    await notes.first().click();
    await page.locator('#recordDialog').waitFor({state:'visible'});
    const readerText=await page.locator('#dialogContent').innerText();
    assert.match(readerText,/Transcription automatique à vérifier/);
    assert.match(readerText,/PDF page/);
    assert.ok((await page.locator('.prayer-block').innerText()).length>100);
    const source=page.locator('#dialogContent .notes-source-reference');
    assert.match(await source.innerText(),/PDF page \d+/);
    assert.equal(await source.locator('a').count(),0,
      'An unverified source-page number must not create a deep link');
    const download=page.waitForEvent('download');
    await page.locator('#downloadRecord').click();
    assert.match((await download).suggestedFilename(),/^Biblaw_Note_.*\.pdf$/);
    await page.locator('#closeDialog').click();
    await page.locator('#notesArchiveSearch').fill('Esséniens');
    assert.ok(await page.locator('.notes-archive-book').count()>0);
    const current=await page.locator('#notesArchiveCount').innerText();
    assert.match(current,/trouvée/);
    await page.locator('#notesArchiveSearch').fill('');
    assert.equal(await page.locator('.notes-archive-book').count(),41);
    await page.locator('#notesArchiveBook').selectOption('17');
    assert.equal(await page.locator('.notes-archive-book').count(),1);
    assert.match(await page.locator('#notesArchiveCount').innerText(),/8 notes/);
    await page.locator('#notesArchiveBook').selectOption('');
    await page.locator('#notesPublishedToggle').click();
    await page.locator('#notesThemeList .notes-theme-item').first().waitFor({timeout:60000});
    assert.equal(await page.locator('#notesArchivePanel').isVisible(),false);
    assert.equal(await page.locator('#notesThemeList .notes-theme-item').count(),26);
    await page.locator('#notesThemeList .notes-theme-item').first().click();
    assert.equal(await page.locator('#notesThemeResults').isVisible(),true);
    await page.locator('#notesLibraryClose').click();
    assert.equal(await page.locator('#notesThemePicker').isVisible(),true);
    await page.locator('#notesLibraryClose').click();
    assert.equal(await page.locator('#notesArchivePanel').isVisible(),true);
    assert.equal(await page.locator('.notes-archive-book').count(),41);
    await page.locator('#notesLibraryClose').click();
    assert.equal(await page.locator('#notesLibrary').isVisible(),false);
    await page.locator('#notesLibraryToggle').click();
    await page.locator('#notesArchiveCount').getByText(/280 notes/).waitFor();
    assert.equal(archive.length,1,'Notes archive must remain cached during the visit');
    assert.deepEqual(errors,[]);
    console.log('NOTES_280_BROWSER_PASS '+width+'px: 280 texts/41 books, 269 clear warnings, '+
      '11 published separately, full note/PDF/source page, word and book filters, back/navigation, 0 heavy startup requests');
  }finally{await page.close();}
 }
}finally{await browser.close();}
