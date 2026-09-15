from PIL import Image, ImageDraw, ImageFont
import wave, struct, math, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUDIO=ROOT.parents[2]/'strongerfx-site/member-assets/original-subdrop-001.wav'
# Resolve sibling site from project root.
AUDIO=ROOT.parents[2]/'strongerfx-site/member-assets/original-subdrop-001.wav'
W,H,FPS,DURATION=1080,1920,30,12
CREAM='#F4F0E9'; PURPLE='#7039EF'; INK='#25212B'; MUTED='#736D7B'; CARD='#26212E'
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
regular='/System/Library/Fonts/Supplemental/Arial.ttf'
def f(size,bold=True): return ImageFont.truetype(font if bold else regular,size)
with wave.open(str(AUDIO)) as w:
    rate=w.getframerate(); values=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
length=len(values)/rate
peaks=[]
for i in range(82):
    part=values[int(i*len(values)/82):int((i+1)*len(values)/82)]
    peaks.append(max(abs(v) for v in part)/32768)

def center(d,text,y,size,color=INK):
    ft=f(size); box=d.textbbox((0,0),text,font=ft); d.text(((W-(box[2]-box[0]))/2,y),text,font=ft,fill=color)
def frame(t):
    im=Image.new('RGB',(W,H),CREAM); d=ImageDraw.Draw(im)
    d.rounded_rectangle((72,128,289,197),radius=34,fill=PURPLE)
    d.text((100,141),'MemeFX',font=f(37),fill='white')
    d.text((748,151),'FREE EFFECT',font=f(23),fill=PURPLE)
    outro=t>=8.0
    if not outro:
        center(d,'YOUR EDIT',300,104)
        center(d,'NEEDS A DROP.',414,104,PURPLE)
        center(d,'Press play energy. Zero price.',560,35,MUTED)
    else:
        center(d,'GET THIS',300,108)
        center(d,'EFFECT FREE.',422,108,PURPLE)
        center(d,'One original sound. Yours to download.',565,33,MUTED)
    # Square player card / original vector design.
    active=next((t-start for start in (2.0,5.6) if 0<=t-start<length),None)
    pulse=0 if active is None else max(0,1-active/length)
    d.rounded_rectangle((74,691,1006,1373),radius=48,fill=CARD)
    d.text((125,744),'01 / ORIGINAL BASS DROP',font=f(29),fill='#D8C8FF')
    d.text((125,801),'Make the punchline land.',font=f(41),fill=CREAM)
    for i,p in enumerate(peaks):
        x=128+i*10
        amp=18+(p**.55)*202
        heard=active is not None and i/82<=active/length
        col='#BDA0FF' if heard else '#71647F'
        d.rounded_rectangle((x,1090-amp/2,x+5,1090+amp/2),radius=3,fill=col)
    d.ellipse((126,1230,210,1314),fill=PURPLE)
    if active is None: d.polygon([(160,1251),(160,1293),(187,1272)],fill='white')
    else:
        d.rectangle((155,1253,164,1291),fill='white'); d.rectangle((176,1253,185,1291),fill='white')
    d.text((235,1254),'BASS DROP 001',font=f(29),fill=CREAM)
    d.text((844,1257),f'{length:.1f}s',font=f(28,False),fill='#A79BAF')
    if outro:
        d.rounded_rectangle((104,1470,976,1594),radius=62,fill=PURPLE)
        center(d,'Comment SOUNDFX',1503,54,'white')
        center(d,'No card. Just your next edit.',1650,34,MUTED)
    else:
        label='SOUND ON' if t<2 else ('HEAR THAT AGAIN.' if t>=4.1 else 'THAT’S THE DROP.')
        center(d,label,1472,44,PURPLE)
        center(d,'An original effect for your next short.',1572,34,MUTED)
    d.rounded_rectangle((440,1795,640,1801),radius=3,fill='#D5CDDF')
    return im

video=ROOT/'free-bass-drop-reel-silent.mp4'
p=subprocess.Popen(['/opt/homebrew/bin/ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
for n in range(FPS*DURATION): p.stdin.write(frame(n/FPS).tobytes())
p.stdin.close()
if p.wait(): raise RuntimeError('Video encode failed')
frame(9).save(ROOT/'preview.jpg',quality=95)
subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-loglevel','error','-i',str(video),'-i',str(AUDIO),'-filter_complex','[1:a]asplit=2[a][b];[a]adelay=2000:all=1[a1];[b]adelay=5600:all=1[b1];[a1][b1]amix=inputs=2:normalize=0,apad=whole_dur=12[out]','-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','192k','-t','12','-movflags','+faststart',str(ROOT/'free-bass-drop-reel.mp4')],check=True)
video.unlink()
(ROOT/'caption.txt').write_text('Your edit needs a drop. 🔊\n\nHear it. Download it. Drop it into your next Reel, TikTok or Short.\n\nThis is our ORIGINAL BASS DROP 001 — one free effect, ready for your next edit.\n\nComment SOUNDFX and we’ll DM you the free download page. Create your free account to download. No card needed.\n\n#soundfx #soundeffects #videoediting #reelsediting #memefx\n')
print(ROOT/'free-bass-drop-reel.mp4')
