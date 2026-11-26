import json,subprocess,os,shutil
tl=json.load(open('out/timeline.json'))
for s in tl['scenes']:
    if s['t']!='stock': continue
    i=s['i'];d=s['end']-s['start']+0.6;dd=f'out/stock/{i}';shutil.rmtree(dd,ignore_errors=True);os.makedirs(dd)
    src=f'out/stock_{i}.mp4'
    sd=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    speed=min(1.0,sd/d)
    vf=f"setpts={1/speed:.4f}*PTS,fps=25,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=saturation=0.85:contrast=1.06:brightness=-0.03,colorbalance=rs=.06:gs=.01:bs=-.06,vignette=PI/4.5"
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-t',str(d),'-vf',vf,'-q:v','3',f'{dd}/f_%05d.jpg'],check=True)
    s['nframes']=len(os.listdir(dd));print(i,s['nframes'])
json.dump(tl,open('out/timeline.json','w'),ensure_ascii=False)
