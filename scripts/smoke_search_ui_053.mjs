import assert from 'node:assert/strict';
import { chromium } from 'playwright';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
page.setDefaultTimeout(45000);
const errors=[]; page.on('pageerror',error=>errors.push(String(error)));
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/-/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
async function scrollCheck(mode){
  const m=await page.locator('#themeAutocomplete').evaluate(el=>({height:el.clientHeight,total:el.scrollHeight,viewport:innerHeight}));
  assert.ok(m.total>m.height,mode+' must scroll');
  assert.ok(m.height<m.viewport/2,mode+' stays compact on mobile');
  await page.locator('#themeAutocomplete').evaluate(el=>el.scrollTop=el.scrollHeight);
  assert.ok((await page.locator('#themeAutocomplete').evaluate(el=>el.scrollTop))>0,mode+' scroll moves');
}
try{
  await page.goto('http://127.0.0.1:4173/index.html',{waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'));
  assert.equal(await page.locator('#resultsSection').isVisible(),false,'No initial results');
  const themePair=await page.evaluate(async()=>{
    const data=await(await fetch('data/thematic-index/theme-directory-public.json')).json();
    const norm=globalThis.BiblawThemeEngine.norm,counts=new Map();
    for(const theme of data.themes||[]){
      const key=norm(theme.label),pairs=new Set();
      for(let i=0;i<key.length-1;i++)if(/^[a-z]{2}$/.test(key.slice(i,i+2)))pairs.add(key.slice(i,i+2));
      for(const p of pairs)counts.set(p,(counts.get(p)||0)+1);
    }
    return [...counts].filter(p=>p[1]>=12&&p[1]<=90).sort((a,b)=>a[1]-b[1])[0]?.[0]||
      [...counts].sort((a,b)=>b[1]-a[1])[0]?.[0];
  });
  assert.ok(themePair,'Indexed themes have pairs');
  await page.locator('#query').fill(themePair[0]);
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),false);
  await page.locator('#query').fill(themePair);
  const themeCount=Number(await page.locator('#themeAutocomplete').getAttribute('data-total-suggestions'));
  assert.ok(themeCount>5,'All matching theme suggestions (>5)');
  assert.ok((await page.locator('[data-autocomplete-theme]').count())<=18,'Theme DOM uses virtual rows');
  await scrollCheck('themes');
  await page.locator('#modeExact').click();
  await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true');
  assert.equal(await page.locator('#modeExact').getAttribute('aria-pressed'),'true','Mode button works while all suggestions open');
  await page.locator('#query').fill('m');
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),false);
  await page.locator('#query').fill('ma');
  const words=page.locator('[data-autocomplete-word]');
  const wordCount=Number(await page.locator('#themeAutocomplete').getAttribute('data-total-suggestions'));
  assert.ok(wordCount>100,'All matching words (>100)');
  assert.ok((await words.count())<=18,'At most 18 DOM nodes represent full suggestions list');
  await scrollCheck('words');
  assert.ok((await words.count())<=18,'Scrolling does not build thousands of buttons');
  // A suggestion menu containing thousands of entries must never prevent basic taps.
  await page.locator('#indexToggle').click();
  assert.equal(await page.locator('#indexPanel').isVisible(),true,'Index remains clickable with massive list');
  await page.locator('#closeIndex').click();
  await page.locator('#query').fill('mé');
  const accents=await words.allTextContents();
  await page.locator('#query').fill('me');
  assert.deepEqual(await words.allTextContents(),accents,'Accent insensitive suggestions');

  const samples=await page.evaluate(async()=>{
    const bundle=await(await fetch('data/browser-search-catalog.json')).json();
    const sources=(bundle.records||[]).flatMap(r=>r.recordType==='psalm'?[r.title,...(r.verses||[]).map(v=>v.text)]:[r.title,r.text,r.summary]).filter(Boolean);
    const patterns={
      hyphen:/[\p{L}]{3,}-[\p{L}]{3,}/gu,
      numeric:/(?:\b\d+|\bquatre|\btrois|\bdeux|\bsept)\s+[\p{L}]{3,}/giu,
      apostrophe:/[\p{L}]{3,}\s+de\s+l[’'][\p{L}]{3,}/giu,
      spaced:/[\p{L}]{3,}\s+(?:de|du|des|au|aux|en|pour|sans)\s+[\p{L}]{3,}/giu
    };
    const found={hyphen:null,numeric:null,apostrophe:null,spaced:null};
    for(const source of sources)for(const [kind,pattern] of Object.entries(patterns)){
      if(found[kind])continue;
      pattern.lastIndex=0;const m=pattern.exec(String(source));
      if(m)found[kind]=m[0];
    }
    for(const [kind,example] of [['hyphen','Père-Mère'],['numeric','4 éléments'],['numeric','quatre éléments'],['apostrophe',"monde de l'homme"]]){
      if(sources.some(s=>String(s).toLocaleLowerCase('fr').includes(example.toLocaleLowerCase('fr'))))found[kind]=example;
    }
    return found;
  });
  let tested=0;
  for(const [kind,candidate] of Object.entries(samples)){
    if(!candidate){console.log('053 source absent '+kind);continue;}
    const words=norm(candidate).split(' ').filter(x=>x.length>=3);
    const query=words[words.length-1];
    await page.locator('#query').fill(query);
    const total=Number(await page.locator('#themeAutocomplete').getAttribute('data-total-suggestions'));
    let selected=null;
    // Scroll through the COMPLETE result set (virtualized DOM) to reach an attested phrase
    // even when its source word has thousands of other occurrences.
    for(let start=0;start<total;start+=13){
      await page.locator('#themeAutocomplete').evaluate((box,index)=>{box.scrollTop=32+64*index;},start);
      await page.waitForTimeout(8);
      const at=await page.locator('[data-autocomplete-word]').evaluateAll((elements,label)=>elements.findIndex(el=>el.dataset.autocompleteWord.toLocaleLowerCase('fr')===label.toLocaleLowerCase('fr')),candidate);
      if(at>=0){selected=page.locator('[data-autocomplete-word]').nth(at);break;}
    }
    assert.ok(selected,kind+' is attested and reachable by scrolling from '+query+': '+candidate);
    assert.equal((await selected.textContent()).toLocaleLowerCase('fr'),candidate.toLocaleLowerCase('fr'),'Punctuation and spaces preserved');
    await selected.click();
    assert.equal(norm(await page.locator('#query').inputValue()),norm(candidate),'Complete phrase inserted');
    const expected=await page.evaluate(async phrase=>{
      const bundle=await(await fetch('data/browser-search-catalog.json')).json();
      const norm=globalThis.BiblawThemeEngine.norm,needle=' '+norm(phrase)+' ';
      return (bundle.records||[]).filter(r=>r.recordType==='psalm'&&[r.title,...(r.verses||[]).map(v=>v.text)].some(s=>(' '+norm(s)+' ').includes(needle))).map(r=>r.id).sort();
    },candidate);
    const actual=await page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(node=>node.dataset.open).sort());
    assert.deepEqual(actual,expected,'Search entire consecutive expression: '+candidate);
    assert.ok(actual.length>0,'Attested phrase has results');
    tested++;
  }
  assert.ok(tested>=2,'Multiple attested compound forms exercised');
  await page.locator('#query').fill('maison');
  await page.locator('#query').press('Enter');
  assert.ok((await page.locator('.result-card').count())>0,'Exact words still work');
  assert.equal(await page.locator('#includeSimplePlurals').isChecked(),true,'Plural choice preserved');
  await page.locator('#includeSimplePlurals').uncheck();
  assert.ok((await page.locator('.result-card').count())>0,'Strict option works');
  await page.locator('#modeThemes').click();
  await page.locator('#query').fill('sainte assemblée');
  await page.locator('#query').press('Enter');
  assert.equal(await page.locator('.result-card').count(),3,'Thematic rankings preserved');
  for(const width of [390,320]){
    await page.setViewportSize({width,height:844});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth+1),'No overflow '+width);
  }
  assert.deepEqual(errors,[],'No browser errors');
  console.log('BIBLAW-053 MOBILE PASS '+JSON.stringify({themeCount,wordCount,tested,samples}));
}finally{await browser.close();}
