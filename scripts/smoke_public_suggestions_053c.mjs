import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const url=process.env.BIBLAW_SMOKE_URL;
if(!url)throw Error('BIBLAW_SMOKE_URL required');
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
page.setDefaultTimeout(45000);
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
const checks=['el','él','element','élément','elements','éléments'];
try{
 const t=Date.now();
 const r=await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
 if(await page.getByRole('button',{name:'Open the page'}).isVisible().catch(()=>false))await page.getByRole('button',{name:'Open the page'}).click();
 await page.waitForFunction(()=>document.getElementById('corpusStats')?.textContent?.includes('psaumes'),{timeout:60000});
 await page.locator('#modeExact').click();
 for(const value of checks){
   await page.locator('#query').fill(value);
   const info=await page.locator('#themeAutocomplete').evaluate(e=>({
      hidden:e.hidden,rows:e.querySelectorAll('[role=option]').length,total:e.dataset.totalSuggestions||null,
      body:e.innerText.slice(0,160),
      ready:document.querySelector('#query')?.dataset.wordSuggestionsReady||null,
      input:document.querySelector('#query')?.value
   }));
   console.log('WORDS_INPUT',JSON.stringify({value,elapsedMs:Date.now()-t,...info}));
 }
 console.log('AWAIT_READY_START',Date.now()-t);
 await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',{timeout:90000});
 console.log('READY_AFTER_MS',Date.now()-t);
 for(const value of checks){
  await page.locator('#query').fill(value);
  const info=await page.locator('#themeAutocomplete').evaluate(e=>({hidden:e.hidden,total:Number(e.dataset.totalSuggestions||0),rows:e.querySelectorAll('[role=option]').length,first:e.querySelector('[role=option]')?.textContent,ready:document.querySelector('#query')?.dataset.wordSuggestionsReady||null}));
  console.log('WORDS_READY',JSON.stringify({value,...info}));
  assert.ok(!info.hidden&&info.total>0,'No results after indexed for '+value);
 }
 await page.locator('#query').fill('élément');
 const all=await page.locator('#themeAutocomplete').evaluate(e=>({count:e.dataset.totalSuggestions,first:e.innerText.slice(0,260)}));
 console.log('EXPRESSIONS',JSON.stringify(all));
 assert.equal(errors.length,0,'JS errors');
 console.log('BIBLAW-053C PUBLIC MOBILE PASS');
}finally{await browser.close();}
