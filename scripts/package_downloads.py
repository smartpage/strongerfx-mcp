import json, zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'catalog/catalog.json').read_text())
sampler=['original-whoosh-001','original-subdrop-002','original-shimmer-001','interface-click-001','interface-glitch-001']
def package(name,sounds):
    with zipfile.ZipFile(root/'dist'/name,'w',zipfile.ZIP_DEFLATED) as z:
        for sound in sounds:
            for fmt,meta in sound['formats'].items():
                z.write(root/meta['path'],f"{fmt.upper()}/{sound['category']}/{sound['id']}.{fmt}")
        z.writestr('sound-index.json',json.dumps({'sounds':sounds},indent=2))
        for path in (root/'licenses').glob('*.txt'): z.write(path,'LICENCES/'+path.name)
        z.writestr('START-HERE.txt','StrongerFX — Sound for the cut.\n\nImport WAV or MP3 files into your editor.\nWAV: mono, 48 kHz, PCM 16-bit. MP3: 192 kbps.\nAudio is CC0, including commercial use.\nKenney recordings are not exclusive; source details in sound-index.json.\nOriginal procedural transitions: StrongerFX.\nThese files are also free in our public repo. Paid packs cover convenience and packaging.\nhttps://github.com/smartpage/strongerfx-mcp\nContact: joao@intuitiva.pt\n')
    print(name,(root/'dist'/name).stat().st_size)
package('strongerfx-sampler.zip',[s for s in catalog['sounds'] if s['id'] in sampler])
package('strongerfx-essentials-vol-01.zip',catalog['sounds'])
