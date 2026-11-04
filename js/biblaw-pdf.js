/* BIBLAW: PDF export directly in browser, selectable French text, no CDN. */
(() => {
 'use strict';
 const special={'€':128,'‚':130,'ƒ':131,'„':132,'…':133,'†':134,'‡':135,'ˆ':136,'‰':137,'Š':138,'‹':139,'Œ':140,'Ž':142,'‘':145,'’':146,'“':147,'”':148,'•':149,'–':150,'—':151,'˜':152,'™':153,'š':154,'›':155,'œ':156,'ž':158,'Ÿ':159};
 const hex=s=>[...String(s||'').normalize('NFC')].map(c=>{let v=c.codePointAt(0);if(v>=32&&v<=126||v>=160&&v<=255)return v;if(special[c])return special[c];if(c==='\n'||c==='\t'||c==='\r')return 32;let x=c.normalize('NFKD').replace(/[\u0300-\u036f]/g,'');return x.length===1&&x.codePointAt(0)>=32&&x.codePointAt(0)<127?x.codePointAt(0):63}).map(x=>x.toString(16).padStart(2,'0')).join('').toUpperCase();
 const slug=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-zA-Z0-9_-]/g,'-').slice(0,80);
 const parts=(record,mode='both')=>{
  if(!record)throw Error('Document introuvable');
  const psalm=record.recordType==='psalm',pray=record.attachedPrayer&&record.attachedPrayer.text;
  const blocks=[],add=(kind,text)=>blocks.push({kind,text:String(text||'')});
  let title='',filename='';
  if(psalm){
   if(!['psalm','prayer','both'].includes(mode))throw Error('Choix incorrect');
   if(mode==='prayer'&&!pray)throw Error('Prière absente');
   const p=mode!=='prayer',q=mode!=='psalm'&&pray;
   title=p?'Psaume '+record.number:'Prière '+record.attachedPrayer.number;
   filename='Biblaw_'+slug('L'+(record.book?.number||'')+'-P'+record.number+'-'+(q&&!p?'priere':q?'psaume-priere':'psaume'))+'.pdf';
   if(p){add('title','Psaume '+record.number+' — '+(record.title||''));if(record.book?.number)add('meta','Livre '+record.book.number);for(const v of record.verses||[])add('text',v.number+'. '+v.text);}
   if(q){if(p)add('gap','');add('title','Prière '+record.attachedPrayer.number);for(const line of record.attachedPrayer.text.split(/\n/))add('text',line);}
  }else if(record.recordType==='master-prayer'){title='Prière '+record.number;filename='Biblaw_Priere_'+slug(record.number||record.id)+'.pdf';add('title',title);add('text',record.text);}
  else if(record.recordType==='note'){title='Note';filename='Biblaw_Note_'+slug(record.id)+'.pdf';add('title',record.title||title);add('text',record.text||record.summary);}
  else if(record.recordType==='faq'){
    title=String(record.title||'Question');
    filename='Biblaw_Question_'+slug(record.id||'reponse')+'.pdf';
    add('title',title);add('text',record.text);
  }
  else throw Error('Type de texte non exportable');
  if(!blocks.some(b=>b.kind==='text'&&b.text))throw Error('Texte indisponible');
  return{title,filename,blocks};
 };
 function createPDF(record,mode='both'){
  const {filename,blocks}=parts(record,mode),pages=[];let cmds=[],y=789;
  const canvas=typeof document==='undefined'?null:document.createElement('canvas'),ctx=canvas?.getContext?.('2d');
  const width=500,measure=(s,size)=>{if(ctx){ctx.font=size+'px Helvetica,Arial,sans-serif';return ctx.measureText(s).width;}return s.length*size*.55;};
  function newPage(){if(cmds.length)pages.push(cmds.join('\n'));cmds=[];y=789;}
  function draw(s,size=11,bold=false){if(y<57)newPage();if(s)cmds.push('BT /'+(bold?'F2':'F1')+' '+size+' Tf 1 0 0 1 47 '+y.toFixed(2)+' Tm <'+hex(s)+'> Tj ET');y-=size+5;}
  function wrap(text,size,bold){
   for(const paragraph of String(text||'').split(/\n/)){
    if(!paragraph.trim()){draw('',size,bold);continue;}
    let current='';
    for(const word of paragraph.split(/\s+/)){
     if(!word)continue;
     let next=current?current+' '+word:word;
     if(measure(next,size)<=width){current=next;continue;}
     if(current){draw(current,size,bold);current='';}
     if(measure(word,size)<=width){current=word;continue;}
     let chunk='';
     for(const c of word){if(chunk&&measure(chunk+c,size)>width){draw(chunk,size,bold);chunk='';}chunk+=c;}
     current=chunk;
    }
    if(current)draw(current,size,bold);
   }
  }
  for(const b of blocks){if(b.kind==='gap'){y-=17;continue;}const title=b.kind==='title',meta=b.kind==='meta';if(title)y-=7;wrap(b.text,title?15:meta?9:11,title);if(title||meta)y-=8;}
  if(cmds.length)pages.push(cmds.join('\n'));
  const objects=['','<< /Type /Catalog /Pages 2 0 R >>','','<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>','<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>'];
  const kids=[];
  pages.forEach((content,i)=>{const page=5+2*i,stream=page+1;kids.push(page+' 0 R');objects[page]='<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents '+stream+' 0 R >>';objects[stream]='<< /Length '+content.length+' >>\nstream\n'+content+'\nendstream';});
  objects[2]='<< /Type /Pages /Kids ['+kids.join(' ')+'] /Count '+pages.length+' >>';
  let out='%PDF-1.4\n',offsets=[0];
  for(let i=1;i<objects.length;i++){offsets[i]=out.length;out+=i+' 0 obj\n'+objects[i]+'\nendobj\n';}
  const xref=out.length;out+='xref\n0 '+objects.length+'\n0000000000 65535 f \n';
  for(let i=1;i<objects.length;i++)out+=String(offsets[i]).padStart(10,'0')+' 00000 n \n';
  out+='trailer\n<< /Size '+objects.length+' /Root 1 0 R >>\nstartxref\n'+xref+'\n%%EOF\n';
  return{blob:new Blob([out],{type:'application/pdf'}),filename,pages:pages.length};
 }
 function download(record,mode){
  const f=createPDF(record,mode),url=URL.createObjectURL(f.blob),a=document.createElement('a');
  a.href=url;a.download=f.filename;a.hidden=true;document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),60000);
  return f.filename;
 }
 globalThis.BiblawPDF=Object.freeze({parts,createPDF,download});
})();