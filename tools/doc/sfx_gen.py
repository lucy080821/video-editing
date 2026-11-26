import os,requests,pathlib,sys
H={'xi-api-key':os.environ['EL_KEY'],'Content-Type':'application/json'}
S={
 'whoosh':('fast soft air whoosh transition, clean, no music',0.8),
 'swipe':('quick paper swipe slide sound',0.6),
 'pop':('small soft bubble pop click for UI element appearing',0.5),
 'marker':('felt tip highlighter marker stroke on paper, short squeak',0.9),
 'scribble':('pen quickly scribbling circle on paper',0.9),
 'ding':('bright short positive ding chime, correct answer',0.8),
 'buzz':('short soft wrong answer buzzer',0.6),
 'tick':('single clean clock tick click',0.5),
 'page':('book page turning, single page flip',0.9),
 'stamp':('rubber stamp thud on paper desk',0.6),
 'type':('short burst of typewriter keys typing',0.9),
 'riser':('short soft cinematic riser swell into hit',1.6),
 'count':('quick digital counter ticking up numbers',1.0),
 'shutter':('soft camera shutter click',0.5),
}
for k,(p,d) in S.items():
    f=pathlib.Path('sfx')/f'{k}.mp3'
    if f.exists(): continue
    r=requests.post('https://api.elevenlabs.io/v1/sound-generation',headers=H,json={'text':p,'duration_seconds':d,'prompt_influence':0.6},timeout=120)
    if r.ok and len(r.content)>2000: f.write_bytes(r.content); print('ok',k)
    else: print('fail',k,r.status_code,r.text[:150])
