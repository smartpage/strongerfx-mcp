#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { catalog, inputSchema, searchSounds, publicResult } from './catalog.js';

export function createServer() {
  const server=new McpServer({name:'strongerfx',version:'1.0.0'});
  const result=data=>({content:[{type:'text',text:JSON.stringify(data)}]});
  const annotations={readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false};
  server.registerTool('search_sound_effects',{description:'Search StrongerFX by sound, material, action or category. Returns preview/download URLs, duration, waveform, SHA-256 and CC0 provenance. No charge and no filesystem writes. English search terms.',inputSchema:inputSchema.shape,annotations},async input=>result({sounds:searchSounds(input).map(s=>publicResult(s,input.format))}));
  server.registerTool('get_sound_effect',{description:'Get a sound by exact catalogue ID with direct WAV or MP3 URL and licence.',inputSchema:{id:z.string().regex(/^[a-z0-9-]+$/),format:z.enum(['wav','mp3']).default('wav')},annotations},async({id,format})=>{const sound=catalog.sounds.find(s=>s.id===id);return sound?result(publicResult(sound,format)):{isError:true,content:[{type:'text',text:'Sound ID not found.'}]};});
  server.registerTool('list_sound_categories',{description:'List categories and sound counts in the StrongerFX CC0 library.',inputSchema:{},annotations},async()=>result({version:catalog.version,count:catalog.count,categories:[...new Set(catalog.sounds.map(s=>s.category))].map(category=>({category,count:catalog.sounds.filter(s=>s.category===category).length}))}));
  server.registerResource('catalog','strongerfx://catalog',{mimeType:'application/json',description:'Complete StrongerFX catalogue with attribution and checksums'},async uri=>({contents:[{uri:uri.href,mimeType:'application/json',text:JSON.stringify(catalog)}]}));
  return server;
}
if(process.argv[1] && import.meta.url===new URL(`file://${process.argv[1]}`).href) await createServer().connect(new StdioServerTransport());
