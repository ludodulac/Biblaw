import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const browser=await chromium.launch({headless:true});
const questions=[
 ["Que devient l'homme après la mort ?",'mort'],
 ["Comment développer la sagesse ?",'sagesse'],
 ["Comment cultiver l'amour ?",'amour'],
 ["Comment se libérer de la colère ?",'liberation']
];
try{
 const page=await browser.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>!document.getElementById('corpusStats')?.textContent.includes('Chargement'));
 const resultIds=()=>page.locator('.result-card [data-open]').evaluateAll(ns=>ns.map(n=>n.dataset.open));
 const run=async(q,id)=>{
  await page.locator('#query').fill(q);await page.locator('#searchButton').click();
  const choices=await page.locator('#senseChoices [data-theme-id]').evaluateAll(ns=>ns.map(n=>n.dataset.themeId));
  assert.equal(new Set(choices).size,choices.length);
  if(choices.length){assert(choices.includes(id),'Missing '+id+' for '+q);await page.locator('#senseChoices [data-theme-id="'+id+'"]').click();}
  const ids=await resultIds();assert(ids.length>0,'Empty results '+q);assert.equal(new Set(ids).size,ids.length,'Duplicate result cards '+q);
  return ids;
 };
 const general=await run('Mort','mort');
 const baseline=['book-03-psalm-005','book-20-psalm-111','book-19-psalm-112','book-19-psalm-118','book-19-psalm-121'];
 assert.deepEqual(general.slice(0,5),baseline,'General Mort order changed');
 for(const [q,id] of questions){
  const ids=await run(q,id);
  if(id==='mort'){
   const direct=['book-03-psalm-005','book-19-psalm-121','book-22-psalm-155','book-22-psalm-159','book-21-psalm-161'];
   const a5=ids.slice(0,5).filter(x=>direct.includes(x)).length,a10=ids.slice(0,10).filter(x=>direct.includes(x)).length;
   assert(a5>=3&&a10>=3,'Question rank not improved: '+a5+'/'+a10);
   console.log(JSON.stringify({query:q,top5:ids.slice(0,5),a5,a10}));
  }else console.log(JSON.stringify({query:q,cards:ids.length,top5:ids.slice(0,5)}));
 }
 assert.deepEqual(errors,[]);
}finally{await browser.close();}
