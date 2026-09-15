import { readFileSync } from 'node:fs';
import { z } from 'zod';
export const memeCatalog = JSON.parse(readFileSync(new URL('../catalog/memefx.json', import.meta.url), 'utf8'));
export const memeInput = z.object({
  query: z.string().max(300).default(''),
  category: z.enum(['all','memes','effects','alerts','transitions','music']).default('all'),
  ids: z.array(z.string().regex(/^[A-Za-z0-9_-]+$/)).max(50).default([]),
  maxDuration: z.number().positive().max(60).optional(),
  limit: z.number().int().min(1).max(50).default(10),
  includeWaveform: z.boolean().default(false)
}).strict();
export function memeResult(sound, includeWaveform=false) {
  const { waveform, ...metadata } = sound;
  return includeWaveform ? {...metadata,waveform} : metadata;
}
export function searchMemes(raw={}) {
  const input=memeInput.parse(raw);
  const missing=input.ids.filter(id=>!memeCatalog.sounds.some(s=>s.id===id));
  if(missing.length) throw new Error(`Unknown sound IDs: ${missing.join(', ')}`);
  const stop=new Set(['find','me','a','the','sound','sounds','effect','effects','for']);
  const terms=(input.query.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(t=>!stop.has(t));
  return memeCatalog.sounds.filter(s=>(!input.ids.length||input.ids.includes(s.id)) && (input.category==='all'||s.category===input.category) && (!input.maxDuration||s.duration<=input.maxDuration))
    .map(s=>({s,score:terms.reduce((n,t)=>n+(s.name.toLowerCase().includes(t)?4:0)+(s.category.includes(t)?1:0),0)}))
    .filter(r=>!terms.length||r.score>0).sort((a,b)=>b.score-a.score||a.s.id.localeCompare(b.s.id))
    .slice(0,input.limit).map(({s})=>memeResult(s,input.includeWaveform));
}
