import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const root=new URL('..',import.meta.url);
const read=path=>readFileSync(new URL(path,root),'utf8');
const library=read('js/biblaw-autocomplete.js');
const sandbox={};
sandbox.globalThis=sandbox;
vm.runInNewContext(library,sandbox,{timeout:5000});
const a=sandbox.BiblawAutocomplete;
assert.ok(a&&a.createIndex&&a.numericValue&&a.countNumericOccurrences);
const raw=[
 {id:'psalm',recordType:'psalm',archangel:'michael',title:'Abondance et abeille',
   verses:[{text:'Abaisser, abandonner, abattre, abricot, abriter, énergie. Quatre chiens et 4 fleurs.'},
           {text:'Quatre-vingts arbres et vingt-quatre oiseaux.'}]},
 {id:'prayer',recordType:'master-prayer',archangel:'raphael',title:'Prière',
   text:'Abdication, abeilles et énergie.'},
 {id:'note',recordType:'note',archangel:'michael',title:'Note publique',
   text:'Abordage, abîme et ÉNERGIE.'}
];
const index=a.createIndex();
raw.forEach(record=>index.addRecord(record));
const records=new Map(raw.map(record=>[record.id,record]));
const topics=[{id:'abondance',label:'Abondance',occurrences:[{recordId:'psalm'}]}];
const all=new Set(['psalm','prayer','note']);
const list=(q,mode='exact',types=all,arch='')=>
  index.suggestions(q,mode,types,arch,topics,records,6).map(item=>item.label);
const six=list('ab');
assert.equal(six.length,6);
assert.deepEqual([...six].map(x=>a.norm(x)),[
 'abaisser','abandonner','abattre','abdication','abeille','abeilles'
]);
assert.deepEqual([...list('ÀB')].map(a.norm),[...six].map(a.norm));
assert.deepEqual([...list('énergie')].map(a.norm),[...list('ENERGIE')].map(a.norm));
assert.ok(list('4').some(x=>a.norm(x)==='quatre'));
assert.ok(list('quatre').includes('4'));
assert.equal(list('abd','exact',new Set(['psalm'])).length,0,'Prayer cannot leak into Psalm scope');
assert.ok(list('abd','exact',new Set(['prayer'])).includes('Abdication'));
assert.ok(list('ab','exact',all,'gabriel').length===0,'Archangel restriction');
assert.ok(index.suggestions('ab','themes',new Set(['psalm']),'',topics,records,6)
  .some(entry=>entry.kind==='theme'&&entry.label==='Abondance'));
for(const [n,text] of [[4,'quatre'],[21,'vingt et un'],[71,'soixante et onze'],
 [80,'quatre-vingts'],[90,'quatre-vingt-dix'],[200,'deux cents'],
 [2026,'deux mille vingt-six']]){
 assert.equal(a.writtenNumber(n),text,String(n));
 assert.equal(a.numericValue(text),n,text);
 assert.equal(a.numericValue(String(n)),n,String(n));
}
assert.equal(a.countNumericOccurrences(['Quatre-vingts arbres et vingt-quatre oiseaux'],'4'),0);
assert.equal(a.countNumericOccurrences(['Quatre-vingts arbres et vingt-quatre oiseaux'],'80'),1);
assert.equal(a.countNumericOccurrences(['Quatre fleurs, quatre saisons et 4 portes'],'4'),3);
assert.equal(a.countNumericOccurrences(['Quatre fleurs, quatre saisons et 4 portes'],'quatre'),3);
assert.equal(a.countNumericOccurrences(['40 fleurs, 400 arbres, 4 portes'],'4'),1);
const html=read('index.html'),app=read('js/biblaw.js');
assert.ok(html.includes('id="searchSuggestions"')&&html.includes('id="searchSuggestions2"'));
assert.ok(html.includes('js/biblaw-autocomplete.js?v=082'));
assert.ok(app.includes("const available=index.suggestions(field.value,state.mode,selectedTypes()"));
assert.ok(app.includes("state.themeDirectory,state.recordById,6"));
assert.ok(app.includes("if(psalmNumber!==null && !query2 && state.mode==='themes')"));
assert.ok(app.includes("BiblawAutocomplete.countNumericOccurrences(original,query)"));
assert.ok(app.includes("correctMobileQueryDuplicate();"));
assert.ok(app.includes("publishedNotes.size!==11"));
assert.ok(app.includes("rankExactWordPairs(query,query2)"));
assert.ok(!library.includes("fetch('data/notes/"));
console.log('082 PASS: six genuine corpus prefixes, optional accents, 4/quatre, 4 vs 80, source filters, public-only record indexing, two-word search intact');
