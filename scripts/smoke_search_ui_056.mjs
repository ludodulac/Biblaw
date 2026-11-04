import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const url=process.env.BIBLAW_SMOKE_URL;
if(!url)throw Error('BIBLAW_SMOKE_URL required');

const browser=await chromium.launch({headless:true});
const norm=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'')
  .toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae')
  .replace(/[’']/g,' ').replace(/[^a-z0-9\s-]/g,' ')
  .replace(/-/g,' ').replace(/\s+/g,' ').trim();
const count=(source,needle)=>{
  const text=norm(source),key=norm(needle);
  if(!key)return 0;
  if(!key.includes(' '))return text.split(' ').filter(x=>x===key).length;
  return (' '+text+' ').split(' '+key+' ').length-1;
};

try{
  const page=await browser.newPage({viewport:{width:320,height:750},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  assert.equal(response?.status(),200,'Public mobile preview reachable');
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  await page.locator('#modeExact').click();
  assert.ok(await page.locator('#exactAddTerm').isVisible(),'Plus button visible in MOTS');
  await page.locator('#includeSimplePlurals').uncheck(); // deterministic literal comparison

  const catalog=await page.evaluate(async()=>{
    const res=await fetch('data/browser-search-catalog.json');
    if(!res.ok)throw Error('Cannot inspect public corpus');
    return (await res.json()).records.filter(r=>r.recordType==='psalm')
      .map(r=>({id:r.id,number:r.number,fragments:[r.title,...(r.verses||[]).map(v=>v.text)]}));
  });
  const matches=term=>catalog.map(r=>({...r,hits:r.fragments.reduce((n,f)=>n+count(f,term),0)}))
    .filter(r=>r.hits>0);
  const find=async query=>{
    await page.locator('#query').fill(query);
    await page.locator('#query').press('Enter');
    const ids=await page.locator('.result-card [data-open]')
      .evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
    const statuses=await page.locator('.result-card .result-status .score')
      .allTextContents();
    return {ids,statuses,banner:await page.locator('#resultCount').textContent()};
  };

  // Count a COMPLETE attested multiword group, not individual words.
  const phrase='ronde des archanges',expectedPhrase=matches(phrase);
  const single=await find(phrase);
  const total=expectedPhrase.reduce((sum,x)=>sum+x.hits,0);
  assert.deepEqual(new Set(single.ids),new Set(expectedPhrase.map(x=>x.id)));
  assert.ok(single.banner.includes(total+' occurrence'),'Phrase total is exact: '+single.banner);
  assert.ok(single.banner.includes(expectedPhrase.length+' psaume'),'Phrase psalm count: '+single.banner);

  await page.locator('#query').fill('vérité');
  await page.locator('#exactAddTerm').click();
  assert.equal(await page.locator('#query').inputValue(),'vérité + ',
    'Touching + inserts the optional second clause');
  const pair=await find('vérité + sagesse');
  const second=new Map(matches('sagesse').map(r=>[r.id,r.hits]));
  const expectedPair=matches('vérité').filter(r=>second.has(r.id))
    .map(r=>({...r,primaryCount:r.hits,secondaryCount:second.get(r.id)}))
    .sort((a,b)=>b.primaryCount-a.primaryCount||
      b.secondaryCount-a.secondaryCount||Number(a.number)-Number(b.number)||
      a.id.localeCompare(b.id,'fr'));
  assert.ok(expectedPair.length>0,'The source has shared occurrences of vérité and sagesse');
  assert.deepEqual(pair.ids,expectedPair.map(r=>r.id),
    'Dual search MUST rank first phrase first, then second phrase');
  for(let i=0;i<Math.min(8,expectedPair.length);i++){
    const expected=expectedPair[i];
    assert.equal(pair.statuses[i],expected.primaryCount+' + '+expected.secondaryCount+
      ' occurrences','Pair counts reflect independently counted phrases');
  }
  assert.ok(pair.banner.includes('tri : 1er puis 2e'),'Sorting priority is visible');
  assert.ok(pair.banner.includes('vérité')&&pair.banner.includes('sagesse'));
  const reversed=await find('sagesse + vérité');
  assert.deepEqual(new Set(reversed.ids),new Set(pair.ids),
    'Changing query order changes sorting but not the AND candidate set');
  const twoPhrases=await find('ronde des archanges + sagesse');
  const secondPhrases=new Map(matches('sagesse').map(r=>[r.id,r.hits]));
  const phraseIDs=matches('ronde des archanges').filter(r=>secondPhrases.has(r.id))
    .map(r=>r.id);
  assert.deepEqual(new Set(twoPhrases.ids),new Set(phraseIDs),
    'Two literal phrases each must occur at least once in the same psalm');
  assert.deepEqual((await find('vérité')).ids.sort(),matches('vérité').map(r=>r.id).sort(),
    'Existing single-word matches not changed');
  assert.equal(await page.locator('#exactAddTerm').isVisible(),true);
  await page.locator('#modeThemes').click();
  assert.equal(await page.locator('#exactAddTerm').isVisible(),false,
    'Plus is only available in MOTS, not THÈME');
  assert.deepEqual(errors,[],'No browser errors');
  console.log('BIBLAW-056 COMBINED MOBILE PASS '+JSON.stringify({
    url,viewport:320,phrase,phraseOccurrences:total,phrasePsalms:expectedPhrase.length,
    bothPsalms:expectedPair.length,topPairs:expectedPair.slice(0,5)
      .map(x=>[x.primaryCount,x.secondaryCount]),
    phraseAndWordPsalms:twoPhrases.ids.length,themeUnchanged:true
  }));
}finally{await browser.close();}
