import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { catalog, searchSounds, fileFor } from '../src/catalog.js';

test('all catalogue assets exist, are audible, have matching hashes and documented CC0 provenance',()=>{
  assert.equal(catalog.sounds.length,254);
  assert.equal(new Set(catalog.sounds.map(s=>s.id)).size,254);
  for(const s of catalog.sounds){
    assert.ok(s.duration>0 && s.duration<10);
    assert.ok(s.peakDbfs > -60 && s.peakDbfs < 0);
    assert.equal(s.source.license,'CC0-1.0');
    assert.ok(s.source.url.startsWith('https://'));
    for(const format of ['wav','mp3']){
      const bytes=readFileSync(fileFor(s,format));
      assert.equal(bytes.length,s.formats[format].bytes);
      assert.equal(createHash('sha256').update(bytes).digest('hex'),s.formats[format].sha256);
      if(format==='wav') assert.equal(bytes.subarray(0,4).toString(),'RIFF');
    }
  }
});
test('search ranks relevant sounds, obeys duration/category/limit and gives no fabricated matches',()=>{
  assert.ok(searchSounds({query:'whoosh',limit:3}).every(s=>s.id.includes('whoosh')));
  assert.ok(searchSounds({category:'footsteps',maxDuration:.5}).every(s=>s.category==='footsteps'&&s.duration<=.5));
  assert.equal(searchSounds({query:'unfindablexyz'}).length,0);
  assert.equal(searchSounds({ids:['original-whoosh-001']})[0].id,'original-whoosh-001');
  assert.throws(()=>searchSounds({ids:['not-real']}),/Unknown/);
  assert.throws(()=>searchSounds({limit:999}));
  assert.throws(()=>searchSounds({ids:['../../etc/passwd']}));
  assert.throws(()=>searchSounds({url:'http://localhost'}));
});
test('MCP stdio handshake, tool discovery, search and resource access work with a real client',async()=>{
  const client=new Client({name:'strongerfx-test',version:'1.0.0'});
  const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('../src/mcp.js',import.meta.url))]});
  try {
    await client.connect(transport);
    assert.equal((await client.listTools()).tools.length,3);
    const result=await client.callTool({name:'search_sound_effects',arguments:{query:'whoosh',limit:2}});
    assert.equal(JSON.parse(result.content[0].text).sounds.length,2);
    assert.equal(JSON.parse((await client.readResource({uri:'strongerfx://catalog'})).contents[0].text).count,254);
    assert.equal((await client.callTool({name:'get_sound_effect',arguments:{id:'missing'}})).isError,true);
  } finally { await client.close(); }
});
