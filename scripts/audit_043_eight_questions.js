#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
const ROOT=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(path.join(ROOT,p),'utf8'));
const engineApi=require('../js/theme-suggestion-engine.js'),directory=read('data/thematic-index/theme-directory-public.json'),runtime=read('data/thematic-index/theme-search-runtime.json');
const engine=engineApi.create(directory.themes,runtime);
const cases=[
 ['Que disent les Archanges sur la peur ?', ['peur']],
 ['Comment développer la sagesse ?', ['sagesse']],
 ["Que devient l'homme après la mort ?", ['mort']],
 ["Comment cultiver l'amour ?", ['amour']],
 ['Comment se libérer de la colère ?', ['liberation']],
 ['Comment vivre avec les Anges ?', ['anges']],
 ["Qu'est-ce que la véritable liberté ?", ['liberte']],
 ['Comment nourrir son âme ?', ['ame']]
];
const rows=cases.map(([question,expected])=>{
 const ev=engine.evaluate(question),themes=engine.suggestIndexedThemes(question);
 const indexed=themes.map(t=>({id:t.id,label:t.label,psalms:[...new Set((t.occurrences||[]).map(x=>x.recordId))],evidence:(t.occurrences||[]).slice(0,3).map(x=>({recordId:x.recordId,verseNumbers:x.verseNumbers,teaching:x.teaching}))}));
 return {question,expected,recognizedNotions:ev.recognizedNotions,themeIds:indexed.map(x=>x.id),themes:indexed,psalmsAccessible:[...new Set(indexed.flatMap(x=>x.psalms))].length,expectedPresent:expected.some(id=>indexed.some(x=>x.id===id)),problem:expected.some(id=>indexed.some(x=>x.id===id))?null:'expected-canonical-theme-not-suggested'};
});
const out=path.join(ROOT,'audit-043-eight-questions.json');fs.writeFileSync(out,JSON.stringify({source:'main editorial directory',questions:rows},null,2)+'\n');
for(const x of rows)console.log(JSON.stringify({question:x.question,themes:x.themeIds,psalms:x.psalmsAccessible,expectedPresent:x.expectedPresent}));
assert.equal(rows.length,8);
if(process.argv.includes('--require-liberation'))assert(rows[4].expectedPresent,'libérer must retrieve existing libération theme');
