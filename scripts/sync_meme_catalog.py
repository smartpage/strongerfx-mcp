"""Export the website's real cut metadata; never copy audio or infer licences."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root.parent / 'strongerfx-site/public/source-review/clips.json'
clips = json.loads(source.read_text())
sounds = []
for c in clips:
    sounds.append(dict(id=c['id'], name=c['name'], category=c['category'].lower(),
        duration=c['duration'], sampleRate=c['sampleRate'], channels=c['channels'],
        sourceUrl=c['source'], sourceId=c['sourceId'], part=c['part'],
        cut=dict(startFrame=round(c['start']*c['sampleRate']), endFrame=round(c['end']*c['sampleRate']),
                 start=c['start'], end=c['end'], boundaryStatus=c['boundaryStatus']),
        pcmSha256=c['pcmSha256'], identityStatus=c['identityStatus'],
        redistributionStatus=c['redistributionStatus'],
        audioDeliveryAvailable=False,
        waveform=c['peaks']))
(root/'catalog/memefx.json').write_text(json.dumps(dict(version='2.0.0',count=len(sounds),
    description='Curated reference catalog; no live trend measurements or audio delivery.',sounds=sounds),indent=2)+'\n')
print(f'Exported {len(sounds)} real sound records; no audio files copied.')
