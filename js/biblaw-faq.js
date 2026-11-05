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
    state.loading=fetch('data/faq-public-085.json?v=086').then(async response=>{
      if(!response.ok)throw Error('Les questions ne sont pas disponibles.');
      const data=await response.json();
      if(data.version!==2||data.questions?.length!==8||
         data.questions.some(q=>!q.id||!q.title||!q.answer||!Array.isArray(q.references)))
        throw Error('Fichier de questions invalide.');
      for(const q of data.questions)for(const ref of q.references)if(!validReference(ref))
        throw Error('Référence de psaume introuvable : '+ref.recordId);
      state.questions=data.questions;
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
