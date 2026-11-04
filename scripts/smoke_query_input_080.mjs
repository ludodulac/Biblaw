import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../js/biblaw.js',import.meta.url),'utf8');
const html=readFileSync(new URL('../index.html',import.meta.url),'utf8');
const start=source.indexOf('function repeatedWholeWordCorrection(value)');
const end=source.indexOf('function correctMobileQueryDuplicate()',start);
assert.ok(start>=0 && end>start,'query correction function exists');
const correct=vm.runInNewContext('('+source.slice(start,end).trim()+')');
for(const [input,output] of [
  ['AmourAmour','Amour'],
  ['amouramour','amour'],
  ['LumièreLUMIÈRE','Lumière'],
  ['ChouetteChouette','Chouette'],
  ['énergieénergie','énergie'],
  ['amour',null],
  ['amour amour',null],
  ['l’amour l’amour',null],
  ['Montagne sacréeMontagne sacrée',null],
  ['coucou',null],
  ['20202020',null],
  ['bonjourbonjour!',null]
])assert.equal(correct(input),output,input);
const searchStart=source.slice(source.indexOf('function search(){'),source.indexOf('function summary('));
assert.ok(searchStart.includes('correctMobileQueryDuplicate();'),'Search must still de-duplicate mobile input');
for(const event of ['blur','change','focus','compositionend'])assert.ok(source.includes("'"+event+"',"),event);
assert.match(html,/id="query" type="search" value="" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" enterkeyhint="search"/);
assert.ok(Number(html.match(/js\/biblaw\.js\?v=(\d+)/)?.[1])>=80,'Expected a current cache-busted app file');
console.log('080 PASS: single-word duplicate correction, normal phrases unaffected, mobile input guards and cache refresh');
