/* BIBLAW 085 — public, owner-provided frequently asked questions.
   The FAQ only references Psalms already contained in the public browser catalog. */
(() => {
  'use strict';
  const $=id=>document.getElementById(id);
  const state={questions:[],byId:new Map(),records:new Map(),openPsalm:null,current:null,
    lastLink:null,lastScroll:0,loading:null};
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
  function renderIndex(){
    $('faqList').replaceChildren();
    for(const question of state.questions){
      const b=document.createElement('button');b.type='button';
      b.className='faq-question-item';
      const title=document.createElement('span');title.className='faq-question-title';title.textContent=question.title;
      const chevron=document.createElement('span');chevron.className='faq-chevron';
      chevron.textContent='›';chevron.setAttribute('aria-hidden','true');
      b.append(title,chevron);
      b.onclick=()=>showAnswer(question.id);
      $('faqList').append(b);
    }
  }
  function appendAnswerWithLinks(container,question){
    const refs=question.references||[];
    const answer=String(question.answer||'');
    let cursor=0;
    for(const ref of refs){
      const at=answer.indexOf(ref.label,cursor);
      if(at<cursor)throw Error('La référence ne correspond pas au texte');
      container.append(document.createTextNode(answer.slice(cursor,at)));
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
    container.append(document.createTextNode(answer.slice(cursor)));
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
    state.loading=fetch('data/faq-public-085.json?v=089').then(async response=>{
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
      const extraUrls=[1,2,3,4,5,6,7,8,9].map(n=>'data/faq-091-'+n+'.json?v=091');
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
      const response092=await fetch('data/faq-092.json?v=092');
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
      const questions=data.questions.concat(newQuestions,questions091,questions092,questions093);
      if(questions.length!==54||new Set(questions.map(q=>q.id)).size!==54)
        throw Error('Liste des questions invalide.');
      for(const q of questions)for(const ref of q.references)if(!validReference(ref))
        throw Error('Référence de psaume introuvable : '+ref.recordId);
      state.questions=questions;
      state.byId=new Map(state.questions.map(q=>[q.id,q]));
      renderIndex();showStatus('');
      return true;
    }).catch(error=>{showStatus(error.message);console.error(error);return false;});
    return state.loading;
  }
  function open(){
    $('faqLibrary').hidden=false;
    document.body.classList.add('view-faq');
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
      BiblawPDF.download({recordType:'faq',id:q.id,title:q.title,text:q.answer});
      showStatus('');
    }catch(error){showStatus('Impossible de créer le PDF : '+error.message);}
  }
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
