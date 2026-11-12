#!/usr/bin/env node
// Explicit phrase associations may only suggest canonical topics;
// they never create, remove or reorder a canonical theme/Psalm relation.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const engine=require('../js/theme-suggestion-engine.js');
const runtime=JSON.parse(await readFile('data/thematic-index/theme-search-runtime.json','utf8'));
const nav=JSON.parse(await readFile('data/thematic-index/theme-semantic-navigation-public.json','utf8'));
const canonical=[...new Set(Object.values(runtime.aliases).flatMap(x=>x.themeIds))].sort();
const themes=canonical.map(id=>({id,label:id.replaceAll('-',' ')}));
const instance=engine.create(themes,runtime,nav);
assert.equal(canonical.length,1267);
for(const [query,item] of Object.entries(nav.queries)){
  const actual=instance.relatedThemesForQuery(query).map(t=>t.id);
  assert.deepEqual(actual,item.themeIds,'Wrong related topics for '+query);
}
assert.deepEqual(instance.relatedThemesForQuery('Contes de fées').map(t=>t.id),
  nav.queries['contes de fees'].themeIds);
assert.deepEqual(instance.relatedThemesForQuery('légendes').map(t=>t.id),
  nav.queries.legendes.themeIds);
assert.deepEqual(instance.relatedThemesForQuery('conte').map(t=>t.id),
  ['blanche-neige','fees','haricot-magique','baguette-magique','licorne']);
assert.deepEqual(instance.resolveIndexedThemes('conte'),[]);
assert.deepEqual(instance.relatedThemesForQuery('assemblée'),[]);
assert.deepEqual(instance.resolveIndexedThemes('Blanche-Neige').map(t=>t.id),['blanche-neige']);
assert.deepEqual(instance.relatedThemesForQuery('Blanche-Neige'),[]);
assert.deepEqual(instance.relatedThemesForQuery('argent'),[]);
assert.deepEqual(instance.resolveIndexedThemes('argent').map(t=>t.id),['argent']);
assert.deepEqual(instance.relatedThemesForQuery('contestation'),[]);
assert.deepEqual(instance.relatedThemesForQuery('contemplation'),[]);
const vanilla=engine.create(themes,runtime);
assert.deepEqual(vanilla.relatedThemesForQuery('conte'),[]);
console.log('SEMANTIC_ENGINE_PASS 1267 canonical themes, '+Object.keys(nav.queries).length+
  ' checked related search phrases; strict themes/exact search remain unchanged');
