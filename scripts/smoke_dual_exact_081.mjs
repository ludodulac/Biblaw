import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const js=readFileSync(new URL('../js/biblaw.js',import.meta.url),'utf8');
const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const start=js.indexOf('function splitExactWordPair(value)');
const end=js.indexOf('function mergeExpansionMatches(',start);
assert.ok(start>=0&&end>start,'Two-word helper must be present');
const factory=vm.runInNewContext('(function(matches){'+js.slice(start,end)+'return {splitExactWordPair,rankExactWordPairs};})');

const fixture=[
 {id:'psalm-1',number:1,vie:26,amour:32},
 {id:'psalm-2',number:2,vie:26,amour:25},
 {id:'psalm-3',number:3,vie:25,amour:32},
 {id:'psalm-4',number:4,vie:20,amour:14},
 {id:'psalm-5',number:5,vie:10,amour:16},
 {id:'psalm-missing-amour',number:6,vie:999,amour:0},
 {id:'psalm-missing-vie',number:7,vie:0,amour:999}
];
function matches(word){
 return fixture.filter(row=>(row[word]||0)>0).map(row=>({
   record:{id:row.id,number:row.number},
   occurrenceCount:row[word]
 }));
}
const {splitExactWordPair,rankExactWordPairs}=factory(matches);
for(const [text,expected] of [
 ['vie + amour',['vie','amour']],
 ['vie+amour',['vie','amour']],
 ['  vie  +  amour  ',['vie','amour']],
 ['vie',null],
 ['vie + ',null],
 ['+ amour',null],
 ['vie + amour + joie',null]
])assert.equal(JSON.stringify(splitExactWordPair(text)),JSON.stringify(expected),text);
const ranking=rankExactWordPairs('vie','amour');
assert.deepEqual(Array.from(ranking,r=>r.record.id),['psalm-1','psalm-2','psalm-3','psalm-4','psalm-5']);
assert.deepEqual(Array.from(ranking,r=>[r.occurrenceCount,r.secondaryOccurrenceCount]),[[26,32],[26,25],[25,32],[20,14],[10,16]]);
const reversed=rankExactWordPairs('amour','vie');
assert.equal(reversed[0].record.id,'psalm-1');
assert.equal(reversed[1].record.id,'psalm-3'); // tied 32 amor occurrences; 'vie' breaks tie.
assert.equal(ranking.some(r=>r.record.id==='psalm-missing-amour'||r.record.id==='psalm-missing-vie'),false);
const tieMatches=word=>[...[
 {id:'A',number:10,vie:26,amour:25},
 {id:'B',number:5,vie:26,amour:25},
 {id:'C',number:5,vie:26,amour:25}
]].filter(r=>r[word]>0).map(r=>({record:{id:r.id,number:r.number},occurrenceCount:r[word]}));
assert.deepEqual(Array.from(factory(tieMatches).rankExactWordPairs('vie','amour'),r=>r.record.id),['B','C','A']);

assert.ok(js.includes("const exactItems=matches(query);"),'Single-word search must stay available');
assert.ok(js.includes("function intersectionItems(themeA, themeB)"),'Two-theme intersection must remain');
assert.ok(js.includes("if(plusPair){")&&js.includes("setAdvancedSearch(true);"),'Entering plus syntax must enable two-word mode');
assert.ok(js.includes("return render(rankExactWordPairs(query,query2)"),'Two-word search must call count-based ranker');
assert.ok(js.includes("companion?.dualExactQueries?"),'Both word counts must appear in results');
assert.ok(js.includes("secondaryOccurrenceCount"),'Second count is shown');
assert.ok(js.includes("const secondCounts=new Map(matches(secondWord)"),'Use same source/archangel-filtered exact matcher for both');
assert.ok(js.includes("correctMobileQueryDuplicate();"),'080 keyboard correction must remain');
assert.ok(js.includes("publishedNotes.size!==11"),'Public note gate must remain');
assert.match(html,/id="dualExactHelp"/);
assert.match(html,/id="advancedSearchToggle"/);
assert.ok(html.includes('js/biblaw.js?v=081'),'Avoid old JavaScript in mobile cache');
console.log('081 PASS — vie/amour 26-32, 26-25, 25-32, 20-14, 10-16; first count dominates, second breaks ties, both required');
