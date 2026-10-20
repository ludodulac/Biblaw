import assert from 'node:assert/strict';
import {chromium} from 'playwright';

const url=process.env.BIBLAW_SMOKE_URL;
if(!url)throw Error('BIBLAW_SMOKE_URL required');
const browser=await chromium.launch({headless:true});

const type=r=>r.recordType==='master-prayer'?'prayer':r.recordType;
const numeric=r=>{
  const match=String(r.id||'').match(/^book-(\d+)-psalm-(\d+)$/);
  return [Number(match?.[1]||r.book?.number||r.bookNumber||9999),
    Number(match?.[2]||r.number||9999)];
};
try{
  const page=await browser.newPage({viewport:{width:320,height:790},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  assert.equal(response?.status(),200,'Public immutable preview should load');
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>
    document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  const docs=await page.evaluate(async()=>{
    const response=await fetch('data/browser-search-catalog.json');
    if(!response.ok)throw Error('Missing published source catalog');
    const source=(await response.json()).records||[];
    return source.map(r=>({id:r.id,recordType:r.recordType,number:r.number,
      archangel:r.archangel,book:r.book,bookNumber:r.bookNumber,
      title:r.title,verses:r.recordType==='psalm'?(r.verses||[]).length:null,
      expectedContent:(r.text||r.summary||'').slice(0,120)}));
  });
  const expected={};
  for(const k of ['psalm','prayer','note','annex'])
    expected[k]=docs.filter(r=>type(r)===k);
  expected.psalm.sort((a,b)=>{
    const ak=numeric(a),bk=numeric(b);
    return ak[0]-bk[0]||ak[1]-bk[1]||a.id.localeCompare(b.id,'fr');
  });
  assert.equal(expected.psalm.length,1158,'1 158 canonical source Psalms');
  await page.locator('#secondaryTools summary').click();
  const counts={};
  for(const category of ['psalm','prayer','note','annex']){
    const control=page.locator('[data-browse-type="'+category+'"]');
    assert.equal(await control.textContent(),'Consulter','Existing category label is unchanged');
    const start=Date.now();
    await control.click();
    const panel=page.locator('#textBrowser');
    assert.ok(await panel.isVisible(),'Panel opens: '+category);
    assert.equal(await control.getAttribute('aria-expanded'),'true');
    const expectedRows=expected[category];
    const actual=Number(await panel.getAttribute('data-total-records'));
    assert.equal(actual,expectedRows.length,'Complete '+category+' category uses only corpus data');
    counts[category]=actual;
    const initial=await page.locator('[data-browse-record]').count();
    assert.ok(initial<=48,'Initial rendering has at most one text-row batch: '+category);
    assert.ok(Date.now()-start<3500,'Initial browse panel must render promptly');
    if(expectedRows.length){
      const first=expectedRows[0];
      assert.equal(await page.locator('[data-browse-record]').first().getAttribute('data-browse-record'),
        first.id,'First entry follows canonical order');
      await page.locator('[data-browse-record]').first().click();
      assert.ok(await page.locator('#recordDialog').isVisible(),'Full document is readable');
      assert.ok(await page.locator('#browseBack').isVisible(),'Return to list is available');
      if(category==='psalm'){
        assert.equal(await page.locator('#recordDialog .verse').count(),first.verses,
          'All canonical Psalm verses are visible without pre-rendering them');
        assert.equal(await page.locator('#recordDialog .prayer-block').count(),0,
          'Browsing Psalms does not silently append a separate prayer');
      }else if(first.expectedContent){
        const shown=await page.locator('#dialogContent').textContent();
        assert.ok(shown.includes(first.expectedContent.slice(0,50)),
          'Actual complete source text starts with published record content: '+category);
      }
      await page.locator('#browseBack').click();
      assert.ok(!(await page.locator('#recordDialog').isVisible()),
        'Back closes text and preserves the list');
      assert.ok(await panel.isVisible(),'Browse list remains open');
      // All rows are reachable, but the list starts with just 48 concise titles.
      for(let loops=0;loops<Math.ceil(expectedRows.length/48)+2;loops++){
        if(!(await page.locator('#browseMore').isVisible()))break;
        await page.locator('#browseMore').click();
      }
      const allIds=await page.locator('[data-browse-record]')
        .evaluateAll(rows=>rows.map(row=>row.dataset.browseRecord));
      assert.deepEqual(allIds,expectedRows.map(r=>r.id),
        'Every existing '+category+' text is accessible exactly once and in correct order');
      assert.equal(new Set(allIds).size,expectedRows.length,'No duplicated browse rows');
    }
    await control.click();
    assert.equal(await panel.isVisible(),false,'Consulter toggles closed');
  }
  assert.ok(await page.locator('#modeThemes').isVisible(),'Search mode remains intact');
  assert.deepEqual(errors,[],'No JavaScript browser errors');
  await page.setViewportSize({width:280,height:750});
  const psalms=page.locator('[data-browse-type="psalm"]');
  await psalms.click();
  const dimensions=await page.evaluate(()=>{
    const viewport=document.documentElement,field=document.querySelector('.browse-source-row');
    const button=field.querySelector('[data-browse-type]');
    return {body:viewport.scrollWidth,viewport:viewport.clientWidth,
      buttonWidth:button.getBoundingClientRect().width};
  });
  assert.ok(dimensions.body<=dimensions.viewport+2,'280px mobile does not overflow horizontally');
  assert.ok(dimensions.buttonWidth>35,'Consulter button has readable tap area');
  console.log('BIBLAW-058 MOBILE BROWSE PASS '+JSON.stringify({url,
    counts,canonicalPsalms:counts.psalm,allIdsChecked:true,fullText:true,
    returnToList:true,initialBatchSize:48,smallestMobileWidth:280}));
}finally{await browser.close();}
