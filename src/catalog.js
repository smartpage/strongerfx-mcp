import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { z } from 'zod';

export const catalog = JSON.parse(readFileSync(new URL('../catalog/catalog.json', import.meta.url), 'utf8'));
export const inputSchema = z.object({
  query: z.string().max(300).default(''),
  category: z.enum(['all','interface','impacts','footsteps','glitches','notifications','transitions']).default('all'),
  ids: z.array(z.string().regex(/^[a-z0-9-]+$/)).max(50).default([]),
  maxDuration: z.number().positive().max(60).optional(),
  limit: z.number().int().min(1).max(50).default(10),
  format: z.enum(['wav','mp3']).default('wav')
}).strict();

export function searchSounds(raw={}) {
  const input=inputSchema.parse(raw);
  const terms=input.query.toLowerCase().match(/[a-z0-9]+/g)||[];
  const stop=new Set(['a','an','the','for','of','with','sound','sounds','effect','effects','me','find','give','short','some']);
  const useful=terms.filter(t=>!stop.has(t));
  const ids=new Set(input.ids);
  const missing=input.ids.filter(id=>!catalog.sounds.some(s=>s.id===id));
  if(missing.length) throw new Error(`Unknown sound IDs: ${missing.join(', ')}`);
  return catalog.sounds.filter(s=>(!ids.size||ids.has(s.id))&&(input.category==='all'||s.category===input.category)&&(!input.maxDuration||s.duration<=input.maxDuration))
    .map(s=>({sound:s,score:useful.reduce((n,t)=>n+(s.name.toLowerCase().includes(t)?4:0)+(s.tags.includes(t)?2:0)+(s.category.includes(t)?1:0),0)}))
    .filter(r=>!useful.length||r.score>0).sort((a,b)=>b.score-a.score||a.sound.id.localeCompare(b.sound.id)).slice(0,input.limit).map(r=>r.sound);
}

export function fileFor(sound, format='wav') {
  if(!['wav','mp3'].includes(format)) throw new Error('Unsupported format');
  return fileURLToPath(new URL(`../${sound.formats[format].path}`, import.meta.url));
}

export function publicResult(sound,format='wav') {
  return {...sound,downloadUrl:`https://raw.githubusercontent.com/smartpage/strongerfx-mcp/main/${sound.formats[format].path}`,previewUrl:`https://raw.githubusercontent.com/smartpage/strongerfx-mcp/main/${sound.formats.mp3.path}`,selectedFormat:format};
}
