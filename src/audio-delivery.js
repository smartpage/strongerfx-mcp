import crypto from 'node:crypto';
import {z} from 'zod';
export const deliveryInput=z.object({query:z.string().max(300).default(''),ids:z.array(z.string().min(1).max(150)).max(50).optional(),maxDuration:z.number().positive().max(60).optional(),limit:z.number().int().min(1).max(50).default(10)});
export async function deliverSounds({input,api,storage,pushData,remaining=()=>Infinity}){
 const options=deliveryInput.parse(input);const library=await api.library();
 if(options.ids?.some(id=>!library.some(s=>s.id===id)))throw new Error('A requested sound is unavailable. No files were delivered.');
 const words=options.query.toLowerCase().split(/\s+/).filter(Boolean);
 const sounds=library.filter(s=>(!options.ids||options.ids.includes(s.id))&&words.every(w=>s.name.toLowerCase().includes(w))&&(!options.maxDuration||s.duration<=options.maxDuration)).slice(0,options.limit);
 let delivered=0;
 for(const sound of sounds){
  if(remaining()<1)break;
  const audio=await api.download(sound.id);
  const sha256=crypto.createHash('sha256').update(audio.bytes).digest('hex');
  const key=sha256+'.wav';
  await storage.setValue(key,audio.bytes,{contentType:'audio/wav'});
  const result=await pushData({id:sound.id,name:sound.name,duration:sound.duration,mimeType:'audio/wav',bytes:audio.bytes.length,sha256,downloadUrl:storage.getPublicUrl(key)},'sound-delivered');
  delivered++;if(result?.eventChargeLimitReached)break;
 }
 return delivered;
}
