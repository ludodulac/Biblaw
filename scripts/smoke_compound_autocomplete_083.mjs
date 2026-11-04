import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const read=path=>readFileSync(new URL('../'+path,import.meta.url),'utf8');
const sandbox={};sandbox.globalThis=sandbox;
vm.runInNewContext(read('js/biblaw-autocomplete.js'),sandbox,{timeout:10000});
const engine=sandbox.BiblawAutocomplete;
const index=engine.createIndex();
const records=[
  {id:'psalm-one',recordType:'psalm',archangel:'michael',
    title:'Le Saint-Esprit',verses:[
      {text:'Le Saint-Esprit, la Saint-Esprit, sain, saine, saint, sainte, saints, sainteté, saintement.'},
      {text:'Énergie, quatre saisons, l\u2019Âme, la clarté.'}
    ]},
  {id:'psalm-two',recordType:'psalm',archangel:'michael',
    title:'Le Saint\u2011Esprit',verses:[{text:'Le Saint\u2011Esprit et le Corps-Sacré.'}]},
  {id:'prayer-one',recordType:'master-prayer',archangel:'raphael',
    title:'Prière',text:'Confiance-en-Dieu.'},
  {id:'note-one',recordType:'note',archangel:'michael',
    title:'Note',text:'Le Saint\u2013Esprit, l\u2019Énergie et la Terre-Mère.'}
];
records.forEach(record=>index.addRecord(record));
const byId=new Map(records.map(record=>[record.id,record]));
const allTypes=new Set(['psalm','prayer','note']);
const psalms=new Set(['psalm']);
const list=(q,types=allTypes,archangel='')=>
  index.suggestions(q,'exact',types,archangel,[],byId,6).map(x=>x.label);
const expectSaint=(q,types=allTypes,arch='')=>{
  const labels=list(q,types,arch);
  assert.ok(labels.some(x=>engine.norm(x)==='saint esprit'),q+': compound absent from '+JSON.stringify(labels));
  assert.ok(labels.length<=6,'Maximum six suggestions');
};
for(const q of ['sain','Saint-Esprit','saint esprit','saintesprit','SAINT-ESPRIT',
                'saint\u2011esprit','saint\u2013esprit','saint e','sain..']){
  expectSaint(q);
}
expectSaint('sain',psalms,'michael');
assert.ok(list('sain',new Set(['prayer'])).every(x=>engine.norm(x)!=='saint esprit'),
  'Do not suggest public psalm compounds for prayer-only scope');
assert.ok(list('confiance en',new Set(['prayer']),'raphael').some(x=>engine.norm(x)==='confiance en dieu'));
assert.ok(list('terrem',new Set(['note']),'michael').some(x=>engine.norm(x)==='terre mere'));
assert.ok(list('ENERGIE').length&&list('energie').length,'Accentless prefixes must work');
assert.ok(list('4').some(x=>engine.norm(x)==='quatre'));
assert.ok(list('quatre').some(x=>x==='4'));
assert.equal(engine.countNumericOccurrences(['Quatre-vingts arbres et quatre oiseaux.'],'4'),1);
assert.equal(engine.countNumericOccurrences(['Quatre-vingts arbres et quatre oiseaux.'],'80'),1);
const noCompound=engine.createIndex();
noCompound.addRecord({id:'simple',recordType:'psalm',archangel:'michael',title:'Sain',
  verses:[{text:'Saint et esprit, mais pas ensemble.'}]});
assert.equal(noCompound.suggestions('saintesprit','exact',psalms,'',[],byId,6).length,0,
  'Never invent unattested compounds');
const html=read('index.html'),css=read('css/biblaw-light.css'),app=read('js/biblaw.js');
assert.ok(html.includes('for="query">✎ &nbsp;Tapez votre mot ou expression'));
assert.ok(html.includes('for="query2">Deuxième mot ou thème'));
assert.ok(css.includes('background:#fff2d4')&&css.includes('border:2px solid #b7832f'),
  'Writing field must be visually distinct from Archangel selector');
assert.ok(html.includes('biblaw-autocomplete.js?v=083')&&html.includes('biblaw-light.css?v=083'));
assert.ok(app.includes('rankExactWordPairs(query,query2)'),'Keep two-word ranking intact');
assert.ok(app.includes('publishedNotes.size!==11'),'Keep eleven public notes guard');
assert.ok(app.includes('correctMobileQueryDuplicate();'),'Keep duplicated input guard');
console.log('083 PASS — Saint-Esprit suggested with/without dash, Unicode dashes, 6-limit, accents, 4/quatre, source/archangel safety, contrasting search box');
