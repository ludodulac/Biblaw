#!/usr/bin/env node
'use strict';
const assert=require('assert'),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const engine=require('../js/theme-suggestion-engine.js').create(read('data/thematic-index/theme-directory-public.json').themes,read('data/thematic-index/theme-search-runtime.json'));
const cases=[
["Que disent les Archanges sur la peur ?",'peur'],
["Comment développer la sagesse ?",'sagesse'],
["Que devient l'homme après la mort ?",'mort'],
["Comment cultiver l'amour ?",'amour'],
["Comment se libérer de la colère ?",'liberation'],
["Comment vivre avec les Anges ?",'anges'],
["Qu'est-ce que la véritable liberté ?",'liberte'],
["Comment nourrir son âme ?",'ame']];
const rows=cases.map(([query,expected])=>{const evaluation=engine.evaluate(query),themes=engine.suggestIndexedThemes(query),ids=themes.map(x=>x.id),rank=ids.indexOf(expected)+1;assert.equal(new Set(ids).size,ids.length);return{query,expected,rank,top8:ids,recognizedNotions:evaluation.recognizedNotions,candidateRank:evaluation.candidateRanking.findIndex(x=>x.id===expected)+1};});
assert(rows.every(x=>x.rank>0),'A canonical expected theme is missing');
assert(rows[2].rank<=4,'Mort must be in first four suggestions');
fs.writeFileSync('audit-043b-ranking.json',JSON.stringify({rows},null,2)+'\n');
rows.forEach(x=>console.log(JSON.stringify(x)));
