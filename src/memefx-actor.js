import { Actor } from 'apify';
import { memeInput, searchMemes } from './meme-catalog.js';
await Actor.main(async()=>{
  const input=memeInput.parse((await Actor.getInput())||{});
  const sounds=searchMemes(input);
  let delivered=0;
  for(const sound of sounds) {
    const charge=await Actor.pushData(sound,'sound-result');
    if(charge.chargedCount>0 || !Actor.getChargingManager().getPricingInfo().isPayPerEvent) delivered++;
    if(charge.eventChargeLimitReached) break;
  }
  await Actor.setStatusMessage(`Returned ${delivered} sound reference records. Source links and cut metadata only; audio downloads are not included.`);
});
