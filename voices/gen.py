import asyncio,json,os,sys,traceback
import edge_tts
async def one(text,v,out,retries=3):
    for a in range(retries):
        try:
            c=edge_tts.Communicate(text,v['voice'],rate=v['rate'],pitch=v['pitch'])
            await c.save(out)
            return os.path.getsize(out)>500
        except Exception as e:
            print('retry',a,out,repr(e)); await asyncio.sleep(2)
    return False
async def main():
    data=json.load(open('voices/lines.json',encoding='utf-8'))
    ok=bad=0
    for lang,chars in data.items():
        for cid,v in chars.items():
            for k,arr in v['lines'].items():
                for i,t in enumerate(arr):
                    out=f'voices/{lang}/{cid}/{k}_{i}.mp3'
                    os.makedirs(os.path.dirname(out),exist_ok=True)
                    if os.path.exists(out) and os.path.getsize(out)>500: ok+=1; continue
                    if await one(t,v,out): ok+=1
                    else: bad+=1; print('FAIL',out)
    print('done ok',ok,'bad',bad)
asyncio.run(main())
