// Educational simulation only. Benchmark values are never generated here.
(()=>{
 const canvas=document.querySelector('#demo'),ctx=canvas.getContext('2d');
 const ids=['flux','sky','radius'];
 function rng(seed){return ()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed+.5)/4294967296}}
 function poisson(lambda,rand){ // Exact additive Poisson decomposition for larger means.
  let out=0;while(lambda>0){let l=Math.min(lambda,20),p=1,k=0;do{k++;p*=rand()}while(p>Math.exp(-l));out+=k-1;lambda-=l}return out;
 }
 function draw(){let [f,b,r]=ids.map(x=>+document.getElementById(x).value),rand=rng(4096),p=[],sum=0;
  for(let y=0;y<32;y++)for(let x=0;x<32;x++){let v=0;for(const dx of [-.25,.25])for(const dy of [-.25,.25])v+=Math.exp(-((x+dx-15.5)**2+(y+dy-15.5)**2)/(2*1.3**2));p.push(v);sum+=v}
  let measured=0,fraction=0,n=0;ctx.clearRect(0,0,320,320);
  p.forEach((v,i)=>{v/=sum;let y=Math.floor(i/32),x=i%32;let normal=Math.sqrt(-2*Math.log(rand()))*Math.cos(2*Math.PI*rand());let z=poisson(f*v+b,rand)+3*normal;
   let shade=Math.max(0,Math.min(255,(z-b+20)/100*255));ctx.fillStyle=`rgb(${shade*.75},${shade*.85},${shade})`;ctx.fillRect(x*10,y*10,10,10);
   if(Math.hypot(x-15.5,y-15.5)<r){measured+=z-b;fraction+=v;n++}
  });ctx.strokeStyle='#dc9345';ctx.lineWidth=2;ctx.beginPath();ctx.arc(160,160,r*10,0,Math.PI*2);ctx.stroke();
  document.querySelector('#demo-output').textContent=`Injected flux ${f} e− · sky ${b} e−/pixel · radius ${r} px · corrected aperture estimate ${(measured/fraction).toFixed(1)} e−. Known sky and known PSF are used in this demonstration.`;
 }
 ids.forEach(id=>document.getElementById(id).addEventListener('input',draw));draw();
})();
(()=>{
 const data=window.STELLAR_RESEARCH,canvas=document.querySelector('#fit-profile'),ctx=canvas.getContext('2d');
 function fit(){const row=+document.querySelector('#fit-row').value,a=data.image[row],b=data.fit[row],e=a.map((v,i)=>v-b[i]),lo=Math.min(0,...a,...b,...e),hi=Math.max(...a,...b,...e),scale=170/Math.max(hi-lo,1);
  ctx.clearRect(0,0,600,220);ctx.font='13px sans-serif';
  for(const [series,color] of [[a,'#386b85'],[b,'#d49343'],[e,'#9a6075']]){ctx.strokeStyle=color;ctx.beginPath();series.forEach((v,i)=>{const x=40+i*17,y=185-(v-lo)*scale;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()}
  ctx.fillStyle='#444';ctx.fillText('Pixel 0',35,207);ctx.fillText('Pixel 31',530,207);ctx.fillText(hi.toFixed(0)+' e−',0,20);ctx.fillText(lo.toFixed(0)+' e−',0,185);
  document.querySelector('#fit-description').textContent=`Object ${data.object_id}, row ${row}. Blue: observed; gold: fitted; purple: residual. Residual RMS across this row: ${Math.sqrt(e.reduce((s,v)=>s+v*v,0)/32).toFixed(2)} e−.`;
 }
 function metrics(){const name=document.querySelector('#metric-method').value,errors=data.first_ten.map(v=>v[name]-v.flux),mae=errors.reduce((s,v)=>s+Math.abs(v),0)/10,rmse=Math.sqrt(errors.reduce((s,v)=>s+v*v,0)/10),bias=errors.reduce((s,v)=>s+v,0)/10;
 document.querySelector('#metric-explanation').textContent=`Signed errors (e−): ${errors.map(v=>v.toFixed(1)).join(', ')}. Mean absolute error = ${mae.toFixed(2)} e−; root mean square error = ${rmse.toFixed(2)} e−; signed mean (bias) = ${bias.toFixed(2)} e−. These values use only the first ten objects.`;
 }
 function compare(){const metric=document.querySelector('#comparison-metric').value;document.querySelector('#comparison-values').textContent=Object.entries(data.summary).map(([k,v])=>`${k}: ${v[metric].toFixed(2)} e−`).join(' · ')+'. All 2,000 test objects.'}
 document.querySelector('#fit-row').addEventListener('input',fit);document.querySelector('#metric-method').addEventListener('change',metrics);document.querySelector('#comparison-metric').addEventListener('change',compare);fit();metrics();compare();
})();
