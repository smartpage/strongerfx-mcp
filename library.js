const $=s=>document.querySelector(s);
$('#cover').src='https://storage.googleapis.com/intuitiva-client-dashboard-fb.firebasestorage.app/organizations/org_intuitiva/sites/site_strongerfx/images/strongerfx-cover-1788884094612.webp';
const audio=new Audio();audio.preload='none';audio.volume=.65;
let sounds=[],category=new URLSearchParams(location.search).get('category')||'all',visible=24,current=null;
const categories=['all','transitions','interface','impacts','glitches','notifications','footsteps'];
if(!categories.includes(category))category='all';
function stop(){audio.pause();audio.currentTime=0;current=null;$('#player').hidden=true;document.querySelectorAll('.play').forEach(b=>{b.textContent='▶';b.setAttribute('aria-pressed','false')});}
async function play(sound){if(current===sound.id){stop();return;}stop();current=sound.id;audio.src='/'+sound.formats.mp3.path;$('#playing').textContent=sound.name;$('#player').hidden=false;$('#progress').value=0;$('#time').textContent='0.0s';const button=document.getElementById('play-'+sound.id);button.textContent='■';button.setAttribute('aria-pressed','true');try{await audio.play()}catch{stop();$('#count').textContent='Preview unavailable. Try the WAV or MP3 download.'}}
audio.addEventListener('ended',stop);audio.addEventListener('timeupdate',()=>{if(audio.duration){$('#progress').value=audio.currentTime/audio.duration;$('#time').textContent=audio.currentTime.toFixed(1)+'s'}});$('#stop').onclick=stop;
function render(){
  const terms=$('#search').value.toLowerCase().trim().split(/\s+/).filter(Boolean),max=Number($('#duration').value);
  const filtered=sounds.filter(s=>(category==='all'||s.category===category)&&s.duration<=max&&terms.every(t=>[s.name,...s.tags].join(' ').toLowerCase().includes(t)));
  $('#count').textContent=`${filtered.length} SOUND${filtered.length===1?'':'S'}${category==='all'?'':' / '+category.toUpperCase()}`;
  $('#sounds').replaceChildren();
  for(const s of filtered.slice(0,visible)){
    const row=document.createElement('article');row.className='sound';
    const button=document.createElement('button');button.className='play';button.id='play-'+s.id;button.type='button';button.textContent=current===s.id?'■':'▶';button.setAttribute('aria-pressed',String(current===s.id));button.setAttribute('aria-label','Preview '+s.name);button.onclick=()=>play(s);
    const title=document.createElement('div'),h=document.createElement('h3'),p=document.createElement('p');h.textContent=s.name;p.textContent=s.category+' / '+s.source.creator;title.append(h,p);
    const waveform=document.createElement('div');waveform.className='wave';waveform.setAttribute('aria-hidden','true');s.waveform.forEach(v=>{const bar=document.createElement('i');bar.style.height=Math.max(2,v*32)+'px';waveform.append(bar)});
    const duration=document.createElement('span');duration.className='seconds';duration.textContent=s.duration.toFixed(2)+'s';
    const downloads=document.createElement('div');downloads.className='downloads';for(const fmt of ['wav','mp3']){const link=document.createElement('a');link.href='/'+s.formats[fmt].path;link.download=s.id+'.'+fmt;link.textContent=fmt.toUpperCase()+' ↓';link.setAttribute('aria-label','Download '+s.name+' as '+fmt.toUpperCase());downloads.append(link)}
    row.append(button,title,waveform,duration,downloads);$('#sounds').append(row);
  }
  if(!filtered.length){const empty=document.createElement('p');empty.className='empty';empty.textContent='No matches. Try a shorter search or another category.';$('#sounds').append(empty)}
  $('#more').hidden=filtered.length<=visible;
  document.querySelectorAll('#filters button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category===category)));
}
for(const name of categories){const b=document.createElement('button');b.type='button';b.textContent=name==='all'?'All sounds':name[0].toUpperCase()+name.slice(1);b.dataset.category=name;b.onclick=()=>{category=name;visible=24;render()};$('#filters').append(b)}
$('#search').addEventListener('input',()=>{visible=24;render()});$('#duration').onchange=()=>{visible=24;render()};$('#more').onclick=()=>{visible+=24;render()};
try{const response=await fetch('/catalog/catalog.json');if(!response.ok)throw Error();sounds=(await response.json()).sounds;render()}catch{$('#count').textContent='Catalogue unavailable. Please refresh or use the GitHub link below.'}
