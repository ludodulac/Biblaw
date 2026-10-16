import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import {readFileSync,writeFileSync} from 'node:fs';
const root='_site/data/thematic-index/';
const directory=JSON.parse(readFileSync(root+'theme-directory-public.json','utf8'));
const runtime=JSON.parse(readFileSync(root+'theme-search-runtime.json','utf8'));
const theme=directory.themes.find(x=>x.id==='pain-de-vie');
assert.ok(theme,'Pain de vie absent from public browser directory');
assert.equal(theme.occurrences.length,26);
const expected=new Set(theme.occurrences.map(x=>x.recordId));
assert.equal(expected.size,26);
const report={};
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
const ids=()=>page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
try{
 await page.goto('http://127.0.0.1:4173/index.html',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>!document.getElementById('corpusStats').textContent.includes('Chargement'));
 await page.locator('#modeThemes').click();
 for(const q of ['pain','pains','pain de vie','pain spirituel','nourriture','amour','lumière']){
  await page.locator('#query').fill(q);await page.locator('#searchButton').click();
  const found=await ids();assert.equal(found.length,new Set(found).size,'duplicate cards: '+q);
  const alias=q.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const target=runtime.aliases[alias];assert.ok(target?.themeIds?.length,'missing alias '+q);
  if(['pain','pains','pain de vie','pain spirituel'].includes(q)){
   assert.deepEqual(target.themeIds,['pain-de-vie']);
   assert.deepEqual(new Set(found),expected,'wrong psalm ids: '+q);
   assert.equal(await page.locator('#themeEntryName').textContent().then(x=>x.includes('Pain de vie')),true);
  }else{
   assert.ok(found.length>0,'regression empty '+q);
  }
  report[q]={psalmCards:found.length,ids:found,themeIds:target.themeIds};
  console.log('042B3_CHROMIUM '+JSON.stringify({query:q,psalmCards:found.length,themeIds:target.themeIds}));
 }
 await page.locator('#modeExact').click();
 await page.locator('#query').fill('pain');await page.locator('#searchButton').click();
 const exact=await ids();assert.ok(exact.length>=40,'exact occurrence regression');
 report.exactPain={psalmCards:exact.length};
 assert.deepEqual(errors,[]);
 writeFileSync('/tmp/042b3-browser.json',JSON.stringify(report,null,2)+'\n');
 console.log('042B3_CHROMIUM_ALL_PASS');
}finally{await browser.close();}
