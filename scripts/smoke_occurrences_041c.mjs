import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { readFileSync,writeFileSync } from 'node:fs';
const runtime=JSON.parse(readFileSync('_site/data/lexical-expansion-runtime.json','utf8'));
const terms=['pain','pains','maison','maisons','aimer','chanter','garder','parler'];
const byForm=new Map(runtime.g.flatMap(group=>group.map(form=>[form,group])));
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
const report={runtimeGroups:runtime.g.length,runtimeAnchors:byForm.size,tests:{}};
try{
 await page.goto('http://127.0.0.1:4173/index.html',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>!document.getElementById('corpusStats').textContent.includes('Chargement'));
 await page.locator('#modeExact').click();
 await page.locator('#secondaryTools summary').click(); // 052: morphology is in the folded advanced menu
 const ids=()=>page.locator('.result-card [data-open]').evaluateAll(nodes=>nodes.map(n=>n.dataset.open));
 for(const term of terms){
  await page.locator('#query').fill(term);await page.locator('#searchButton').click();
  const exact=await ids();const checkbox=page.locator('#includeWordForms');
  const forms=(byForm.get(term)||[]).filter(x=>x!==term);
  const optionVisible=await page.locator('#exactExpansionOption').isVisible();
  assert.equal(await checkbox.isChecked(),false,term+' default exact');
  assert.equal(optionVisible,forms.length>0,term+' option visibility');
  assert.equal(new Set(exact).size,exact.length,term+' exact duplicate');
  let expanded=exact,restored=exact;
  if(forms.length){
   await checkbox.check();expanded=await ids();
   assert.equal(new Set(expanded).size,expanded.length,term+' expanded duplicate');
   assert.ok(exact.every(x=>expanded.includes(x)),term+' lost exact result');
   assert.ok(expanded.length>=exact.length,term+' count decreased');
   await checkbox.uncheck();restored=await ids();
   assert.deepEqual(restored,exact,term+' failed exact restore');
  }
  report.tests[term]={exactPsalmCards:exact.length,additionalForms:forms,expandedPsalmCards:expanded.length,uniqueExpandedIds:new Set(expanded).size,restoredExactPsalmCards:restored.length,optionVisible,passed:true};
  console.log('041C_BROWSER_CASE='+JSON.stringify({term,...report.tests[term]}));
 }
 assert.deepEqual(errors,[],'page errors');
 writeFileSync(process.env.BIBLAW_REPORT||'/tmp/041c-browser.json',JSON.stringify(report,null,2)+'\n');
 console.log('041C_BROWSER_ALL_PASS');
}finally{await browser.close();}
