import assert from 'node:assert/strict';
import { chromium } from 'playwright';
const url=process.env.BIBLAW_SMOKE_URL;
const base='https://rawcdn.githack.com/ludodulac/Biblaw/8a9a00ad357361da96aa0a3a9e7db26dc2542873/index.html';
if(!url)throw new Error('BIBLAW_SMOKE_URL required');
const browser=await chromium.launch({headless:true});
const norm=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/-/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function open(address) {
  const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  page.setDefaultTimeout(60000);
  await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
  const notice=page.getByRole('button',{name:'Open the page'});
  if(await notice.isVisible().catch(()=>false))await notice.click();
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
  return page;
}
async function contents(page,needle,{mode='exact',exhaustive=true}={}){
  const switcher=mode==='exact'?'#modeExact':'#modeThemes';
  if((await page.locator(switcher).getAttribute('aria-pressed'))!=='true')await page.locator(switcher).click();
  await page.locator('#query').fill(needle);
  const box=page.locator('#themeAutocomplete');
  const visible=await box.isVisible();
  const total=visible?Number(await box.getAttribute('data-total-suggestions')||0):0;
  const rows=new Map();
  const selector=mode==='exact'?'[data-autocomplete-word]':'[data-autocomplete-theme]';
  if(visible){
    const positions=exhaustive?Array.from({length:Math.ceil(total/11)},(_,i)=>i*11):[0,Math.floor(total/2),Math.max(0,total-1)];
    for(const pos of positions){
      await box.evaluate((e,n)=>e.scrollTop=Math.max(0,32+(n-3)*64),pos);
      await page.waitForTimeout(12);
      for(const row of await box.locator(selector).evaluateAll((nodes,attr)=>
        nodes.map(node=>({i:Number(node.dataset.suggestionIndex),display:node.textContent,
          label:node.getAttribute(attr)})),mode==='exact'?'data-autocomplete-word':'data-autocomplete-theme'))rows.set(row.i,row);
    }
    assert.ok((await box.locator(selector).count())<=18,'Virtualized DOM remains compact');
    assert.ok(await box.evaluate(e=>e.clientHeight<innerHeight/2),'Mobile dropdown bounded by half viewport');
  }
  return {total,rows:[...rows.values()].sort((a,b)=>a.i-b.i)};
}
async function ids(page,mode,query){
  const which=mode==='exact'?'#modeExact':'#modeThemes';
  if((await page.locator(which).getAttribute('aria-pressed'))!=='true')await page.locator(which).click();
  await page.locator('#query').fill(query);
  await page.locator('#query').press('Enter');
  return page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
}
try{
  const start=Date.now();
  const page=await open(url);
  const preTheme=await contents(page,'el',{mode:'themes',exhaustive:false});
  await page.locator('#modeExact').click();
  await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  const elapsed=Date.now()-start;
  assert.ok(elapsed<45000,'Mobile index ready before 45 sec; observed '+elapsed+'ms');
  const checks=['qu','qua','quat','quatre','4','dou','douze','12','quarante','40','cent','100','144','cent quarante-quatre','elem','ÉLÉMENT','monde','père'];
  const results={};
  for(const entry of checks){
    const answer=await contents(page,entry,{exhaustive:!['qu','dou','cent','monde','père'].includes(entry)});
    results[entry]=answer;
    if(answer.total===0)console.log('053F_NOT_ATTESTED',entry);
    else console.log('053F_SUGGEST',JSON.stringify({query:entry,total:answer.total,examples:answer.rows.slice(0,6).map(r=>r.display)}));
  }
  const expectedLabel='4 éléments';
  for(const input of ['qu','qua','quat','quatre','4']){
    const found=results[input].rows.filter(r=>r.display===expectedLabel);
    assert.equal(found.length,1,'Attested 4 éléments must be shown exactly once for '+input);
  }
  assert.ok(!results.elem.rows.some(r=>r.display===expectedLabel),'elem must not suggest 4 éléments');
  assert.ok(!results['4'].rows.some(r=>/^(40|400|41|44|144)\b/.test(r.label)),'4 must not match 40 or other numbers');
  assert.ok(!results['4'].rows.some(r=>r.label.startsWith('4')&&!/^4(?:\s|$)/.test(r.label)),'4 must only match complete leading integer token');
  assert.ok(results['4'].rows.every(r=>r.label==='4 éléments'||!r.label.startsWith('4')||/^4\s/.test(r.label)),'numeric token exact');
  const accent=await contents(page,'element',{exhaustive:true});
  const accented=await contents(page,'élément',{exhaustive:true});
  assert.deepEqual(accented.rows.map(r=>r.label),accent.rows.map(r=>r.label),'accents optional');
  const upper=await contents(page,'QUATRE',{exhaustive:true});
  assert.ok(upper.rows.some(r=>r.label==='4 éléments'),'uppercase numbers work');
  for(const [digit,spoken,fragment] of [['12','douze','dou'],['40','quarante','quarante'],['100','cent','cent'],['144','cent quarante-quatre','cent quarante-quatre']]){
    const direct=results[digit].rows.filter(r=>new RegExp('^'+digit+'\\s').test(r.label)).map(r=>r.label);
    const words=results[spoken].rows.map(r=>r.label);
    for(const label of direct)assert.ok(words.includes(label),'Attested '+digit+' entry must also match '+spoken+': '+label);
    if(direct.length){
      const startPart=results[fragment].rows.map(r=>r.label);
      for(const label of direct)assert.ok(startPart.includes(label),'Spoken prefix matches attested '+digit+': '+label);
    }
    console.log('053F_ATTESTED_NUMBER',JSON.stringify({digit,spoken,direct}));
  }
  const old=await open(base);
  await old.locator('#modeExact').click();
  await old.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
  const oldThemes=await contents(old,'el',{mode:'themes',exhaustive:false});
  assert.equal(preTheme.total,oldThemes.total,'THEME indexed count unchanged');
  assert.deepEqual(preTheme.rows.map(r=>r.label),oldThemes.rows.map(r=>r.label),'THEME unchanged');
  const unchanged={};
  for(const [mode,q] of [['exact','élément'],['exact','4 éléments'],['exact','monde'],['themes','sainte assemblée']]){
    const expected=await ids(old,mode,q),actual=await ids(page,mode,q);
    assert.deepEqual(actual,expected,'Unchanged psalm matches for '+mode+' '+q);
    unchanged[mode+' '+q]=actual.length;
  }
  // Select exactly the source spelling, not the spelled-out number alias.
  await page.locator('#modeExact').click();
  await page.locator('#query').fill('quatre');
  const row=page.locator('#themeAutocomplete [data-autocomplete-word="4 éléments"]').first();
  assert.ok(await row.count(),'4 éléments selectable');
  await row.evaluate(button=>button.click());
  assert.equal(await page.locator('#query').inputValue(),'4 éléments','Original corpus spelling selected verbatim');
  const afterClick=await page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open).sort());
  assert.deepEqual(afterClick,await ids(old,'exact','4 éléments'),'Selection searches original complete expression');
  assert.equal((await page.locator('#includeSimplePlurals').isChecked()),true,'Singular/plural remains active');
  console.log('BIBLAW-053F PUBLIC MOBILE PASS '+JSON.stringify({
    url,readyMs:elapsed,priority:['qu','qua','quat','quatre','4'],numericMatchedLabel:expectedLabel,
    sources:[12,40,100,144].map(n=>({n,sourceCount:results[String(n)].rows.filter(r=>r.label.startsWith(n+' ')).length})),
    noFourToForty:true,caseInsensitive:true,accentInsensitive:true,
    noDupes:true,unchanged,themeCount:preTheme.total
  }));
}finally{await browser.close();}
