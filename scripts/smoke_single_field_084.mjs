import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const html=read('index.html'),js=read('js/biblaw.js'),css=read('css/biblaw-light.css');
assert.match(html,/<label class="search-query-label" for="query">/);
assert.match(html,/<div class="search-input-line">/);
assert.match(html,/<button type="button" id="addQueryTerm"/);
assert.match(html,/Pour ajouter un autre mot, appuyez sur <strong>\+<\/strong>/);
assert.equal((html.match(/class="search-input-line"/g)||[]).length,1,'One visible query entry row');
assert.ok(html.includes('<div hidden aria-hidden="true"><input id="query2"'),
  'Second legacy query may exist only as hidden internal state');
assert.ok(!html.includes('class="search-field compact-search theme2-slot'),
  'Second visible query field must be removed');
assert.match(html,/id="advancedSearchToggle"[^>]*hidden/);
assert.ok(!html.includes('class="popular-questions-toggle" type="button" aria-expanded="false" aria-controls="query2"'),
  'No crossing control shown on screen');
assert.ok(css.includes('.primary-search #advancedSearchToggle,') &&
  css.includes('.primary-search .theme-plus,.primary-search .theme2-slot,'),
  'Hidden cross controls cannot be surfaced by older CSS');
assert.ok(css.includes('background:#eef0f2')&&css.includes('border:0!important') &&
  css.includes('background:#fff2d4'), 'Dropdown must look different from text field');
const i=js.indexOf("  $('addQueryTerm').onclick=()=>{");
const j=js.indexOf("  $('searchButton').onclick=",i);
assert.ok(i>=0&&j>i,'Plus button must have a direct action');
const expression=js.slice(i,j)+"; return $('addQueryTerm').onclick;";
function testPlus(value) {
  let focused=false,cursor=-1;const field={value,
    focus(){focused=true;},setSelectionRange(i){cursor=i;}};
  const elements={query:field,addQueryTerm:{}},state={mode:'themes'};
  let closed=false;
  const plusHandler=Function('$','state','activateExactMode','closeAllSuggestions',
    expression)(id=>elements[id],state,()=>{state.mode='exact';},()=>{closed=true;});
  plusHandler();
  return {value:field.value,focused,cursor,closed,mode:state.mode};
}
assert.deepEqual(testPlus('vie'),{
  value:'vie + ',focused:true,cursor:6,closed:true,mode:'exact'
});
assert.equal(testPlus('vie + amour').value,'vie + amour','Never add a third term');
assert.equal(testPlus('').value,'','Empty search does not insert a leading plus');
assert.ok(js.includes("const plusPair=splitExactWordPair(rawQuery);"), 'Plus parser still used');
assert.ok(js.includes("const query=plusPair?plusPair[0]:rawQuery,query2=plusPair?plusPair[1]:'';"),
  'Search must not split visible query into a second field');
assert.ok(js.includes("if(plusPair){") &&
  js.includes("return render(rankExactWordPairs(query,query2)"),
  'Two-word priority sort must remain intact');
assert.ok(!js.includes("$('query').value=plusPair[0]"),
  'Full typed expression must not be overwritten');
assert.ok(js.includes("publishedNotes.size!==11"), 'Note privacy invariant');
assert.ok(html.includes('biblaw.js?v=084')&&html.includes('biblaw-light.css?v=084'));
console.log('084 PASS: single search field, inline plus, hidden legacy state, normal dropdown, word ranking and notes safety');
