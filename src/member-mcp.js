#!/usr/bin/env node
import {pathToFileURL} from 'node:url';
import {McpServer} from '@modelcontextprotocol/sdk/server/mcp.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import {z} from 'zod';
import {memberApi} from './member-api.js';
export function createMemberServer(api){
 const server=new McpServer({name:'memefx-member',version:'2.0.0'});
 const annotations={readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:true};
 const result=data=>({content:[{type:'text',text:JSON.stringify(data)}]});
 server.registerTool('search_sounds',{description:'Search the available paid MemeFX sound library. Requires your member API key. Returns IDs and metadata; use download_sound to retrieve a WAV.',inputSchema:{query:z.string().max(300).default(''),limit:z.number().int().min(1).max(50).default(10)},annotations},async({query,limit})=>{const words=query.toLowerCase().split(/\s+/).filter(Boolean);const sounds=(await api.library()).filter(s=>words.every(w=>s.name.toLowerCase().includes(w))).slice(0,limit);return result({sounds:sounds.map(({id,name,duration})=>({id,name,duration}))});});
 server.registerTool('download_sound',{description:'Retrieve the actual WAV audio for an available member sound. Returns an embedded audio resource for your editor to save/import. No local filesystem writes. Maximum 20 MB per file; no monthly credit quota.',inputSchema:{id:z.string().min(1).max(150)},annotations},async({id})=>{const audio=await api.download(id);return {content:[{type:'text',text:JSON.stringify({id:audio.id,name:audio.name,mimeType:audio.mimeType,bytes:audio.bytes.length})},{type:'resource',resource:{uri:'memefx://audio/'+encodeURIComponent(id),mimeType:audio.mimeType,blob:audio.bytes.toString('base64')}}]};});
 return server;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await createMemberServer(memberApi({origin:process.env.MEMEFX_API_ORIGIN,key:process.env.MEMEFX_API_KEY})).connect(new StdioServerTransport());
