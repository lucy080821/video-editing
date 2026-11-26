"""Voice (ElevenLabs, chunked, with timestamps), music (ElevenLabs Music) and landscape b-roll (Pixabay) for a long documentary video.

python3 doc_media.py doc_script.json OUTDIR
Env: EL_KEY, PX_KEY. Voice and model are fixed for every video: voice ueSxRO0nLF1bj93J2hVt, model eleven_v3 (no fallback).
"""
import base64, json, os, pathlib, subprocess, sys, requests

sc = json.load(open(sys.argv[1], encoding='utf-8')); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
EL, PX = os.environ['EL_KEY'], os.environ['PX_KEY']
VOICE, MODEL = 'ueSxRO0nLF1bj93J2hVt', 'eleven_v3'  # fixed by anh Tuấn for all videos
H = {'xi-api-key': EL, 'Content-Type': 'application/json'}
vos = [s['vo'] for s in sc['scenes']]

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)]).decode().strip())

# 1) voice in chunks of whole scenes (<= ~1800 chars), merged alignment for the full text ' '.join(vos)
chunks, cur = [], []
for v in vos:
    if cur and len(' '.join(cur + [v])) > 1800: chunks.append(cur); cur = []
    cur.append(v)
chunks.append(cur)
import time
model = MODEL
chars, starts, ends, parts, offset = [], [], [], [], 0.0
for ci, ch in enumerate(chunks):
    text = ' '.join(ch)
    for m in [MODEL, MODEL, MODEL]:  # same model, up to 3 attempts
        body = {'text': text, 'model_id': m, 'output_format': 'mp3_44100_128'}
        if m == 'eleven_turbo_v2_5': body['language_code'] = 'vi'
        r = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps', headers=H, json=body, timeout=600)
        if r.ok: break
        print('voice chunk', ci, 'failed with', m, r.status_code, r.text[:200]); time.sleep(10)
    else:
        sys.exit('no voice')
    j = r.json(); al = j.get('alignment') or j.get('normalized_alignment')
    p = out / f'voice_{ci:02d}.mp3'; p.write_bytes(base64.b64decode(j['audio_base64'])); parts.append(p)
    if ci:  # the joining space between chunks
        chars.append(' '); starts.append(offset); ends.append(offset)
    chars += al['characters']; starts += [offset + x for x in al['character_start_times_seconds']]; ends += [offset + x for x in al['character_end_times_seconds']]
    offset += dur(p)
lst = out / 'voice_parts.txt'; lst.write_text(''.join(f"file '{p.name}'\n" for p in parts))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c:a', 'libmp3lame', '-b:a', '160k', str(out / 'voice.mp3')], check=True)
for p in parts: p.unlink()
lst.unlink()
full = ' '.join(vos)
if ''.join(chars) != full: print('warning: alignment text differs from script text; timing may drift')
json.dump({'characters': chars, 'character_start_times_seconds': starts, 'character_end_times_seconds': ends}, open(out / 'alignment.json', 'w'), ensure_ascii=False)
print('voice ok with', model, f'{offset:.1f}s in {len(chunks)} chunks')

# 2) music (instrumental, looped later if shorter than the video)
r = requests.post('https://api.elevenlabs.io/v1/music', headers=H, timeout=600,
                  json={'prompt': sc.get('music_prompt', 'calm cinematic documentary background music, soft piano and strings, no vocals'),
                        'music_length_ms': int(min(offset + 4, 240) * 1000), 'model_id': 'music_v1', 'force_instrumental': True})
if r.ok and len(r.content) > 20000:
    (out / 'music.mp3').write_bytes(r.content); print('music ok')
else:
    print('music failed', r.status_code, r.text[:200])

# 3) landscape b-roll, one distinct clip per stock scene
used, picks = set(), {}
for i, s in enumerate(sc['scenes']):
    if s['t'] != 'stock': continue
    hits = []
    for q in [s['query']] + s.get('alt', []):
        r = requests.get('https://pixabay.com/api/videos/', params={'key': PX, 'q': q, 'per_page': 30, 'safesearch': 'true'}, timeout=60)
        if r.ok: hits = [h for h in r.json().get('hits', []) if h['id'] not in used]
        if hits: break
    if not hits: print('no clip for', s['query']); continue
    def score(h):
        v = h['videos'].get('large') or h['videos'].get('medium') or {}
        return ((v.get('width') or 0) >= (v.get('height') or 1), (v.get('width') or 0) >= 1280, h.get('duration', 0) >= 6, h.get('likes', 0))
    hits.sort(key=score, reverse=True); h = hits[0]; used.add(h['id'])
    v = h['videos'].get('large') if (h['videos'].get('large') or {}).get('url') else h['videos'].get('medium')
    (out / f'stock_{i}.mp4').write_bytes(requests.get(v['url'], timeout=300).content)
    picks[i] = {'query': s['query'], 'page': h['pageURL'], 'id': h['id']}
    print('clip', i, s['query'], h['pageURL'])
json.dump(picks, open(out / 'stock.json', 'w'), ensure_ascii=False, indent=1)
