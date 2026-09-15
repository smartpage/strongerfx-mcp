"""Sample-exact cuts of the downloaded Reels. No synthesis, gain or replacement audio.

Boundaries are selected inside measured low-level gaps, not rounded timestamps.
These exports are internal review assets, not a redistribution licence.
"""
import hashlib
import json
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'research/source-media'
OUT = ROOT / 'research/clip-review'

# Blind per-clip analysis disagreed with the first full-compilation analysis.
# Preserve the audio and stable filenames; do not promote either guess to fact.
DISPUTED_PART5 = {2, 3, 4, 8}

SETS = [
    ('Dcev_ZJpDfK', '',
     ['FAAH', 'CORE', 'CLICK', 'TACO BELL BONG', 'DISCORD NOTIFICATION', 'DING', 'WOOSH', 'CHA-CHING MONEY', 'MAGIC REVEAL', 'DEXTER MEME'],
     [0, 1.8355, 2.595, 2.848, 4.38985, 4.74265, 5.75782, 6.33455, 7.5964, 8.76263, 13.489342]),
    ('DcqbRPAR9v9', 'part5-',
     ['Whoosh', 'Pop', 'Camera shutter', 'Glass break', 'Chime', 'Cash register', 'Boing', 'Explosion'],
     [0, 1.58675, 2.62847, 3.24489, 4.38814, 5.60147, 6.68604, 7.06677, 8.938231]),
]


def export(source_id, prefix, names, boundaries):
    source_file = SOURCE / f'{source_id}.wav'
    with wave.open(str(source_file), 'rb') as recording:
        params = recording.getparams()
        source_bytes = recording.readframes(params.nframes)
    stride = params.nchannels * params.sampwidth
    manifest = []
    for index, name in enumerate(names):
        start = round(boundaries[index] * params.framerate)
        end = min(params.nframes, round(boundaries[index + 1] * params.framerate))
        filename = f'{prefix}{index + 1:02d}-{name.lower().replace(" ", "-")}.wav'
        pcm = source_bytes[start * stride:end * stride]
        destination = OUT / filename
        with wave.open(str(destination), 'wb') as output:
            output.setparams(params)
            output.writeframes(pcm)
        with wave.open(str(destination), 'rb') as check:
            assert check.readframes(check.getnframes()) == pcm, filename
        disputed = bool(prefix) and index + 1 in DISPUTED_PART5
        manifest.append({
            'name': f'Effect {index + 1:02d} — unidentified' if disputed else name,
            'start': start / params.framerate, 'end': end / params.framerate,
            'file': filename, 'sourceId': source_id,
            'source': f'https://www.instagram.com/p/{source_id}/',
            'startFrame': start, 'endFrame': end, 'sampleRate': params.framerate,
            'channels': params.nchannels, 'pcmSha256': hashlib.sha256(pcm).hexdigest(),
            'sourceSha256': hashlib.sha256(source_file.read_bytes()).hexdigest(),
            'boundaryStatus': 'revision 2: selected inside measured low-level gaps; perceptual verification pending',
            'identityStatus': 'conflicting machine descriptions; human identification required' if disputed else ('machine-suggested acoustic description; unverified identity' if prefix else 'label transcribed from reference video; identity not independently verified'),
            'redistributionStatus': 'unresolved', 'matchingMemeImage': None,
        })
    # Every sample from the source is preserved once across the full sequence.
    assert sum(m['endFrame'] - m['startFrame'] for m in manifest) == params.nframes
    return manifest


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    old = OUT / 'manifest.json'
    original = OUT / 'manifest-revision1.json'
    if old.exists() and not original.exists():
        original.write_bytes(old.read_bytes())
    primary, part5 = [export(*item) for item in SETS]
    (OUT / 'manifest.json').write_text(json.dumps(primary, indent=2) + '\n')
    (OUT / 'part5-manifest.json').write_text(json.dumps(part5, indent=2) + '\n')
    (OUT / 'all-clips.json').write_text(json.dumps(primary + part5, indent=2) + '\n')
    print(f'Exported {len(primary) + len(part5)} sample-exact WAV clips; byte equality and complete source coverage passed.')
