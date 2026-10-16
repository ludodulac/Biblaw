(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;if(root)root.BiblawQuestionPsalmRanker=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
  const norm=x=>String(x||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/œ/g,'oe').replace(/æ/g,'ae').replace(/[’']/g,' ').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
  const stop=new Set('que qui quoi quel quelle quels quelles comment pourquoi est ce qu est la le les l un une des du de d dans sur au aux a et ou pour par en avec son sa ses leur leurs il elle ils elles nous vous je tu on homme archanges archange dieu dire disent devenir devient developper cultiver faire peut doit'.split(' '));
  const tokens=q=>norm(q).split(' ').filter(w=>w.length>=3&&!stop.has(w));
  const stem=w=>w.length>=7?w.slice(0,-2):w.length>=5?w.slice(0,-1):w;
  const score=(query,themeLabel,occurrence,record)=>{
    const words=tokens(query),theme=new Set(tokens(themeLabel).map(stem)),focus=words.filter(w=>!theme.has(stem(w)));
    if(!focus.length)return 0;
    const teaching=norm(occurrence?.teaching),verseNumbers=new Set(occurrence?.verseNumbers||[]);
    const selected=(record?.verses||[]).filter(v=>verseNumbers.has(v.number)).map(v=>norm(v.text));
    const evidence=[teaching,...selected].filter(Boolean);
    let total=0;
    for(const word of focus){const root=stem(word),re=new RegExp('(?:^| )'+root+'[a-z]*(?: |$)');
      if(re.test(teaching))total+=3;
      if(selected.some(t=>re.test(t)))total+=2;
    }
    // Preserve the original importance ordering unless at least one distinct
    // question-specific notion is grounded in the indexed evidence.
    return total;
  };
  const isSpecific=q=>/\?/.test(q)||/^(que|qui|comment|pourquoi|qu est|quel|quelle|ou|quand)\b/i.test(norm(q));
  const rerank=(items,query,themeLabel)=>{
    if(!isSpecific(query))return items.slice();
    return items.map((item,i)=>({item,i,s:score(query,themeLabel,item.thematic,item.record)})).sort((a,b)=>b.s-a.s||a.i-b.i).map(x=>x.item);
  };
  return{norm,tokens,score,isSpecific,rerank};
});
