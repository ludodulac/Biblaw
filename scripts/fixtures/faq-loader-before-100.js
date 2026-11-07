// Archival snapshot from released version before FAQ 100. Used by the
// historical 085–098 tests to verify the untouched source answers; the
// current production loader is tested separately by check_faq_dom and Chromium.
/* BIBLAW 085 — public, owner-provided frequently asked questions.
   The FAQ only references Psalms already contained in the public browser catalog. */
(() => {
  'use strict';
  const $=id=>document.getElementById(id);
  const state={questions:[],byId:new Map(),records:new Map(),openPsalm:null,current:null,
    lastLink:null,lastScroll:0,loading:null,routes:[],aliases:new Map()};
  const labelNumber=(n,verses)=>'Psaume '+n+', verset'+(verses.length>1?'s':'')+' '+verses.join(', ');
  function validReference(ref){
    const record=state.records.get(ref.recordId);
    return Boolean(record&&record.recordType==='psalm'&&
      record.archangel===ref.archangel&&Number(record.number)===Number(ref.number)&&
      Array.isArray(ref.verses)&&ref.verses.length>0&&
      ref.verses.every(n=>record.verses?.some(verse=>Number(verse.number)===n)));
  }
  // 090: build cited verse links from the author's unchanged words; never guess a Psalm.
  function linkedReferences(question,bookNumbers,expectedCitations=4){
    const pattern=/\(psaume\s+(\d+)\s+(?:de\s+|d['’])\s*(Michaël|Gabriel|Raphaël|Ouriel),\s+versets?\s+([^)]+)\)/g;
    const matches=[...String(question.answer||'').matchAll(pattern)];
    if(matches.length!==expectedCitations||question.answer.split('(psaume ').length!==expectedCitations+1)
      throw Error('Références incomplètes : '+question.id);
    const references=matches.map(match=>{
      const number=Number(match[1]),archangel=match[2].normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
      const book=bookNumbers[archangel+':'+number];
      if(!Number.isInteger(book))throw Error('Psaume non identifié : '+match[0]);
      const verses=[],tail=match[3].replace(/(\d+)\s+à\s+(\d+)/g,(_,start,end)=>{
        const a=Number(start),b=Number(end);
        if(b<a||b-a>100)throw Error('Plage de versets invalide');
        for(let i=a;i<=b;i++)verses.push(i);
        return '';
      });
      for(const digit of tail.matchAll(/\d+/g))verses.push(Number(digit[0]));
      const selected=[...new Set(verses)].sort((a,b)=>a-b);
      if(!selected.length)throw Error('Versets introuvables : '+match[0]);
      return {label:match[0],recordId:'book-'+String(book).padStart(2,'0')+
        '-psalm-'+String(number).padStart(3,'0'),archangel,number,verses:selected};
    });
    if(question.references?.length){
      if(JSON.stringify(question.references)!==JSON.stringify(references))
        throw Error('Références contradictoires : '+question.id);
    }
    return {...question,references};
  }
  function showStatus(message){
    $('faqStatus').textContent=message;
    $('faqStatus').hidden=!message;
  }
  function normalizeQuestion(text){
    return String(text||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'')
      .toLowerCase().replace(/[’']/g,' ').replace(/[^a-z0-9]+/g,' ').trim();
  }
  function renderIndex(){
    $('faqList').replaceChildren();
    const query=normalizeQuestion($('faqSearch').value);
    let shown=0;
    for(const question of state.questions){
      const texts=[question.title,...(state.aliases.get(question.id)||[])];
      if(query&&!texts.some(text=>normalizeQuestion(text).includes(query)))continue;
      shown++;
      const b=document.createElement('button');b.type='button';
      b.className='faq-question-item';
      const title=document.createElement('span');title.className='faq-question-title';title.textContent=question.title;
      const chevron=document.createElement('span');chevron.className='faq-chevron';
      chevron.textContent='›';chevron.setAttribute('aria-hidden','true');
      b.append(title,chevron);
      b.onclick=()=>showAnswer(question.id);
      $('faqList').append(b);
    }
    const unsupported=state.routes.some(route=>route.resolution==='unsupported'&&
      normalizeQuestion(route.question)===query);
    $('faqSearchStatus').textContent=query
      ?(unsupported?'Aucune réponse fondée dans les psaumes pour cette question.':
        shown+' réponse'+(shown>1?'s':'')+' trouvée'+(shown>1?'s':''))
      :'';
  }
  // 098: preserve author-written subsection headings as visible bold text, without rendering markup as HTML.
  function appendFormattedText(container,fragment){
    const bold=/\*\*([^*\n]+)\*\*/g;
    let cursor=0;
    for(const match of fragment.matchAll(bold)){
      container.append(document.createTextNode(fragment.slice(cursor,match.index)));
      const strong=document.createElement('strong');
      strong.textContent=match[1];
      container.append(strong);
      cursor=match.index+match[0].length;
    }
    container.append(document.createTextNode(fragment.slice(cursor)));
  }
  function appendAnswerWithLinks(container,question){
    const refs=question.references||[];
    const answer=String(question.answer||'');
    let cursor=0;
    for(const ref of refs){
      const at=answer.indexOf(ref.label,cursor);
      if(at<cursor)throw Error('La référence ne correspond pas au texte');
      appendFormattedText(container,answer.slice(cursor,at));
      const button=document.createElement('button');
      button.type='button';button.className='faq-psalm-link';
      button.textContent=ref.label;
      const valid=validReference(ref);
      button.disabled=!valid;
      button.title=valid?'Lire '+labelNumber(ref.number,ref.verses):'Référence non disponible dans le corpus public';
      button.setAttribute('aria-label',button.title);
      if(valid)button.onclick=()=>{
        if(typeof state.openPsalm!=='function'){showStatus('Lecteur des psaumes indisponible.');return;}
        state.lastLink=button;state.lastScroll=window.scrollY;
        state.openPsalm(ref);
      };
      container.append(button);
      cursor=at+ref.label.length;
    }
    appendFormattedText(container,answer.slice(cursor));
  }
  function showAnswer(id){
    const question=state.byId.get(id);if(!question)return;
    state.current=question;
    $('faqIndex').hidden=true;$('faqAnswer').hidden=false;
    $('faqAnswerTitle').textContent=question.title;
    $('faqAnswerBody').replaceChildren();
    appendAnswerWithLinks($('faqAnswerBody'),question);
    showStatus('');
    window.scrollTo({top:0,behavior:'instant'});
    $('faqAnswerTitle').setAttribute('tabindex','-1');
    $('faqAnswerTitle').focus({preventScroll:true});
  }
  function backToIndex(){
    state.current=null;
    $('faqIndex').hidden=false;$('faqAnswer').hidden=true;
    showStatus('');
    window.scrollTo({top:0,behavior:'instant'});
  }
  async function init(records){
    state.records=new Map((records||[]).map(r=>[r.id,r]));
    if(state.loading)return state.loading;
    state.loading=fetch('data/faq-public-085.json?v=099').then(async response=>{
      if(!response.ok)throw Error('Les questions ne sont pas disponibles.');
      const data=await response.json();
      if(data.version!==5||data.questions?.length!==25||
         data.questions.some(q=>!q.id||!q.title||!q.answer||!Array.isArray(q.references)))
        throw Error('Fichier de questions invalide.');
      const urls=[1,2,3,4,5].map(n=>'data/faq-090-'+n+'.json?v=090');
      const [books,...additional]=await Promise.all([
        'data/faq-090-books.json?v=090',...urls
      ].map(async url=>{
        const r=await fetch(url);
        if(!r.ok)throw Error('Questions supplémentaires indisponibles : '+url);
        return r.json();
      }));
      if(books.version!==1||Object.keys(books.verifiedPsalms||{}).length!==15||
          additional.length!==5)throw Error('Références 090 incomplètes.');
      const newQuestions=additional.map((q,i)=>{
        if(q.id!=='faq-presence-dieu-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 090 absente ou incorrecte.');
        return linkedReferences(q,books.verifiedPsalms);
      });
      // 091: exactly nine additional owner-authored answers, with validated canonical Psalm links.
  // The citation counts are pinned to the corrected editorial data; every citation must resolve.
      const extraUrls=[1,2,3,4,5,6,7,8,9].map(n=>'data/faq-091-'+n+'.json?v=099');
      const [newBookData,...newAnswers]=await Promise.all([
        'data/faq-091-books.json?v=091',...extraUrls
      ].map(async url=>{
        const response=await fetch(url);
        if(!response.ok)throw Error('Questions 091 indisponibles : '+url);
        return response.json();
      }));
      if(newBookData.version!==1||Object.keys(newBookData.verifiedPsalms||{}).length!==24||
          newAnswers.length!==9)throw Error('Références 091 incomplètes.');
      const questions091=newAnswers.map((q,i)=>{
        if(q.id!=='faq-priere-paix-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 091 absente ou incorrecte.');
        return linkedReferences(q,newBookData.verifiedPsalms,i===0?3:4);
      });
      // 092: ten verbatim owner-authored answers, with 30 verified Psalm citations.
      const response092=await fetch('data/faq-092.json?v=099');
      if(!response092.ok)throw Error('Questions 092 indisponibles.');
      const data092=await response092.json();
      if(data092.version!==1||Object.keys(data092.verifiedPsalms||{}).length!==16||
          data092.questions?.length!==10)throw Error('Références 092 incomplètes.');
      const questions092=data092.questions.map((q,i)=>{
        if(q.id!=='faq-religions-science-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 092 absente ou incorrecte.');
        return linkedReferences(q,data092.verifiedPsalms,3);
      });
      // 093: five owner-authored questions on personal meaning, preserving full paragraphs.
      const response093=await fetch('data/faq-093.json?v=093');
      if(!response093.ok)throw Error('Questions 093 indisponibles.');
      const data093=await response093.json();
      if(data093.version!==1||Object.keys(data093.verifiedPsalms||{}).length!==6||
          data093.questions?.length!==5)throw Error('Références 093 incomplètes.');
      const questions093=data093.questions.map((q,i)=>{
        if(q.id!=='faq-sens-personnel-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 093 absente ou incorrecte.');
        return linkedReferences(q,data093.verifiedPsalms,3);
      });
      // 094: six complete author-written articles on happiness and five related questions.
      const response094=await fetch('data/faq-094.json?v=094');
      if(!response094.ok)throw Error('Questions 094 indisponibles.');
      const data094=await response094.json();
      if(data094.version!==1||Object.keys(data094.verifiedPsalms||{}).length!==9||
          data094.questions?.length!==6)throw Error('Références 094 incomplètes.');
      const questions094=data094.questions.map((q,i)=>{
        if(q.id!=='faq-bonheur-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 094 absente ou incorrecte.');
        return linkedReferences(q,data094.verifiedPsalms,i===5?4:3);
      });
      // 095: seven complete owner-authored answers on thoughts, emotions and self-mastery.
      const response095=await fetch('data/faq-095.json?v=095');
      if(!response095.ok)throw Error('Questions 095 indisponibles.');
      const data095=await response095.json();
      if(data095.version!==1||Object.keys(data095.verifiedPsalms||{}).length!==14||
          data095.questions?.length!==7)throw Error('Références 095 incomplètes.');
      const expected095=[3,3,3,3,4,4,5];
      const questions095=data095.questions.map((q,i)=>{
        if(q.id!=='faq-maitrise-interieure-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 095 absente ou incorrecte.');
        return linkedReferences(q,data095.verifiedPsalms,expected095[i]);
      });
      // 096: seven articles on harmony, seven on consciousness, all owner-authored.
      const response096=await fetch('data/faq-096.json?v=099');
      if(!response096.ok)throw Error('Questions 096 indisponibles.');
      const data096=await response096.json();
      if(data096.version!==1||Object.keys(data096.verifiedPsalms||{}).length!==28||
          data096.questions?.length!==14)throw Error('Références 096 incomplètes.');
      const expected096=[4,4,4,4,4,4,4,4,7,6,4,4,6,5];
      const questions096=data096.questions.map((q,i)=>{
        if(q.id!=='faq-harmonie-conscience-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 096 absente ou incorrecte.');
        return linkedReferences(q,data096.verifiedPsalms,expected096[i]);
      });
      // 097: eight complete owner-authored questions about spiritual reality.
      const response097=await fetch('data/faq-097.json?v=097');
      if(!response097.ok)throw Error('Questions 097 indisponibles.');
      const data097=await response097.json();
      if(data097.version!==1||Object.keys(data097.verifiedPsalms||{}).length!==19||
          data097.questions?.length!==8)throw Error('Références 097 incomplètes.');
      const expected097=[3,3,3,4,3,3,4,4];
      const questions097=data097.questions.map((q,i)=>{
        if(q.id!=='faq-realite-spirituelle-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 097 absente ou incorrecte.');
        return linkedReferences(q,data097.verifiedPsalms,expected097[i]);
      });
      // 098: thirteen complete articles about everyday spiritual practice.
      const response098=await fetch('data/faq-098.json?v=099');
      if(!response098.ok)throw Error('Questions 098 indisponibles.');
      const data098=await response098.json();
      if(data098.version!==1||Object.keys(data098.verifiedPsalms||{}).length!==25||
          data098.questions?.length!==13)throw Error('Références 098 incomplètes.');
      const expected098=[3,5,4,4,5,5,4,5,5,5,5,6,18];
      const questions098=data098.questions.map((q,i)=>{
        if(q.id!=='faq-pratique-spirituelle-'+(i+1)||!q.title||!q.answer)
          throw Error('Question 098 absente ou incorrecte.');
        return linkedReferences(q,data098.verifiedPsalms,expected098[i]);
      });
      // 099 — Exactly three new canonical answers; the other formulations
      // are routed to existing entries, never duplicated in the index.
      const [response099,responseRoutes]=await Promise.all([
        fetch('data/faq-099.json?v=100'),fetch('data/faq-099-routing.json?v=100')
      ]);
      if(!response099.ok||!responseRoutes.ok)throw Error('Questions 19 et 20 indisponibles.');
      const data099=await response099.json();
      const routeData=await responseRoutes.json();
      if(data099.version!==1||data099.questions?.length!==3||
          Object.keys(data099.verifiedPsalms||{}).length!==9)
        throw Error('Nouvelles réponses 099 incomplètes.');
      const expected099=[7,5,6];
      const questions099=data099.questions.map((q,i)=>linkedReferences(q,data099.verifiedPsalms,expected099[i]));
      const questions=data.questions.concat(newQuestions,questions091,questions092,questions093,questions094,questions095,questions096,questions097,questions098,questions099);
      if(questions.length!==105||new Set(questions.map(q=>q.id)).size!==105)
        throw Error('Liste des questions invalide.');
      for(const q of questions)for(const ref of q.references)if(!validReference(ref))
        throw Error('Référence de psaume introuvable : '+ref.recordId);
      state.questions=questions;
      state.byId=new Map(state.questions.map(q=>[q.id,q]));
      if(routeData.version!==1||routeData.routes?.length!==19)
        throw Error('Correspondances des 19 questions incomplètes.');
      const numbers=new Set();
      state.aliases=new Map();
      const counts={new:0,reuse:0,redirect_new:0,unsupported:0};
      for(const route of routeData.routes){
        if(!Number.isInteger(route.number)||numbers.has(route.number)||!route.question||
           !(route.resolution in counts))throw Error('Correspondance de question incorrecte.');
        numbers.add(route.number);counts[route.resolution]++;
        if(route.resolution==='unsupported'){
          if(route.target_id!==null)throw Error('Question sans source avec cible.');
          continue;
        }
        const question=state.byId.get(route.target_id);
        if(!question)throw Error('Correspondance introuvable : '+route.question);
        if(route.resolution==='new'&&question.title!==route.question)
          throw Error('Titre de la nouvelle réponse incohérent.');
        const aliases=state.aliases.get(question.id)||[];
        aliases.push(route.question);
        state.aliases.set(question.id,aliases);
      }
      if(numbers.size!==19||counts.new!==3||counts.reuse!==12||
         counts.redirect_new!==2||counts.unsupported!==2)
        throw Error('Classement 19/20 incohérent.');
      state.routes=routeData.routes;
      renderIndex();showStatus('');
      return true;
    }).catch(error=>{showStatus(error.message);console.error(error);return false;});
    return state.loading;
  }
  function open(){
    $('faqLibrary').hidden=false;
    document.body.classList.add('view-faq');
    $('faqSearch').value='';
    renderIndex();
    backToIndex();
    if(!state.questions.length)showStatus('Chargement des questions…');
    $('faqClose').focus({preventScroll:true});
  }
  function close(){
    document.body.classList.remove('view-faq');
    $('faqLibrary').hidden=true;
  }
  function restoreAfterPsalm(){
    if($('faqLibrary').hidden||!state.current)return;
    // The answer and scroll position are kept, even across multiple referenced Psalms.
    window.scrollTo({top:state.lastScroll,behavior:'instant'});
    state.lastLink?.focus({preventScroll:true});
  }
  function download(){
    const q=state.current;if(!q)return;
    try{
      // Bold is a typographic heading, not literal asterisks in the exported PDF.
      BiblawPDF.download({recordType:'faq',id:q.id,title:q.title,
        text:q.answer.replace(/\*\*([^*\n]+)\*\*/g,'$1')});
      showStatus('');
    }catch(error){showStatus('Impossible de créer le PDF : '+error.message);}
  }
  $('faqSearch').oninput=renderIndex;
  $('faqBack').onclick=backToIndex;
  $('faqClose').onclick=()=>{
    close();window.scrollTo({top:0,behavior:'instant'});
    $('faqToggle').focus({preventScroll:true});
  };
  $('faqPdf').onclick=download;
  $('faqPrint').onclick=()=>window.print();
  globalThis.BiblawFAQ=Object.freeze({
    init,open,close,restoreAfterPsalm,
    setOpenPsalm(callback){state.openPsalm=callback;}
  });
})();
