#!/usr/bin/env node
'use strict';
const fs=require('fs');
const path=require('path');
const engineApi=require('../js/theme-suggestion-engine.js');
const ROOT=path.resolve(__dirname,'..');
const readJson=relative=>JSON.parse(fs.readFileSync(path.join(ROOT,relative),'utf8'));
const directory=readJson('data/thematic-index/theme-directory-public.json');
const runtime=readJson('data/thematic-index/theme-search-runtime.json');
const corpus=readJson('tests/fixtures/biblaw-benchmark-q001-q120.json');
const engine=engineApi.create(directory.themes||[],runtime);
function labels(query){return engine.suggestIndexedThemes(query).map(t=>t.label);}
function selfTest(){
  const checks=[
    ['mort',['Mort','La mort ne résout pas le non-accompli','Préparer la mort en vivant','Vie après la mort comme continuité','Vie et mort']],
  ];
  for(const [query,expected] of checks){const actual=labels(query);if(JSON.stringify(actual)!==JSON.stringify(expected))throw new Error('Regression '+query+': '+JSON.stringify(actual));}
  for(const [query,required] of [
    ['Pourquoi existons-nous ?',['Sens de la vie','But de la vie']],
    ['Pourquoi avons-nous peur de mourir ?',['Peur','Mort']],
    ['les 4 éléments magiques',['Quatre éléments','Magie']],
    ['Peut-on faire le mal en croyant faire le bien ?',['Intention','Acte']],
  ]){const actual=labels(query);for(const label of required)if(!actual.includes(label))throw new Error('Regression '+query+': missing '+label+' in '+JSON.stringify(actual));}
  const ordinary=labels('acte intention bien');if(ordinary.includes('Intention'))throw new Error('Ordinary-token quota regression');
  if(engine.resolveIndexedThemes('mort')[0]?.id!=='mort')throw new Error('Canonical resolution regression: mort');
  for(const [query,required] of [
    ["Pourquoi est-ce qu’on meurt ?",['Mort']],
    ["Où va-t-on quand on meurt ?",['Mort']],
    ["Pourquoi souffrons-nous ?",['Souffrance']],
    ["Pourquoi certaines personnes souffrent-elles alors qu’elles n’ont rien fait ?",['Souffrance']],
    ["Peut-on aimer quelqu’un et pourtant devoir le quitter ?",['Amour']],
    ["Pourquoi certaines personnes veulent-elles avoir des enfants ?",['Enfant']],
  ]){const actual=labels(query);for(const label of required)if(!actual.includes(label))throw new Error('Controlled morphology '+query+': missing '+label+' in '+JSON.stringify(actual));}
  const exactVariants=query=>engine.themeQueryNotions(query).map(v=>[...v].sort());
  for(const [query,forbidden] of [
    ['pardonner','pardon'],['guerres','guerre'],['riches','richesse'],['servir','service'],['vieillir','vieillesse'],['mechant','mal'],['planete','terre'],['sommes','existence'],['cerveau','conscience'],['quittent','quitter']
  ]){const variants=exactVariants(query).flat();if(variants.includes(forbidden))throw new Error('Unauthorized morphology '+query+' -> '+forbidden);}
  const enfantVariants=exactVariants('enfants').flat();if(!enfantVariants.includes('enfant'))throw new Error('Controlled plural enfants -> enfant missing');
  if(exactVariants('maisons').flat().includes('maison'))throw new Error('Unexpected universal singularization');
  const notionKeys=query=>exactVariants(query).map(v=>v.join('|'));
  for(const [query,forbidden,required] of [
    ["d'être",'d','etre'],["c'est",'c',null],["n'ont",'n','ont'],["s'aiment",'s','aiment'],
    ["j'existe",'j','existe'],["l'âme",'l','ame'],["qu'on",'qu',null]
  ]){
    const keys=notionKeys(query),flat=exactVariants(query).flat();
    if(keys.includes(forbidden)||flat.includes(forbidden))throw new Error('French elision fragment survived: '+query+' -> '+forbidden);
    if(required&&!flat.includes(required))throw new Error('French elision lexical part missing: '+query+' -> '+required);
  }
  for(const [query,forbidden,required] of [
    ['a-t-il','t',null],['existe-t-il','t','existe'],['va-t-on','t','va'],['tombe-t-il','t','tombe']
  ]){
    const flat=exactVariants(query).flat();
    if(flat.includes(forbidden))throw new Error('Euphonic t survived: '+query);
    if(required&&!flat.includes(required))throw new Error('Inversion lexical part missing: '+query+' -> '+required);
  }
  for(const [query,required] of [
    ['sommes-nous','sommes'],['meurent-ils','mort'],['souffrons-nous','souffrance'],['soi-même','soi'],['au-dessus','dessus'],
    ['D','d'],['lettre D','d'],['X','x']
  ])if(!exactVariants(query).flat().includes(required))throw new Error('Structural counterexample mutilated: '+query+' missing '+required);
  if(engineApi.norm('peut-on')!=='peut on')throw new Error('Generic norm changed for peut-on');
  if(engineApi.norm("l'âme")!=='l ame')throw new Error('Generic norm changed for literal apostrophe path');
  for(const query of [
    'Toutes les religions parlent-elles au fond de la même réalité ?',
    'Pourquoi les humains se croient-ils au-dessus des autres animaux ?',
    "Quel monde allons-nous laisser aux enfants qui naissent aujourd'hui ?"
  ]){
    const flat=exactVariants(query).flat();
    if(flat.includes('au')||flat.includes('aux'))throw new Error('Thematic au/aux survived: '+query);
  }
  const q116=exactVariants('Pourquoi les humains se croient-ils au-dessus des autres animaux ?').flat();
  if(!q116.includes('dessus')||!q116.includes('animaux'))throw new Error('au-dessus regression: lexical remainder missing');
  if(engineApi.norm('au')!=='au'||engineApi.norm('aux')!=='aux'||engineApi.norm('au-dessus')!=='au dessus')throw new Error('Generic norm changed for literal au/aux path');
  for(const query of [
    'Pourquoi Dieu ne se montre-t-il pas ?',
    'Pourquoi les humains se tuent-ils entre eux ?',
    "Pourquoi les gens qui s'aiment se font-ils parfois du mal ?",
    'Comment se pardonner à soi-même ?',
    'Peut-on se réconcilier après une grande blessure ?',
    'Pourquoi se sent-on parfois seul même entouré ?',
    'Pourquoi les humains se croient-ils au-dessus des autres animaux ?'
  ])if(exactVariants(query).flat().includes('se'))throw new Error('Thematic se survived: '+query);
  const q083=exactVariants('Comment se pardonner à soi-même ?').flat();
  if(!q083.includes('soi'))throw new Error('Q083 regression: soi missing after se filter');
  const q116=exactVariants('Pourquoi les humains se croient-ils au-dessus des autres animaux ?').flat();
  if(!q116.includes('dessus')||!q116.includes('animaux'))throw new Error('Q116 regression after se filter');
}
function validateCorpus(){
  if(corpus.length!==120)throw new Error('Expected 120 questions, got '+corpus.length);
  const ids=corpus.map(x=>x.id),expected=Array.from({length:120},(_,i)=>'Q'+String(i+1).padStart(3,'0'));
  if(JSON.stringify(ids)!==JSON.stringify(expected))throw new Error('Corpus IDs are not exactly Q001-Q120');
  if(new Set(ids).size!==120)throw new Error('Duplicate corpus IDs');
  if(new Set(corpus.map(x=>x.family)).size!==14)throw new Error('Expected 14 families');
  const witnesses={Q001:'Pourquoi sommes-nous là ?',Q059:"Est-ce l'intention ou ce que l'on fait réellement qui compte le plus ?",Q120:"Quel monde allons-nous laisser aux enfants qui naissent aujourd'hui ?"};
  for(const [id,q] of Object.entries(witnesses))if(corpus.find(x=>x.id===id)?.q!==q)throw new Error('Corpus witness mismatch: '+id);
}
function benchmark(){
  validateCorpus();selfTest();
  const results=corpus.map(item=>{
    const a=engine.evaluate(item.q),b=engine.evaluate(item.q);
    const sig=x=>JSON.stringify({normalizedQuery:x.normalizedQuery,recognizedNotions:x.recognizedNotions,composedNotions:x.composedNotions,candidateCountBeforeTop8:x.candidateCountBeforeTop8,top8:x.top8.map(t=>t.id)});
    if(sig(a)!==sig(b))throw new Error('Non-deterministic result: '+item.id);
    return{id:item.id,family:item.family,question:item.q,normalizedQuery:a.normalizedQuery,recognizedNotions:a.recognizedNotions,composedNotions:a.composedNotions,candidateCountBeforeTop8:a.candidateCountBeforeTop8,top8:a.top8.map(t=>({id:t.id,label:t.label})),candidateRanking:a.candidateRanking};
  });
  if(results.length!==120)throw new Error('Expected 120 benchmark results');
  fs.mkdirSync(path.join(ROOT,'benchmark-output'),{recursive:true});
  fs.writeFileSync(path.join(ROOT,'benchmark-output/benchmark-q001-q120.json'),JSON.stringify({engine:'js/theme-suggestion-engine.js',directory:'data/thematic-index/theme-directory-public.json',runtime:'data/thematic-index/theme-search-runtime.json',count:results.length,results},null,2)+'\n');
  const csv=['id,family,question,normalizedQuery,recognizedNotions,composedNotions,candidateCountBeforeTop8,top8'];
  const quote=v=>'"'+String(v??'').replace(/"/g,'""')+'"';
  for(const r of results)csv.push([r.id,r.family,r.question,r.normalizedQuery,JSON.stringify(r.recognizedNotions),JSON.stringify(r.composedNotions),r.candidateCountBeforeTop8,r.top8.map(x=>x.label).join(' | ')].map(quote).join(','));
  fs.writeFileSync(path.join(ROOT,'benchmark-output/benchmark-q001-q120.csv'),csv.join('\n')+'\n');
  for(const id of ['Q001','Q059','Q120']){const r=results.find(x=>x.id===id);console.log(id,JSON.stringify({question:r.question,normalizedQuery:r.normalizedQuery,recognizedNotions:r.recognizedNotions,composedNotions:r.composedNotions,candidateCountBeforeTop8:r.candidateCountBeforeTop8,top8:r.top8}));}
  console.log('BENCHMARK_OK count=120 families=14 deterministic=yes');
}
selfTest();
if(!process.argv.includes('--self-test-only'))benchmark();
