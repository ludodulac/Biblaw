import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const url=process.env.BIBLAW_SMOKE_URL;
if(!url)throw Error('Missing BIBLAW_SMOKE_URL');
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const errors=[],requests=[];
page.on('console',message=>{if(message.type()==='error')errors.push('console '+message.text());});
page.on('pageerror',error=>errors.push('page '+error.message));
page.on('requestfailed',request=>requests.push(request.url()+' '+request.failure()?.errorText));
page.on('response',response=>{
  if(/(js\/biblaw|theme-suggestion-engine|browser-search-catalog|lexical-expansion-runtime|theme-directory-public|theme-search-runtime|linguistic-grammar-browser)/.test(response.url())){
    console.log('LIVE_RESOURCE',response.status(),response.headers()['content-type'],response.url().split('/').slice(-2).join('/'));
  }
});
try{
  const response=await page.goto(url,{waitUntil:'networkidle',timeout:45000});
  console.log('LIVE_DOCUMENT',response?.status(),page.url());
  await page.waitForTimeout(1500);
  const status=await page.evaluate(async()=>{
    const stat=document.querySelector('#corpusStats')?.textContent;
    const result=document.querySelector('#results')?.textContent?.slice(0,150);
    const entry=await Promise.all(['data/browser-search-catalog.json','data/thematic-index/theme-directory-public.json','js/biblaw.js'].map(async path=>{
      try{
        const res=await fetch(path);
        return {path,status:res.status,contentType:res.headers.get('content-type'),length:res.headers.get('content-length'),prefix:(await res.text()).slice(0,80)};
      }catch(e){return {path,error:String(e)};}
    }));
    return {stat,result,entry};
  });
  console.log('LIVE_STATUS',JSON.stringify(status));
  console.log('LIVE_ROOT',JSON.stringify(await page.evaluate(()=>({title:document.title,html:document.documentElement.outerHTML.slice(0,1100),body:document.body?.innerText?.slice(0,700),scripts:[...document.scripts].map(s=>s.src)}))));
  if(!status.stat){
    const alt=url.replace('rawcdn.githack.com','raw.githack.com');
    const altResponse=await page.goto(alt,{waitUntil:'networkidle',timeout:30000});
    console.log('ALTERNATIVE_DOCUMENT',altResponse?.status(),page.url());
    console.log('ALTERNATIVE_ROOT',JSON.stringify(await page.evaluate(()=>({title:document.title,stat:document.querySelector('#corpusStats')?.textContent,body:document.body?.innerText?.slice(0,600),html:document.documentElement.outerHTML.slice(0,700)}))));
  }
  console.log('LIVE_ERRORS',JSON.stringify(errors.slice(0,15)),JSON.stringify(requests.slice(0,15)));
  assert.match(status.stat||'',/psaumes/,'Corpus loaded from live preview');
  await page.locator('#indexToggle').click();
  assert.equal(await page.locator('#indexPanel').isVisible(),true,'Index clickable on actual link');
  await page.locator('#closeIndex').click();
  await page.locator('#modeExact').click();
  await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',{timeout:30000});
  await page.locator('#query').fill('ma');
  assert.ok(Number(await page.locator('#themeAutocomplete').getAttribute('data-total-suggestions'))>100,'Live suggestions loaded');
  await page.locator('#searchButton').click();
  assert.equal(await page.locator('#resultsSection').isVisible(),true,'Live search clickable');
  console.log('BIBLAW-054 LIVE PREVIEW MOBILE PASS');
}finally{await browser.close();}
