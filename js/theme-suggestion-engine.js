(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root)root.BiblawThemeEngine=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  const norm=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/[^a-z0-9\s-]/g,' ').replace(/-/g,' ').replace(/\s+/g,' ').trim();
  const stripLeadingArticle=value=>{const q=norm(value),parts=q.split(' ').filter(Boolean);return parts.length>1&&['l','le','la','les','un','une','des'].includes(parts[0])?parts.slice(1).join(' '):q;};
  const themeQueryForms=value=>{const q=norm(value),stripped=stripLeadingArticle(q);return [...new Set([q,stripped].filter(Boolean))];};
  const thematicFrenchStructure=value=>String(value||'').replace(/(^|\s)(?:d|c|n|s|j|m|l|qu)[’'](?=[A-Za-zÀ-ÖØ-öø-ÿŒœÆæ])/gi,'$1').replace(/-t-(?=(?:il|elle|on|ils|elles)\b)/gi,'-');
  const THEME_QUERY_STOP_WORDS=new Set(['a','avons','avec','ce','comment','dans','de','des','du','en','est','et','il','j','la','le','les','l','m','ma','ne','nous','on','ou','par','pas','peut','pour','pourquoi','qu','que','quelle','qui','sans','soit','sont','un','une']);
  const THEME_QUERY_EQUIVALENTS={'4':['4','quatre'],quatre:['quatre','4'],magique:['magique','magie'],magiques:['magiques','magie'],mourir:['mourir','mort'],meurt:['meurt','mourir','mort'],meurent:['meurent','mourir','mort'],mourons:['mourons','mourir','mort'],souffrons:['souffrons','souffrir','souffrance'],souffrent:['souffrent','souffrir','souffrance'],aimer:['aimer','amour'],enfants:['enfants','enfant']};
  const composeThemeQueryNotions=query=>{const terms=norm(query).split(' ').filter(Boolean),has=term=>terms.includes(term),hasAny=values=>values.some(has),existence=terms.some(term=>['existe','existent','existons','exister','existence'].includes(term)),why=has('pourquoi'),life=has('vivre')||has('vie'),representation=hasAny(['intention','intentions','croire','croyant','penser','pensant']),action=hasAny(['faire','agir','action','acte','actes']),moralOpposition=hasAny(['bien','bon','bonne','bonnes'])&&hasAny(['mal','mauvais','mauvaise','mauvaises']),questionedJustice=hasAny(['tromper','erreur','suffire','suffit','garantir','garantit','juste','justes']);if(representation&&action&&(moralOpposition||questionedJustice))return[new Set(['intention']),new Set(['acte'])];if((why&&existence)||(why&&life)||(has('raison')&&existence))return[new Set(['sens','but']),new Set(['vie'])];if(has('sens')&&existence)return[new Set(['sens']),new Set(['vie'])];if(has('but')&&existence)return[new Set(['but']),new Set(['vie'])];return[];};
  const themeQueryNotions=query=>{const seen=new Set();return[...composeThemeQueryNotions(query),...norm(thematicFrenchStructure(query)).split(' ').filter(term=>term&&!THEME_QUERY_STOP_WORDS.has(term)).map(term=>new Set(THEME_QUERY_EQUIVALENTS[term]||[term]))].filter(variants=>{const key=[...variants].sort().join('|');if(seen.has(key))return false;seen.add(key);return true;});};
  function create(themeDirectory,runtime){
    const themes=themeDirectory||[],themeById=new Map(themes.map(t=>[t.id,t]));
    function resolveIndexedThemes(query){const forms=themeQueryForms(query);if(!forms.length)return[];for(const q of forms){const alias=runtime?.aliases?.[q];if(alias?.themeIds?.length)return alias.themeIds.map(id=>themeById.get(id)).filter(Boolean);}for(const q of forms){const exact=themes.filter(t=>q===norm(t.label)||q===norm(t.id));if(exact.length)return exact;}return[];}
    function evaluate(query){
      const composedNotions=composeThemeQueryNotions(query),composedNotionCount=composedNotions.length,notions=themeQueryNotions(query);
      if(!notions.length)return{normalizedQuery:norm(query),recognizedNotions:[],composedNotions:[],candidateCountBeforeTop8:0,candidateRanking:[],top8:[]};
      const exactIds=new Set(resolveIndexedThemes(query).map(theme=>theme.id)),candidates=new Map();
      const consider=(theme,source,text)=>{if(!theme)return;const words=new Set(norm(text).split(' ').filter(Boolean)),matched=notions.map((variants,index)=>[...variants].some(term=>words.has(term))?index:-1).filter(index=>index>=0),hits=matched.length;if(!hits)return;const exact=exactIds.has(theme.id)?1:0,sourceRank=source==='label'?0:1,current=candidates.get(theme.id),candidate={theme,exact,hits,sourceRank,source,matched};if(!current||exact>current.exact||hits>current.hits||hits===current.hits&&sourceRank<current.sourceRank)candidates.set(theme.id,candidate);};
      for(const theme of themes)consider(theme,'label',theme.label);
      for(const[alias,entry]of Object.entries(runtime?.aliases||{}))for(const id of entry.themeIds||[])consider(themeById.get(id),'alias',alias);
      const ranked=[...candidates.values()].sort((a,b)=>b.exact-a.exact||b.hits-a.hits||a.sourceRank-b.sourceRank||a.theme.label.localeCompare(b.theme.label,'fr')||a.theme.id.localeCompare(b.theme.id,'fr')),selected=[],selectedIds=new Set(),add=item=>{if(item&&!selectedIds.has(item.theme.id)&&selected.length<8){selected.push(item);selectedIds.add(item.theme.id);}};
      const maxHits=ranked[0]?.hits||0;if(maxHits>1)for(const item of ranked)if(item.hits===maxHits)add(item);
      for(let index=0;index<composedNotionCount;index++)add(ranked.find(item=>item.matched.includes(index)));
      for(const item of ranked)add(item);
      const serializeNotion=variants=>[...variants].sort();
      const serializeCandidate=item=>({id:item.theme.id,label:item.theme.label,exact:Boolean(item.exact),hits:item.hits,sourceRank:item.sourceRank,provenance:item.source,matchedNotionIndexes:item.matched});
      return{normalizedQuery:norm(query),recognizedNotions:notions.map(serializeNotion),composedNotions:composedNotions.map(serializeNotion),candidateCountBeforeTop8:ranked.length,candidateRanking:ranked.map(serializeCandidate),top8:selected.map(item=>item.theme)};
    }
    return{resolveIndexedThemes,composeThemeQueryNotions,themeQueryNotions,suggestIndexedThemes:query=>evaluate(query).top8,evaluate};
  }
  return{norm,composeThemeQueryNotions,themeQueryNotions,create};
});
// Shared unchanged algorithm: browser UI and Node benchmark use this same module.\n