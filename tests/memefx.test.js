import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { memeCatalog, searchMemes } from '../src/meme-catalog.js';
test('real reference search filters accurately and exposes no audio delivery',()=>{
  assert.equal(memeCatalog.count,44);
  const sounds=searchMemes({query:'vine boom',maxDuration:2,includeWaveform:true});
  assert.ok(sounds.length>0);
  for(const s of sounds){assert.equal(s.name,'Vine boom');assert.ok(s.waveform.length>0);assert.equal(s.audioDeliveryAvailable,false);assert.equal(s.downloadUrl,undefined);assert.equal(s.redistributionStatus,'unresolved');assert.ok(Math.abs((s.cut.endFrame-s.cut.startFrame)/s.sampleRate-s.duration)<.001);}
  assert.equal(searchMemes({query:'nonesuch123'}).length,0);
  for(const category of new Set(memeCatalog.sounds.map(s=>s.category))) assert.ok(searchMemes({category}).length>0);
  assert.throws(()=>searchMemes({ids:['missing']}));
  assert.throws(()=>searchMemes({limit:51}));
  assert.throws(()=>searchMemes({url:'http://localhost'}));
  assert.equal(searchMemes({limit:1})[0].waveform,undefined);
});
test('MemeFX MCP negotiates tools and returns real FAAH references',async()=>{
  const client=new Client({name:'memefx-test',version:'1.0.0'});
  try {
    await client.connect(new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('../src/memefx-mcp.js',import.meta.url))]}));
    assert.equal((await client.listTools()).tools.length,3);
    const result=await client.callTool({name:'search_meme_sounds',arguments:{query:'FAAH'}});
    assert.equal(JSON.parse(result.content[0].text).sounds.length,2);
    assert.equal(JSON.parse((await client.readResource({uri:'memefx://catalog'})).contents[0].text).count,44);
    assert.equal((await client.callTool({name:'get_meme_sound',arguments:{id:'missing'}})).isError,true);
  } finally {await client.close();}
});
