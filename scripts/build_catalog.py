"""Build a reproducible, provenance-preserving catalogue. Requires ffmpeg."""
import concurrent.futures, hashlib, json, math, random, re, shutil, struct, subprocess, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SR = 48000

def render_originals():
    target = ROOT / 'assets/source-original/Audio'
    target.mkdir(parents=True, exist_ok=True)
    for kind in ['whoosh', 'riser', 'subdrop', 'shimmer']:
        for variant in range(1, 7):
            rng = random.Random(variant * 7919 + sum(map(ord, kind)))
            duration = (0.45 + variant * .11) if kind == 'whoosh' else (0.9 + variant * .22)
            n = int(SR * duration)
            values, phase, smooth = [], 0., 0.
            for i in range(n):
                x, t = i/n, i/SR
                noise = rng.uniform(-1, 1)
                smooth = .91*smooth + .09*noise
                if kind == 'whoosh':
                    env = math.sin(math.pi*x)**(2+variant*.2)
                    value = (smooth * 2.2 + noise*.12) * env
                elif kind == 'riser':
                    freq = 110 * (1 + variant*.12) * (12**x)
                    phase += 2*math.pi*freq/SR
                    value = (.23*math.sin(phase) + .3*smooth) * x**1.8 * min(1, (1-x)*35)
                elif kind == 'subdrop':
                    freq = 38 + (170+variant*20) * math.exp(-7*x)
                    phase += 2*math.pi*freq/SR
                    value = math.sin(phase) * math.exp(-5*x) * min(1, x*150)
                else:
                    value = sum(math.sin(2*math.pi*f*t)*math.exp(-(2+j)*x) for j,f in enumerate([660+variant*55,990+variant*55,1320+variant*55])) / 3
                    value *= min(1, x*100) * min(1,(1-x)*30)
                values.append(value)
            peak = max(map(abs, values)) or 1
            with wave.open(str(target/f'{kind}_{variant:03}.wav'), 'wb') as out:
                out.setparams((1,2,SR,0,'NONE','not compressed'))
                out.writeframes(b''.join(struct.pack('<h',round(v/peak*26027)) for v in values))

def convert(spec):
    pack, file = spec
    ident = f'{pack}-{file.stem}'.replace('_','-')
    tokens = re.findall('[a-z]+', file.stem.lower())
    family = tokens[0]
    category = ('transitions' if family in ['whoosh','riser','subdrop','shimmer'] else
                'footsteps' if family=='footstep' else
                'impacts' if pack=='impact' else
                'glitches' if family in ['glitch','scratch','error'] else
                'notifications' if family in ['confirmation','bong','glass'] else 'interface')
    stem = ROOT/'audio'/ident
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(file),'-af','volume=0.85','-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(stem)+'.wav'],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(stem)+'.wav','-codec:a','libmp3lame','-b:a','192k',str(stem)+'.mp3'],check=True)
    with wave.open(str(stem)+'.wav','rb') as w:
        frames=w.readframes(w.getnframes()); duration=w.getnframes()/w.getframerate()
        samples=struct.unpack('<'+'h'*(len(frames)//2),frames)
        peak=max(map(abs,samples)) / 32768
        bins=[round(max(map(abs,samples[i:i+max(1,len(samples)//64)]),default=0)/32768,3) for i in range(0,len(samples),max(1,len(samples)//64))][:64]
    purposes={'interface':'UI button click tap app tutorial text reveal','impacts':'hit thud punch cut object foley','footsteps':'walk movement scene foley','glitches':'error glitch digital disruption transition','notifications':'success notification reveal confirm','transitions':'transition cinematic reveal whoosh motion sweep'}
    return {'id':ident,'name':file.stem.replace('_',' ').title(),'category':category,'tags':list(dict.fromkeys(tokens+purposes[category].split())), 'duration':round(duration,4),'sampleRate':SR,'channels':1,'bitDepth':16,'peakDbfs':round(20*math.log10(peak),2) if peak else -120,'waveform':bins,'formats':{fmt:{'path':f'audio/{ident}.{fmt}','bytes':Path(str(stem)+'.'+fmt).stat().st_size,'sha256':hashlib.sha256(Path(str(stem)+'.'+fmt).read_bytes()).hexdigest()} for fmt in ['wav','mp3']},'source':{'creator':'StrongerFX' if pack=='original' else 'Kenney','pack':pack,'url':'https://github.com/smartpage/strongerfx-mcp/blob/main/scripts/build_catalog.py' if pack=='original' else f'https://kenney.nl/assets/{pack}-sounds','originalFile':file.name,'license':'CC0-1.0','licenseUrl':'https://creativecommons.org/publicdomain/zero/1.0/'},'provenance':'Procedurally synthesized for StrongerFX; no third-party samples.' if pack=='original' else 'Kenney CC0 recording; converted to 48 kHz mono WAV and MP3. Not exclusive.'}

if __name__ == '__main__':
    render_originals()
    specs=[]
    for pack in ['interface','impact','original']:
        specs += [(pack,p) for p in sorted((ROOT/f'assets/source-{pack}/Audio').glob('*')) if p.suffix in ['.ogg','.wav']]
        license_file=ROOT/f'assets/source-{pack}/License.txt'
        if license_file.exists(): shutil.copyfile(license_file,ROOT/f'licenses/kenney-{pack}.txt')
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: sounds=list(ex.map(convert,specs))
    catalog={'version':'1.0.0','name':'StrongerFX Essentials','license':'CC0-1.0','count':len(sounds),'sounds':sounds}
    (ROOT/'catalog/catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    print(json.dumps({'count':len(sounds),'categories':{c:sum(s['category']==c for s in sounds) for c in sorted(set(s['category'] for s in sounds))}}))
