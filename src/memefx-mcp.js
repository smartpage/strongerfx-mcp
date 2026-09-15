#!/usr/bin/env node
import { pathToFileURL } from 'node:url';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { memeCatalog, memeInput, memeResult, searchMemes } from './meme-catalog.js';
export function createMemeServer() {
  const server=new McpServer({name:'memefx',version:'2.0.0'});
  const result=data=>({content:[{type:'text',text:JSON.stringify(data)}]});
  const annotations={readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false};
  server.registerTool('search_meme_sounds',{description:'Find MemeFX reference sounds by name, category or duration. Returns source Reel links, exact cut timings and permission status. Optional waveform peaks. Does not deliver audio or measure current trends.',inputSchema:memeInput.shape,annotations},async input=>result({sounds:searchMemes(input)}));
  server.registerTool('get_meme_sound',{description:'Inspect one exact MemeFX sound ID, source, cut timings and waveform. No audio download is granted.',inputSchema:{id:z.string().regex(/^[A-Za-z0-9_-]+$/),includeWaveform:z.boolean().default(true)},annotations},async({id,includeWaveform})=>{
    const sound=memeCatalog.sounds.find(s=>s.id===id);
    return sound?result(memeResult(sound,includeWaveform)):{isError:true,content:[{type:'text',text:'Sound ID not found.'}]};
  });
  server.registerTool('list_meme_categories',{description:'List categories and counts in the curated MemeFX reference catalog.',inputSchema:{},annotations},async()=>result({count:memeCatalog.count,categories:[...new Set(memeCatalog.sounds.map(s=>s.category))].map(category=>({category,count:memeCatalog.sounds.filter(s=>s.category===category).length}))}));
  server.registerResource('catalog','memefx://catalog',{mimeType:'application/json',description:'MemeFX sound metadata; no audio files'},async uri=>({contents:[{uri:uri.href,mimeType:'application/json',text:JSON.stringify({...memeCatalog,sounds:memeCatalog.sounds.map(s=>memeResult(s))})}]}));
  return server;
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href) await createMemeServer().connect(new StdioServerTransport());
