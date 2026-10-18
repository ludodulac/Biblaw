import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';

const pageUrl=process.env.BIBLAW_SMOKE_URL||'http://127.0.0.1:4173/index.html';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const errors=[];
page.on('pageerror',error=>errors.push(String(error)));

try{
  await page.goto(pageUrl,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'));
  const index=await page.evaluate(async()=>{
    const data=await(await fetch('data/thematic-index/theme-directory-public.json')).json();
    const themes=data.themes||[],norm=globalThis.BiblawThemeEngine.norm;
    const preferred=themes.find(t=>norm(t.label)==='ame')||themes.find(t=>norm(t.label)==='amour');
    const target=preferred||themes.find(t=>norm(t.label).length>=4&&t.occurrenceCount>0);
    if(!target)throw Error('No indexed theme to test');
    return {id:target.id,label:target.label,key:norm(target.label),ids:themes.map(t=>t.id),labels:themes.map(t=>t.label),count:themes.length};
  });
  await mkdir('screenshots-052',{recursive:true});
  await page.screenshot({path:'screenshots-052/01-accueil-mobile.png',fullPage:true});
  assert.equal(await page.locator('#resultsSection').isVisible(),false,'No initial results');
  assert.equal((await page.locator('#resultCount').textContent()).trim(),'','No initial 0 counter');
  assert.equal(await page.locator('.result-card').count(),0);
  assert.equal((await page.locator('#modeThemes').innerText()).trim(),'THÈME');
  assert.equal((await page.locator('#modeExact').innerText()).trim(),'MOTS');
  assert.ok((await page.locator('#popularThemes button').count())>0,'Indexed popular chips loaded');
  const chipIds=await page.locator('[data-popular-theme]').evaluateAll(nodes=>nodes.map(x=>x.dataset.popularTheme));
  assert.ok(chipIds.every(id=>index.ids.includes(id)),'Popular chips must be truly indexed');

  await page.locator('#query').fill(index.key.slice(0,1));
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),false,'No suggestions after 1 char');
  await page.locator('#query').fill(index.key.slice(0,2));
  const options=page.locator('#themeAutocomplete [data-autocomplete-theme]');
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),true,'Show suggestions at 2 letters');
  assert.ok((await options.count())>0&&(await options.count())<=5,'At most 5 suggestions');
  const optionIds=await options.evaluateAll(nodes=>nodes.map(x=>x.dataset.autocompleteTheme));
  assert.ok(optionIds.every(id=>index.ids.includes(id)),'Suggestions must be canonical or real aliases');

  // Accent-insensitive match on a real canonical label.
  await page.locator('#query').fill(index.key);
  const wanted=page.locator('#themeAutocomplete [data-autocomplete-theme]').filter({hasText:index.label});
  if(await wanted.count())await wanted.first().click();
  else{
    const explicit=page.locator('#themeAutocomplete [data-autocomplete-theme]').first();
    assert.ok(await explicit.count()>0,'Must have canonical suggestion for normalized label');
    await explicit.click();
  }
  assert.equal(await page.locator('#resultsSection').isVisible(),true,'Suggestion selection launches search');
  assert.ok((await page.locator('#query').inputValue()).length>0);

  await page.reload({waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.querySelector('#corpusStats')?.textContent.includes('psaumes'));
  assert.equal(await page.locator('#resultsSection').isVisible(),false,'Reload stays empty');
  await page.locator('#query').fill('105');
  await page.locator('#query').press('Enter');
  assert.match(await page.locator('#resultCount').innerText(),/numéro 105/,'Direct psalm number works');
  assert.ok((await page.locator('.result-card').count())>0,'Psalm cards rendered');
  await page.locator('.result-card [data-toggle-result]').first().click();
  await page.locator('.result-card [data-open]').first().click();
  assert.equal(await page.locator('#recordDialog').isVisible(),true,'Psalm opens');
  await page.locator('#closeDialog').click();

  await page.locator('#modeExact').click();
  await page.locator('#query').fill('acclame');
  await page.locator('#query').press('Enter');
  assert.equal(await page.locator('.result-card').count(),1,'Exact search count unchanged');
  assert.equal(await page.locator('#themeAutocomplete').isVisible(),false,'No autocomplete remains after submitting a word query');
  await page.locator('#secondaryTools summary').click();
  assert.equal(await page.locator('#exactExpansionOption').isVisible(),true,'Optional morphology in advanced options');
  assert.equal(await page.locator('#includeWordForms').isChecked(),false,'Morphology defaults off');
  await page.locator('#includeWordForms').check();
  assert.equal(await page.locator('.result-card').count(),2,'Opt-in morphology still expands');
  await page.locator('#includeWordForms').uncheck();
  assert.equal(await page.locator('.result-card').count(),1,'Exact-only can be restored');

  await page.locator('#modeThemes').click();
  await page.locator('#query').fill('sainte assemblée');
  await page.locator('#query').press('Enter');
  assert.equal(await page.locator('.result-card').count(),3,'Canonical thematic ranking/results unchanged');
  await page.screenshot({path:'screenshots-052/02-resultats-mobile.png',fullPage:true});
  const statuses=await page.locator('.result-card .score').allTextContents();
  assert.ok(statuses.every(x=>['Central','Important','Lié'].includes(x.trim())));
  await page.locator('#popularQuestionsToggle').click();
  assert.equal(await page.locator('#popularQuestionsPanel').isVisible(),true,'Questions remain accessible');
  await page.locator('#closePopularQuestions').click();
  await page.locator('#advancedSearchToggle').click();
  assert.equal(await page.locator('#query2').isVisible(),true,'Dual-theme remains accessible');
  await page.locator('#query2').fill('alliance');
  await page.locator('#query').press('Enter');
  assert.ok((await page.locator('#resultCount').innerText()).length>0,'Dual-theme route responded');

  await page.locator('#advancedSearchToggle').click();
  await page.locator('#query').fill('zzyyxxnonindexed052');
  await page.locator('#query').press('Enter');
  assert.match(await page.locator('#results').innerText(),/Aucun thème trouvé/);
  await page.locator('[data-search-in-words]').click();
  assert.equal(await page.locator('#modeExact').getAttribute('aria-pressed'),'true','Explicit word fallback');
  await page.locator('#indexToggle').click();
  assert.equal(await page.locator('#indexPanel').isVisible(),true,'Header Index works');
  await page.locator('#closeIndex').click();

  for(const width of [390,320]){
    await page.setViewportSize({width,height:844});
    const viewport=await page.evaluate(()=>({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
    assert.ok(viewport.scroll<=viewport.client+1,`No horizontal overflow at ${width}px: ${JSON.stringify(viewport)}`);
  }
  assert.deepEqual(errors,[],'No Chromium JS page errors');
  console.log('BIBLAW-052 Chromium mobile smoke PASS — blank start, 2-letter canonical/alias autocomplete, accent folding, selection, Enter, psalm, words two-letter suggestions, optional plurals, exact/optional morphology, themes, advanced tools, 390/320px');
} finally{
  await browser.close();
}
