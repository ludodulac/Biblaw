/* BIBLAW 082 — suggestions from the already-published corpus only.
   Never reads historic/private notes, and never changes original source text. */
(function (root) {
  'use strict';
  const norm = value => String(value || '').normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/œ/g, 'oe').replace(/æ/g, 'ae')
    .replace(/[’']/g, ' ').replace(/[^a-z0-9\s-]/g, ' ')
    .replace(/-/g, ' ').replace(/\s+/g, ' ').trim();

  const SMALL = ['zéro','un','deux','trois','quatre','cinq','six','sept','huit','neuf',
    'dix','onze','douze','treize','quatorze','quinze','seize','dix-sept',
    'dix-huit','dix-neuf'];
  const TENS = {20:'vingt',30:'trente',40:'quarante',50:'cinquante',60:'soixante'};
  function under100(n,nonTerminal=false) {
    if(n<20)return SMALL[n];
    if(n<70) {
      const tens=Math.floor(n/10)*10,unit=n%10;
      return TENS[tens]+(unit===0?'':unit===1?' et un':'-'+SMALL[unit]);
    }
    if(n<80)return n===71?'soixante et onze':'soixante-'+SMALL[n-60];
    if(n===80)return nonTerminal?'quatre-vingt':'quatre-vingts';
    return 'quatre-vingt-'+SMALL[n-80];
  }
  function under1000(n,nonTerminal=false) {
    if(n<100)return under100(n,nonTerminal);
    const h=Math.floor(n/100),rest=n%100;
    const base=(h===1?'':SMALL[h]+' ')+'cent';
    if(!rest)return h>1&&!nonTerminal?base+'s':base;
    return base+' '+under100(rest,nonTerminal);
  }
  function writtenNumber(n) {
    if(!Number.isSafeInteger(n)||n<0||n>9999)return null;
    if(!n)return 'zéro';
    const thousands=Math.floor(n/1000),rest=n%1000;
    return [thousands?(thousands===1?'mille':under1000(thousands,true)+' mille'):'',rest?under1000(rest):''].filter(Boolean).join(' ');
  }
  let NUMBER_MAP=null;
  function numberMap(){
    if(NUMBER_MAP)return NUMBER_MAP;
    NUMBER_MAP=new Map();
    for(let n=0;n<=9999;n++){
      NUMBER_MAP.set(norm(writtenNumber(n)),n);
      if(n===80)NUMBER_MAP.set('quatre vingt',n);
      if(n>=200&&n<=900&&n%100===0)NUMBER_MAP.set(norm(writtenNumber(n).replace(/cents$/,'cent')),n);
    }
    return NUMBER_MAP;
  }
  function numericValue(value){
    const raw=String(value||'').trim();
    if(/^\d{1,4}$/u.test(raw))return Number(raw);
    return numberMap().get(norm(raw))??null;
  }
  function otherNumericForm(value){
    const key=String(value||'').trim(),n=numericValue(key);
    if(n===null)return null;
    return /^\d+$/u.test(key)?writtenNumber(n):String(n);
  }

  function createIndex() {
    const words=new Map();
    const tokenize = str => String(str||'').match(/[\p{L}\p{M}\p{N}]+/gu)||[];
    const category = r => (r.recordType==='master-prayer'?'prayer':r.recordType)+':'+(r.archangel||'');
    function addRecord(record) {
      if(!record||!['psalm','master-prayer','note'].includes(record.recordType))return;
      // Only passed records, which must come from the browser's public catalog.
      const scope=category(record);
      const fragments=record.recordType==='psalm'?
        [record.title,...(record.verses||[]).map(v=>v.text)]:
        [record.title,record.text,record.summary];
      for(const fragment of fragments){
        for(const original of tokenize(fragment)){
          const key=norm(original);
          if(key.length<2&&!/^\d$/u.test(key))continue;
          if(!/^[a-z0-9]+$/u.test(key))continue;
          let item=words.get(key);
          if(!item){
            item={key,label:original,frequency:0,scope:new Set()};
            words.set(key,item);
          }
          item.frequency++;
          item.scope.add(scope);
          // Keep real accented French spelling if both variants occur.
          if(!/[\u00C0-\u024F]/u.test(item.label)&&/[\u00C0-\u024F]/u.test(original))item.label=original;
        }
      }
    }
    function hasScope(entry,types,archangel){
      if(!types||!types.size)return false;
      for(const scope of entry.scope){
        const [kind,arch]=scope.split(':');
        if(types.has(kind)&&(!archangel||arch===archangel))return true;
      }
      return false;
    }
    function suggestions(input,mode,types,archangel,themeDirectory,recordById,limit=6){
      const key=norm(input);
      if((key.length<2&&!/^\d$/u.test(key))||key.includes(' ')&&numericValue(input)===null)return[];
      const output=[],seen=new Set();
      const add=(label,kind,target)=>{const id=kind+':'+norm(label);if(seen.has(id))return;seen.add(id);output.push({label,kind,value:target||label});};
      if(mode==='themes'&&types?.has('psalm')){
        const themes=(themeDirectory||[]).filter(theme=>{
          if(!norm(theme.label).startsWith(key))return false;
          return !archangel||(theme.occurrences||[]).some(row=>recordById?.get(row.recordId)?.archangel===archangel);
        }).sort((a,b)=>a.label.localeCompare(b.label,'fr',{sensitivity:'base'}));
        for(const theme of themes.slice(0,Math.min(2,limit)))add(theme.label,'theme',theme.label);
      }
      const numeric=numericValue(input);
      const wordHits=[...words.values()].filter(item=>hasScope(item,types,archangel)&&
        (item.key.startsWith(key)||(numeric!==null&&numericValue(item.key)===numeric)));
      wordHits.sort((a,b)=>{
        const rank=item=>item.key===key?0:
          numeric!==null&&numericValue(item.key)===numeric?1:2;
        return rank(a)-rank(b)||a.key.localeCompare(b.key,'fr',{sensitivity:'base'})||
          b.frequency-a.frequency;
      });
      for(const item of wordHits){if(output.length>=limit)break;add(item.label,'word',item.label);}
      return output.slice(0,limit);
    }
    return {addRecord,suggestions,wordCount:()=>words.size};
  }

  // For numeric queries, count whole spelled numbers, rather than pieces of
  // "quatre-vingts" as an isolated "quatre". Source corpus fragments only.
  function countNumericOccurrences(fragments,query){
    const number=numericValue(query);
    if(number===null)return null;
    let total=0;
    for(const fragment of fragments||[]){
      const tokens=norm(fragment).match(/[a-z0-9]+/g)||[];
      for(let i=0;i<tokens.length;){
        let bestLength=0,bestNumber=null;
        if(/^\d+$/u.test(tokens[i])){
          bestLength=1;bestNumber=numericValue(tokens[i]);
        }else{
          // Longest valid French numeral at this position (up to 8 tokens).
          for(let len=1;len<=8&&i+len<=tokens.length;len++){
            const val=numericValue(tokens.slice(i,i+len).join(' '));
            if(val!==null){bestLength=len;bestNumber=val;}
          }
        }
        if(bestLength){if(bestNumber===number)total++;i+=bestLength;}
        else i++;
      }
    }
    return total;
  }
  root.BiblawAutocomplete=Object.freeze({
    norm,numericValue,writtenNumber,otherNumericForm,createIndex,countNumericOccurrences
  });
})(globalThis);
