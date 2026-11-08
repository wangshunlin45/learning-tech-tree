import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url),E=require('../src/engine.cjs');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2),skip=args.includes('--skip-validation'),pos=args.filter(x=>x!=='--skip-validation');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const safeJSON=data=>JSON.stringify(data).replaceAll('<','\\u003c').replaceAll('\u2028','\\u2028').replaceAll('\u2029','\\u2029');
function render(data,output){
 if(!skip){const errors=E.validateTree(data);if(errors.length)throw Error(errors.join('\n'));}
 const prefix=path.dirname(output)===root?'':'../';
 const catalog=[['','自定义科技树'],[prefix+'index.html','现代通信技术 · 学习科技树'],[prefix+'examples/computer-science-phd.html','计算机博士示例'],[prefix+'examples/minimal-template.html','最小自定义模板']].map(([value,label])=>`<option value="${escape(value)}"${(data.id==='comm-tech-2603'&&value===prefix+'index.html')||(data.id==='computer-science-phd'&&label==='计算机博士示例')||(data.id==='minimal-template'&&label==='最小自定义模板')?' selected':''}>${label}</option>`).join('');
 let html=read('src/template.html');
 const parts={'/*STYLE*/':read('src/style.css'),'/*CATALOG*/':catalog,'/*DATA*/':safeJSON(data),'/*ENGINE*/':read('src/engine.cjs'),'/*APP*/':read('src/app.js')};
 for(const [marker,value]of Object.entries(parts))html=html.replace(marker,()=>value);
 html=html.replace('<html lang="zh-CN">',`<html lang="${escape(data.language||'zh-CN')}">`);
 fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,html,'utf8');
 console.log(`Built ${path.relative(root,output)} (${data.nodes.length} nodes)`);
}
if(pos.length){
 if(pos.length!==2)throw Error('Usage: node scripts/build.mjs input.json output.html [--skip-validation]');
 render(JSON.parse(fs.readFileSync(path.resolve(pos[0]),'utf8')),path.resolve(pos[1]));
}else{
 const main=JSON.parse(read('data/comm-tech-tree.json')),cs=JSON.parse(read('data/computer-science-phd.json')),minimal=JSON.parse(read('data/minimal-template.json'));
 render(main,path.join(root,'index.html'));render(cs,path.join(root,'examples/computer-science-phd.html'));render(minimal,path.join(root,'examples/minimal-template.html'));
}
