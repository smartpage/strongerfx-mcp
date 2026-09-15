"""Build waveform-guided cuts and covers. Originals remain untouched.

Coarse boundaries follow source-video labels and inspected waveforms. Within
each region, remove low-level head/tail padding and apply a 1.5ms click guard.
No denoising, replacement, pitch change or loudness normalization is applied.
"""
import hashlib, html, json, shutil, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / 'research/source-media'
OUT = ROOT / 'research/clean-clips'
PUBLIC = ROOT.parent / 'strongerfx-site/public/source-review'
NEW = [
 ('DchpROhxiAc', 2, ['Dramatic fart','Rubber duck','Oh my God','Wow','Vine boom','SpongeBob disappointed','Cartoon running','Nerd emoji','Windows error','Metal pipe'],
  [0,1.089,1.6268,3.270,5.135,5.73,7.831,9.2863,10.936,11.63,13.280363]),
 ('Dcj8GnvpG73', 3, ['Ceeday huh','FAAH','Punch','Cha-ching money','Shocking','Rizz','Core','Vine boom','Bruh','Ding'],
  [0,.395,1.285,1.852,2.91,4.521,5.934,6.641,7.87,8.4437,9.4897]),
 ('DcmnBRjxKrU', 4, ['Shocking','Taco Bell bong','Drawer noise','Crickets','A few moments later','Boxing bell'],
  [0,1.3315,2.945,6.0697,7.92925,9.8755,11.469206]),
]

def read_audio(path):
 with wave.open(str(path),'rb') as w:
  rate=w.getframerate(); channels=w.getnchannels()
  assert w.getsampwidth()==2
  data=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,channels).copy()
 return rate,data

def category(name):
 n=name.lower()
 if any(x in n for x in ['faah','huh','bruh','god','wow','spongebob','nerd','moments','rizz']):return 'Memes'
 if any(x in n for x in ['ding','bell','notification','chime','windows']):return 'Alerts'
 if any(x in n for x in ['woosh','whoosh','magic','running']):return 'Transitions'
 if 'dexter' in n:return 'Music'
 return 'Effects'

def waveform_svg(peaks, number, duration, color):
 bars=''.join(f'<rect x="{36+i*4.1:.1f}" y="{218-v*120:.2f}" width="2.5" height="{max(1,v*240):.2f}" rx="1.2"/>' for i,v in enumerate(peaks))
 grid=''.join(f'<path d="M{x} 98V338"/>' for x in range(36,700,66))
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="440" viewBox="0 0 720 440">
 <rect width="720" height="440" fill="#141b25"/><g stroke="#ffffff" opacity=".055">{grid}<path d="M36 158H684M36 218H684M36 278H684"/></g>
 <g font-family="monospace" font-size="17" fill="#8e9aa9"><text x="36" y="49">MEMEFX / {number:03d}</text><text x="684" y="49" text-anchor="end" fill="{color}">WAVEFORM</text></g>
 <g fill="{color}">{bars}</g><path d="M36 360H684" stroke="#303945"/>
 <g font-family="monospace" font-size="17" fill="#8e9aa9"><text x="36" y="399">00:00</text><text x="684" y="399" text-anchor="end">{duration:.3f} SEC</text></g></svg>'''

def main():
 OUT.mkdir(exist_ok=True);PUBLIC.mkdir(exist_ok=True)
 original=json.loads((ROOT/'research/clip-review/all-clips.json').read_text())
 for m in original:m['part']=5 if m['sourceId']=='DcqbRPAR9v9' else 1
 for ident,part,names,bounds in NEW:
  for i,name in enumerate(names):original.append({'name':name,'sourceId':ident,'part':part,'start':bounds[i],'end':bounds[i+1], 'file':f'part{part}-{i+1:02d}.wav','identityStatus':'label read from source video; original provenance unverified','redistributionStatus':'unresolved'})
 sources={ident:read_audio(MEDIA/f'{ident}.wav') for ident in {m['sourceId'] for m in original}}
 results=[];audit=[]
 for index,m in enumerate(original):
  rate,full=sources[m['sourceId']];left=round(m['start']*rate);right=min(len(full),round(m['end']*rate))
  raw=full[left:right];amp=np.max(np.abs(raw.astype(np.float64)),axis=1)/32768
  # RMS avoids tiny codec spikes preventing an otherwise silent edge from trimming.
  block=max(1,round(.002*rate));pad=(-len(amp))%block
  rms=np.sqrt(np.mean(np.pad(amp**2,(0,pad)).reshape(-1,block),axis=1))
  threshold=max(.002,float(amp.max())*.008)
  active=np.flatnonzero(rms>threshold)
  above=np.array([int(active[0])*block,min(len(amp)-1,(int(active[-1])+1)*block-1)]) if len(active) else np.array([])
  if not len(above):raise ValueError(f'No signal: {m["name"]}')
  start=max(0,int(above[0])-round(.003*rate));end=min(len(raw),int(above[-1])+round(.008*rate)+1)
  # Choose low-magnitude endpoints in the padding only, preserving the attack.
  if start>0:
   lo=max(0,start-round(.001*rate));hi=min(int(above[0]),start+round(.001*rate))
   if hi>lo:start=lo+int(np.argmin(amp[lo:hi]))
  # Reviewed endpoint: the next effect starts around 1.30s in this source.
  # Silence detection alone cannot distinguish it from the intended sound.
  if m['sourceId']=='Dcev_ZJpDfK' and m['file']=='01-faah.wav':
   end=min(end,round((55247/44100)*rate)-left)
   if end<=start:raise ValueError('FAAH reviewed boundary precedes its attack')
  data=raw[start:end].astype(np.float64);fade=min(round(.0015*rate),len(data)//4)
  # FAAH has an audible residual tail at the source edit: give it a short release.
  tail_fade=min(round((.025 if m['name']=='FAAH' else .0015)*rate),len(data)//4)
  ramp=np.linspace(0,1,fade)
  data[:fade]*=ramp[:,None];data[-tail_fade:]*=np.linspace(1,0,tail_fade)[:,None]
  pcm=np.rint(data).astype('<i2');duration=len(pcm)/rate
  file=m['file'];path=OUT/file
  with wave.open(str(path),'wb') as w:w.setnchannels(full.shape[1]);w.setsampwidth(2);w.setframerate(rate);w.writeframes(pcm.tobytes())
  assert np.max(np.abs(pcm[0]))==0 and np.max(np.abs(pcm[-1]))==0
  assert np.array_equal(pcm[fade:-tail_fade],raw[start+fade:end-tail_fade])
  peak=max(1,float(np.max(np.abs(pcm.astype(float)))))
  peaks=[round(float(np.max(np.abs(b.astype(float))))/peak,5) for b in np.array_split(pcm,160)]
  cat=category(m['name']);color={'Memes':'#b7a4ff','Alerts':'#89c8ff','Transitions':'#72d7bf','Effects':'#d7e794','Music':'#ebaabf'}[cat]
  cover=Path(file).stem+'.svg';(OUT/cover).write_text(waveform_svg(peaks,index+1,duration,color))
  before=(right-left)/rate
  item={**m,'id':f'{m["sourceId"]}-{index+1}','name':m['name'].title() if m['name'].isupper() and m['name']!='FAAH' else m['name'],
   'start':(left+start)/rate,'end':(left+end)/rate,'startFrame':left+start,'endFrame':left+end,'duration':duration,'originalStart':left/rate,'originalEnd':right/rate,
   'image':cover,'category':cat,'color':color,'peaks':peaks,'sampleRate':rate,'channels':full.shape[1],
   'trimmedHeadMs':round(start/rate*1000,2),'trimmedTailMs':round((len(raw)-end)/rate*1000,2),'edgeFadeMs':1.5,'tailFadeMs':round(tail_fade/rate*1000,3),
   'pcmSha256':hashlib.sha256(pcm.tobytes()).hexdigest(),'boundaryStatus':f'waveform-trimmed; 1.5ms attack fade; {tail_fade/rate*1000:.1f}ms release; source-limited tails',
   'sourceFile':f'sources/{m["sourceId"]}.wav','source':f'https://www.instagram.com/p/{m["sourceId"]}/'}
  results.append(item);audit.append((m,amp,start,end,rate))
  for asset in [path,OUT/cover]:shutil.copy2(asset,PUBLIC/asset.name)
  print(f'{index+1:02} {m["name"]:28} {before:.3f}s -> {duration:.3f}s | removed {item["trimmedHeadMs"]:6.1f}/{item["trimmedTailMs"]:6.1f}ms')
 (PUBLIC/'sources').mkdir(exist_ok=True)
 for ident in sources:shutil.copy2(MEDIA/f'{ident}.wav',PUBLIC/'sources'/f'{ident}.wav')
 for path in [OUT/'manifest.json',PUBLIC/'clips.json']:path.write_text(json.dumps(results,indent=2)+'\n')
 font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
 for page in range(0,len(audit),8):
  im=Image.new('RGB',(1600,8*180),'#10151b');d=ImageDraw.Draw(im)
  for row,(m,amp,start,end,rate) in enumerate(audit[page:page+8]):
   y=row*180;d.text((28,y+10),f'{page+row+1:02} {m["name"]} — source {m["start"]:.3f}–{m["end"]:.3f}s',font=font,fill='white')
   for x,b in enumerate(np.array_split(amp,1500)):
    h=float(b.max())*58;frame=x/1500*len(amp);color='#718094' if frame<start or frame>=end else '#a7dc83'
    d.line((40+x,y+100-h,40+x,y+100+h),fill=color)
   for at in [start,end]:
    x=40+at/len(amp)*1500;d.line((x,y+35,x,y+165),fill='#ffb45e',width=2)
  im.save(ROOT/f'research/waveform-audit/cuts-{page//8+1}.png')
 print(f'Built {len(results)} cleaned files and unique waveform covers; original samples unchanged outside 1.5ms edge guards.')

if __name__=='__main__':main()
