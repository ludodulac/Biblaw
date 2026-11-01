import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL || 'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
const viewports=[{width:1280,height:840,mobile:false},{width:390,height:844,mobile:true},{width:320,height:760,mobile:true}];
const statuses=new Map([
  ['book-17-psalm-105-note-001','validated'],
  ['book-17-psalm-109-note-001','machine-validated'],
  ['book-17-psalm-112-note-001','machine-validated'],
  ['book-17-psalm-121-note-001','machine-validated'],
  ['book-17-psalm-122-note-001','machine-validated'],
  ['book-17-psalm-127-note-001','machine-validated'],
  ['book-17-psalm-130-note-001','machine-validated'],
  ['book-18-psalm-112-note-001','machine-extracted-needs-human-review'],
  ['book-19-psalm-104-note-001','machine-extracted-needs-human-review'],
  ['book-21-psalm-143-note-002','manually-located-needs-transcription-review'],
  ['book-26-psalm-182-note-001','machine-extracted-needs-human-review']
]);

async function openById(page,id){
  const item=page.locator('[data-browse-record="'+id+'"]');
  for(let i=0;i<35 && await item.count()===0;i++){
    const more=page.locator('#browseMore');
    if(!(await more.isVisible()))break;
    await more.click();
  }
  assert.equal(await item.count(),1,'Unique browsable record '+id);
  await item.click();
  assert.ok(await page.locator('#recordDialog').isVisible(),'Dialog visible '+id);
}
async function initialized(page){
  await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('1158 psaumes'),null,{timeout:90000});
  await page.locator('#secondaryTools summary').click();
}

try{
  for(const view of viewports){
    const page=await browser.newPage({viewport:{width:view.width,height:view.height},isMobile:view.mobile,hasTouch:view.mobile});
    page.setDefaultTimeout(60000);
    const errors=[],unpublished=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(r.url().includes('/data/notes/'))unpublished.push(r.url());});
    await initialized(page);
    const notes=await page.evaluate(async()=>{
      const response=await fetch('data/browser-search-catalog.json');
      if(!response.ok)throw Error('Missing browser catalog');
      const records=(await response.json()).records;
      const byId=new Map(records.map(r=>[r.id,r]));
      return {psalms:records.filter(r=>r.recordType==='psalm').length,
        prayers:records.filter(r=>r.recordType==='master-prayer').length,
        noteRows:records.filter(r=>r.recordType==='note').map(n=>({id:n.id,status:n.validation?.status,source:n.source?.document,
          recordId:n.appliesTo?.recordId,verse:n.appliesTo?.verse,linked:byId.get(n.appliesTo?.recordId)?.noteIds?.includes(n.id),
          prayerLink:n.appliesToPrayerId||null})),
        human:records.filter(r=>r.recordType==='note'&&r.validation?.status==='validated').length};
    });
    assert.equal(notes.psalms,1158);
    assert.equal(notes.prayers,677);
    assert.equal(notes.human,1);
    assert.equal(notes.noteRows.length,11);
    assert.deepEqual(notes.noteRows.map(n=>n.id).sort(),[...statuses.keys()].sort());
    for(const n of notes.noteRows){
      assert.equal(n.status,statuses.get(n.id),'Unchanged validation '+n.id);
      assert.equal(n.source,'Bible essénienne (classée par livres).pdf','Provenance '+n.id);
      assert.ok(n.recordId?.startsWith('book-'),'Source Psalm '+n.id);
      assert.ok(n.linked,'Reciprocal Psalm link '+n.id);
    }
    await page.locator('[data-browse-type="note"]').click();
    assert.equal(await page.locator('#textBrowser').getAttribute('data-total-records'),'11');
    assert.equal(await page.locator('[data-browse-record]').count(),11);
    for(const id of statuses.keys()){
      const authenticated=statuses.get(id)==='validated';
      const item=page.locator('[data-browse-record="'+id+'"]');
      const caption=await item.textContent();
      assert.ok(caption.includes(authenticated?'Authentifiée':'Non authentifiée'),'Browse warning '+id);
      await openById(page,id);
      const notice=page.locator('[data-note-auth]');
      assert.equal(await notice.count(),1);
      assert.equal(await notice.getAttribute('data-note-auth'),authenticated?'human':'not-human');
      const noticeText=await notice.textContent();
      assert.ok(noticeText.includes(id),'Provenance ID '+id);
      assert.ok(noticeText.includes('Bible essénienne'),'Provenance source '+id);
      assert.ok((await page.locator('#dialogEyebrow').textContent()).includes(authenticated?'Authentifiée':'Non authentifiée'));
      if(!authenticated)assert.ok(noticeText.includes('sans authentification humaine'));
      await page.locator('#browseBack').click();
    }
    await page.locator('[data-browse-type="note"]').click();
    await page.locator('[data-browse-type="psalm"]').click();
    await openById(page,'book-17-psalm-105');
    assert.equal(await page.locator('#recordDialog [data-verified-note]').count(),1,'105 authenticated attached');
    assert.equal(await page.locator('#recordDialog [data-verified-note]').first().getAttribute('data-verified-note'),'book-17-psalm-105-note-001');
    await page.locator('#browseBack').click();
    await openById(page,'book-17-psalm-109');
    assert.equal(await page.locator('#recordDialog [data-verified-note]').count(),0,'109 machine-only not attached');
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="psalm"]').click();

    await page.locator('[data-browse-type="prayer"]').click();
    await openById(page,'michael-book-21-prayer-038');
    assert.equal(await page.locator('#recordDialog [data-verified-note]').count(),0,'Legacy prayer note not human authenticated');
    await page.locator('#browseBack').click();
    await page.locator('[data-browse-type="prayer"]').click();

    // Legacy note search is a pre-existing public surface, now explicitly labelled.
    await page.locator('input[name="sourceType"][value="psalm"]').uncheck();
    await page.locator('input[name="sourceType"][value="note"]').check();
    await page.locator('#modeExact').click();
    await page.locator('#query').fill('Nom de la Mère');
    await page.locator('#searchButton').click();
    const result=page.locator('#results .result-card').filter({hasText:'Non authentifiée'}).first();
    await result.waitFor();
    await result.locator('[data-toggle-result]').click();
    assert.equal(await result.locator('[data-note-auth="not-human"]').count(),1,'Search result disclaimer');
    await result.locator('[data-open]').click();
    assert.equal(await page.locator('#recordDialog [data-note-auth="not-human"]').count(),1);
    await page.locator('#closeDialog').click();
    await page.locator('#modeThemes').click();
    await page.locator('input[name="sourceType"][value="note"]').uncheck();
    await page.locator('input[name="sourceType"][value="psalm"]').check();
    await page.locator('#query').fill('sainte assemblée');
    await page.locator('#searchButton').click();
    await page.locator('#results .result-card').first().waitFor();
    assert.ok(await page.locator('#results .result-card').count()>0,'Theme search still functional');
    assert.deepEqual(errors,[],'Browser runtime errors');
    assert.deepEqual(unpublished,[],'No historical note directory requests');
    console.log('BIBLAW-069 REAL-CATALOG PASS '+JSON.stringify({viewport:view.width,notes:11,authenticated:1,nonAuthenticated:10,prayer038:'not promoted',wordTheme:'pass'}));
    await page.close();
  }

  // Isolated browser-only synthetic fixture: prove future reciprocal prayer notes are gated.
  // It does not change any repository file or publish any synthetic note.
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await page.route('**/data/browser-search-catalog.json',async route=>{
    const response=await route.fetch();
    const payload=await response.json();
    const ps=payload.records.find(r=>r.id==='book-21-psalm-143');
    const prayer=payload.records.find(r=>r.id==='michael-book-21-prayer-038');
    if(!ps||!prayer)throw Error('Missing genuine Psalm/Prayer fixture');
    const ids=['test-069-human-prayer','test-069-machine-prayer','test-069-mismatched-prayer'];
    for(const id of ids){ps.noteIds.push(id);prayer.noteIds.push(id);}
    for(const [i,id] of ids.entries()){
      payload.records.push({id,recordType:'note',archangel:'michael',text:'Note de test navigateur uniquement '+id,
        appliesTo:{recordId:i===2?'book-17-psalm-105':ps.id,verse:1},
        appliesToPrayerId:prayer.id,validation:{status:i===1?'machine-validated':'validated'},
        source:{document:'TEST BROWSER-ONLY',printedPage:1}});
    }
    payload.recordCount=payload.records.length;
    await route.fulfill({response,body:JSON.stringify(payload),contentType:'application/json'});
  });
  await initialized(page);
  await page.locator('[data-browse-type="prayer"]').click();
  await openById(page,'michael-book-21-prayer-038');
  assert.equal(await page.locator('[data-verified-note="test-069-human-prayer"]').count(),1,'Verified reciprocal prayer note allowed');
  assert.equal(await page.locator('[data-verified-note="test-069-machine-prayer"]').count(),0,'Machine prayer note blocked');
  assert.equal(await page.locator('[data-verified-note="test-069-mismatched-prayer"]').count(),0,'Mismatched Psalm note blocked');
  console.log('BIBLAW-069 PRAYER-GATE FIXTURE PASS (browser only)');
  await page.close();
} finally {
  await browser.close();
}
