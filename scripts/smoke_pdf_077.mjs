import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../js/biblaw-pdf.js',import.meta.url),'utf8');
const context={Blob,document:undefined};context.globalThis=context;
vm.runInNewContext(source,context);
const {parts,createPDF}=context.BiblawPDF;
const fixture={
 recordType:'psalm',id:'book-17-psalm-195',number:195,title:'La maison des âmes',
 book:{number:29},verses:[
  {number:1,text:'PSALM_ONLY_MARKER — Une œuvre et des êtres.'},
  {number:2,text:'Père, œuvrons dans la lumière.'}
 ],attachedPrayer:{number:86,text:'PRAYER_ONLY_MARKER — Ô Père, voici la paix.'}
};
function hasMarker(blobString,marker){return blobString.includes(Buffer.from(marker,'ascii').toString('hex').toUpperCase());}
for(const mode of ['psalm','prayer','both']){
 const spec=parts(fixture,mode);
 const output=createPDF(fixture,mode);
 const str=Buffer.from(await output.blob.arrayBuffer()).toString('latin1');
 assert.match(str,/^%PDF-1\.4/);
 assert.match(str,/startxref\n[0-9]+\n%%EOF/);
 assert.equal(output.blob.type,'application/pdf');
 assert.equal(output.filename.endsWith('.pdf'),true);
 assert.equal(hasMarker(str,'PSALM_ONLY_MARKER'),mode!=='prayer');
 assert.equal(hasMarker(str,'PRAYER_ONLY_MARKER'),mode!=='psalm');
 assert.ok(spec.blocks.length>0);
}
const prayer={recordType:'master-prayer',number:41,id:'p41',text:'PRAYER_ONLY_MARKER — Paix.'};
assert.equal(createPDF(prayer).pages,1);
const note={recordType:'note',id:'public-example',text:'Texte de note publique.'};
assert.equal(parts(note).filename.endsWith('.pdf'),true);
const veryLong={...fixture,verses:Array.from({length:150},(_,i)=>({number:i+1,text:'La lumière, les êtres et la vie se retrouvent dans la maison.'}))};
assert.ok(createPDF(veryLong,'psalm').pages>1,'Multipage psalm PDF required');
assert.throws(()=>parts(fixture,'invalid'),/Choix incorrect/);
assert.throws(()=>parts({...fixture,attachedPrayer:null},'prayer'),/Prière absente/);
console.log('PDF 077 PASS: independent Psalm/Prayer/both, French accents, standalone prayers, notes, multipage PDF');
