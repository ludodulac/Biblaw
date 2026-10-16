import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const cases=[
["Que devient l'homme après la mort ?",'mort'],
["Comment se libérer de la colère ?",'liberation'],
["Comment développer la sagesse ?",'sagesse'],
["Comment cultiver l'amour ?",'amour']];
const browser=await chromium.launch({headless:true});
try{
const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto(process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>!document.getElementById('corpusStats')?.textContent.includes('Chargement'));
for(const [query,expected] of cases){
 await page.locator('#query').fill(query);await page.locator('#searchButton').click();
 const ids=await page.locator('#senseChoices [data-theme-id]').evaluateAll(nodes=>nodes.map(n=>n.dataset.themeId));
 assert.equal(new Set(ids).size,ids.length,'Duplicate theme choices for '+query);
 const direct=ids.length===0;
 const rank=direct?1:ids.indexOf(expected)+1;
 assert(rank>0,'Missing '+expected+' for '+query);
 if(expected==='mort')assert(rank<=4,'Mort not prominent: '+ids);
 if(!direct)await page.locator('#senseChoices [data-theme-id="'+expected+'"]').click();
 const cards=await page.locator('.result-card').count();assert(cards>0,'No psalm cards for '+expected);
 const resultIds=await page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
 assert.equal(new Set(resultIds).size,resultIds.length,'Duplicate psalms for '+expected);
 console.log(JSON.stringify({query,expected,rank,ids,cards}));
}
assert.deepEqual(errors,[]);
}finally{await browser.close()}
