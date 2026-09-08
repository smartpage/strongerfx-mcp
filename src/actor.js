import { readFile } from 'node:fs/promises';
import { Actor } from 'apify';
import { inputSchema, searchSounds, fileFor, publicResult } from './catalog.js';

await Actor.main(async()=>{
  const input=inputSchema.parse((await Actor.getInput())||{});
  const sounds=searchSounds(input);
  let delivered=0;
  for(const sound of sounds) {
    // Read and validate delivery bytes before the SDK couples output to billing.
    const bytes=await readFile(fileFor(sound,input.format));
    const row={...publicResult(sound,input.format),audioBase64:bytes.toString('base64'),mimeType:input.format==='wav'?'audio/wav':'audio/mpeg'};
    const charge=await Actor.pushData(row,'sound-delivered');
    if(charge.chargedCount>0 || !Actor.getChargingManager().getPricingInfo().isPayPerEvent) delivered++;
    if(charge.eventChargeLimitReached) break;
  }
  await Actor.setStatusMessage(sounds.length?`Delivered ${delivered} sound effects. Download URLs and base64 audio are in the dataset.`:'No matching sounds. Try another category or fewer search words.');
});
