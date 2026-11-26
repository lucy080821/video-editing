// node render.js out [workers] [from] [to]   -> out/part_k.mp4 ; or: node render.js out still t1,t2,... -> out/still_t.jpg
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');const path=require('path');
const OUT=process.argv[2];const mode=process.argv[3]||'4';
const TL=JSON.parse(fs.readFileSync(path.join(OUT,'timeline.json')));
const FPS=25;
async function page(b){const p=await b.newPage({viewport:{width:1920,height:1080}});await p.goto('file://'+path.resolve('stage.html'));await p.evaluate(tl=>window.boot(tl),TL);return p}
(async()=>{const b=await chromium.launch();
 if(mode==='still'){const p=await page(b);for(const t of process.argv[4].split(',').map(Number)){await p.evaluate(t=>window.seek(t),t);await p.screenshot({path:path.join(OUT,`still_${t}.jpg`),type:'jpeg',quality:80})}await b.close();return}
 const W=+mode;const total=Math.ceil(TL.total*FPS);const from=+(process.argv[4]||0),to=+(process.argv[5]||total);const per=Math.ceil((to-from)/W);
 await Promise.all([...Array(W).keys()].map(async k=>{const a=from+k*per,z=Math.min(to,a+per);if(a>=z)return;const p=await page(b);
  const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-c:v','mjpeg','-r',String(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',String(FPS),path.join(OUT,`part_${String(k).padStart(2,'0')}.mp4`)],{stdio:['pipe','inherit','inherit']});
  for(let f=a;f<z;f++){await p.evaluate(t=>window.seek(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:88});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(k===0&&f%250===0)console.log('frame',f,'/',z)}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await p.close()}));
 await b.close();console.log('done')})();
