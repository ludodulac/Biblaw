import {chromium} from 'playwright';
const address=process.env.BIBLAW_SMOKE_URL;
if(!address)throw Error('BIBLAW_SMOKE_URL');
const browser=await chromium.launch({headless:true});
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[-‐‑‒–’']/g,' ').replace(/\s+/g,' ').trim();
try{
 const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await page.goto(address,{waitUntil:'domcontentloaded',timeout:60000});
 const notice=page.getByRole('button',{name:'Open the page'});
 if(await notice.isVisible().catch(()=>false))await notice.click();
 await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'),null,{timeout:90000});
 await page.locator('#modeExact').click();
 await page.waitForFunction(()=>document.querySelector('#query')?.dataset.wordSuggestionsReady==='true',null,{timeout:90000});
 console.log('053H_BASELINE_HYPHEN_COUNT',await page.locator('#query').getAttribute('data-hyphen-suggestion-count'));
 for(const q of ['soi','soi me','au','au dela','elem','qu','4','père','monde','est','qui','b','c','d','p','v']){
   if(q.length===1&&!/^\d$/.test(q))continue;
   await page.locator('#query').fill(q);
   const box=page.locator('#themeAutocomplete'),count=Number(await box.getAttribute('data-total-suggestions')||0);
   const items=new Map();
   for(let i=0;i<count;i+=10){
     await box.evaluate((e,index)=>e.scrollTop=Math.max(0,32+(index-3)*64),i);
     await page.waitForTimeout(6);
     for(const item of await box.locator('[data-autocomplete-word]').evaluateAll(nodes=>nodes.map(n=>({i:+n.dataset.suggestionIndex,w:n.dataset.autocompleteWord}))))items.set(item.i,item.w);
   }
   const vals=[...items.values()];
   const suspicious=vals.filter(v=>/\b(?:soi[-‐‑‒–]même\s+|est\s+au[-‐‑‒–]delà|qui\s+est|élément\s+à\s+sa|\b(?:est|dans|qui|et|de|pour|une|un|des|le|la|les|sur|avec)\s*$)/iu.test(v));
   const ends=vals.filter(v=>v.includes(' ')&&!/^\d/u.test(v)&&!v.includes('-')&&!v.includes('‑'));
   console.log('053H_BASELINE '+JSON.stringify({q,count,visited:vals.length,suspicious:suspicious.slice(0,35),wordPhrases:ends.slice(0,65),first:vals.slice(0,30)}));
 }
}finally{await browser.close();}
