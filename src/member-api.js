export function memberApi({origin='https://strongerfx.intuitiva.app',key,fetcher=fetch}={}) {
 const base=new URL(origin);
 if(base.protocol!=='https:'||base.username||base.password||base.pathname!=='/'||base.search||base.hash)throw new Error('MEMEFX_API_ORIGIN must be an HTTPS origin.');
 if(!/^mfx_[a-f0-9]{64}$/.test(key||''))throw new Error('Set MEMEFX_API_KEY to your member API key.');
 async function request(path){const response=await fetcher(new URL(path,base),{headers:{Authorization:`Bearer ${key}`},redirect:'error',signal:AbortSignal.timeout(20000)});if(!response.ok)throw new Error(response.status===401?'Invalid or revoked MemeFX API key.':response.status===403?'An active MemeFX membership is required.':`MemeFX request failed (${response.status}).`);return response;}
 async function library(){const response=await request('/api/membership/library');const items=await response.json();if(!Array.isArray(items))throw new Error('Invalid library response.');return items;}
 async function download(id){const items=await library();const item=items.find(s=>s.id===id);if(!item)throw new Error('Sound not available in the member library.');const response=await request('/api/membership/download/'+encodeURIComponent(id));const reader=response.body.getReader();const chunks=[];let size=0;try{while(true){const {done,value}=await reader.read();if(done)break;size+=value.length;if(size>20*1024*1024)throw new Error('Sound exceeds the 20 MB per-file delivery limit.');chunks.push(Buffer.from(value));}}finally{await reader.cancel();}const bytes=Buffer.concat(chunks);if(bytes.toString('ascii',0,4)!=='RIFF'||bytes.toString('ascii',8,12)!=='WAVE')throw new Error('Server did not return WAV audio.');return {id:item.id,name:item.name,mimeType:'audio/wav',bytes};}
 return {library,download};
}
