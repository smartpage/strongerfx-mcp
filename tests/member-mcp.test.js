import test from 'node:test';
import assert from 'node:assert/strict';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { InMemoryTransport } from '@modelcontextprotocol/sdk/inMemory.js';
import { createMemberServer } from '../src/member-mcp.js';

test('member MCP negotiates tools, searches and delivers exact WAV bytes', async()=>{
 const wav=Buffer.from('RIFF0000WAVEfixture');
 const server=createMemberServer({library:async()=>[{id:'boom',name:'Vine boom',duration:.8},{id:'bell',name:'Bell',duration:1}],download:async id=>({id,name:'Vine boom',mimeType:'audio/wav',bytes:wav})});
 const client=new Client({name:'integration-test',version:'1.0.0'});
 const [clientTransport,serverTransport]=InMemoryTransport.createLinkedPair();
 try {
  await server.connect(serverTransport);await client.connect(clientTransport);
  const tools=await client.listTools();assert.deepEqual(tools.tools.map(t=>t.name).sort(),['download_sound','search_sounds']);
  const results=await client.callTool({name:'search_sounds',arguments:{query:'VINE boom',limit:1}});
  assert.equal(results.isError,undefined);assert.deepEqual(JSON.parse(results.content[0].text).sounds,[{id:'boom',name:'Vine boom',duration:.8}]);
  const audio=await client.callTool({name:'download_sound',arguments:{id:'boom'}});
  assert.equal(audio.content[1].resource.mimeType,'audio/wav');assert.deepEqual(Buffer.from(audio.content[1].resource.blob,'base64'),wav);
  const invalid=await client.callTool({name:'search_sounds',arguments:{limit:51}});assert.equal(invalid.isError,true);
 } finally {await client.close();await server.close();}
});

test('member MCP reports access failure instead of returning audio',async()=>{
 const server=createMemberServer({library:async()=>{throw new Error('An active paid membership is required.');},download:async()=>{throw new Error('Invalid or revoked API key.');}});
 const client=new Client({name:'denied-test',version:'1.0.0'});const [a,b]=InMemoryTransport.createLinkedPair();
 try{await server.connect(b);await client.connect(a);const result=await client.callTool({name:'download_sound',arguments:{id:'boom'}});assert.equal(result.isError,true);assert.match(result.content[0].text,/revoked/);assert.equal(result.content.some(c=>c.type==='resource'),false);}finally{await client.close();await server.close();}
});
