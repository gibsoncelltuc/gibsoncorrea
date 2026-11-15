// Renderiza frames.json + scene.glb (exportados do Blender) com Three.js headless (Chromium/SwiftShader). Uso: node three/render.js <pasta_export> <pasta_png> [w h env a b]
const {chromium}=require('playwright'); const fs=require('fs'), path=require('path'), http=require('http');
const [dir,out,W='540',H='960',env='golden',A='0',B='999999',AMB='2.6',SUN='3.2']=process.argv.slice(2); fs.mkdirSync(out,{recursive:true});
const root=path.resolve(__dirname,'..'); const srv=http.createServer((q,s)=>{let p=decodeURIComponent(q.url.split('?')[0]); let f=p.startsWith('/dir/')?path.join(path.resolve(dir),p.slice(5)):path.join(root,'three',p); if(!fs.existsSync(f)){s.writeHead(404);return s.end();} s.writeHead(200,{'Content-Type':f.endsWith('.js')||f.endsWith('.mjs')?'text/javascript':f.endsWith('.html')?'text/html':f.endsWith('.json')?'application/json':'application/octet-stream'}); fs.createReadStream(f).pipe(s);}).listen(0);
(async()=>{const port=srv.address().port; const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']}); const pg=await b.newPage({viewport:{width:+W,height:+H}});
 pg.on('console',m=>{const t=m.text(); if(/error|Error/.test(t)) console.log('console:',t.slice(0,200));}); pg.on('pageerror',e=>console.log('pageerror',String(e).slice(0,300)));
 await pg.goto(`http://localhost:${port}/viewer.html?dir=/dir&w=${W}&h=${H}&env=${env}&amb=${AMB}&sun=${SUN}`); await pg.waitForFunction('window.ready',null,{timeout:120000});
 const n=await pg.evaluate('window.nframes'); const t0=Date.now(); let k=0;
 for(let i=+A;i<Math.min(n,+B);i++){const d=await pg.evaluate(i=>window.renderFrame(i),i); fs.writeFileSync(path.join(out,`f${String(i).padStart(4,'0')}.png`),Buffer.from(d,'base64')); k++;}
 console.log('OK',k,'quadros em',((Date.now()-t0)/1000).toFixed(1),'s ->',((Date.now()-t0)/1000/Math.max(k,1)).toFixed(2),'s/quadro'); await b.close(); srv.close();})();
