import {Actor} from 'apify';
import {memberApi} from './member-api.js';
import {deliverSounds} from './audio-delivery.js';
await Actor.main(async()=>{
 // Publisher-managed secret. Customers pay Apify per file; no second membership key in input.
 const api=memberApi({origin:process.env.MEMEFX_API_ORIGIN,key:process.env.MEMEFX_API_KEY});
 const charging=Actor.getChargingManager();
 const delivered=await deliverSounds({input:(await Actor.getInput())||{},api,storage:await Actor.openKeyValueStore(),pushData:(row,event)=>Actor.pushData(row,event),remaining:()=>charging.getPricingInfo().isPayPerEvent?charging.calculateMaxEventChargeCountWithinLimit('sound-delivered'):Infinity});
 await Actor.setStatusMessage(`Delivered ${delivered} WAV sound files. Download links are in the dataset.`);
});
