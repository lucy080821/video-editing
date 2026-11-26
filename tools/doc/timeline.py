"""Build the final timeline (scene times with pauses, anchor times, word timings, SFX marks) and mix audio.
python3 timeline.py doc_script.json out
"""
import json, sys, subprocess, re, pathlib, numpy as np

sc = json.load(open(sys.argv[1], encoding='utf-8')); out = pathlib.Path(sys.argv[2])
al = json.load(open(out / 'alignment.json'))
chars, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
scenes = sc['scenes']; vos = [s['vo'] for s in scenes]
full = ' '.join(vos)
# map script char index -> alignment index (they should match; fall back to proportional)
same = ''.join(chars) == full
ratio = (len(chars) - 1) / max(1, len(full) - 1)
def ai(i): return i if same else min(len(chars) - 1, round(i * ratio))
def T0(i): return st[ai(i)]
def T1(i): return en[ai(i)]

LEAD = 0.6; PAUSE = 2.2; SR = 44100
starts = []; c = 0
for v in vos: starts.append(c); c += len(v) + 1
# boundaries in voice time (between scenes)
vb = [0.0]
for i in range(1, len(scenes)):
    a = T1(starts[i] - 2); b = T0(starts[i])
    vb.append((a + b) / 2)
voice_dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out / 'voice.mp3')]).decode())
vb.append(voice_dur)
pauses = []
for i, s in enumerate(scenes):
    p = 0.0
    if s['t'] in ('chapter', 'end') or s.get('pause_before'): p = float(s.get('pause_before', PAUSE))
    if i == 0: p = 0
    pauses.append(p)
# offset to add to voice time for scene i speech
off = []; o = LEAD
for i in range(len(scenes)): o += pauses[i]; off.append(o)
TAIL = 3.0
tl = []
for i, s in enumerate(scenes):
    vis0 = vb[i] + off[i] - pauses[i] if i else 0.0
    vis1 = vb[i + 1] + (off[i + 1] - pauses[i + 1] if i + 1 < len(scenes) else off[i] + TAIL)
    tl.append({'i': i, 't': s['t'], 'start': round(vis0, 3), 'end': round(vis1, 3), 'pause': pauses[i], 'speech': round(T0(starts[i]) + off[i], 3)})
total = tl[-1]['end']

def anchor(i, phrase):
    k = vos[i].find(phrase)
    if k < 0: raise SystemExit(f'anchor not found scene {i}: {phrase}')
    return round(T0(starts[i] + k) + off[i] - tl[i]['start'], 3)

def collect(o, i, acc):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if (k == 'at' or k.endswith('_at')) and isinstance(v, str):
                o[k] = anchor(i, v); acc.append((k, o[k]))
            else: collect(v, i, acc)
    elif isinstance(o, list):
        for x in o: collect(x, i, acc)

sfx = []
TR = ['whoosh', 'swipe', 'page', 'whoosh', 'shutter', 'swipe']
for i, s in enumerate(scenes):
    acc = []
    collect(s, i, acc)
    tl[i]['scene'] = {k: v for k, v in s.items() if k != 'vo'}
    t0 = tl[i]['start']
    if i:
        sfx.append((t0, 'riser' if s['t'] in ('chapter',) else TR[i % len(TR)], 0.55 if s['t'] != 'chapter' else 0.5))
    if s['t'] == 'chapter': sfx.append((t0 + 0.9, 'stamp', 0.45)); sfx.append((t0 + 1.4, 'marker', 0.5))
    if s['t'] == 'stat': sfx.append((t0 + 0.6, 'count', 0.35))
    kmap = {'stamp_at': 'stamp', 'wrong_at': 'buzz', 'right_at': 'ding', 'hl_at': 'marker', 'big_at': 'pop', 'check_at': 'ding', 'guess_at': 'scribble', 'clue_at': 'marker', 'timer_at': 'tick', 'chunk_at': 'ding', 'good_at': 'ding', 'bad_at': 'buzz', 'join_at': 'ding', 'text_at': 'marker', 'climb_at': 'pop'}
    last = -9
    for k, v in sorted(acc, key=lambda x: x[1]):
        t = t0 + v
        if t - last < 0.35: continue
        name = kmap.get(k, 'pop' if s['t'] not in ('steps', 'schedule', 'points', 'summary', 'rule') else 'tick')
        if s['t'] in ('points', 'summary', 'rule', 'steps') and k == 'at': name = 'tick' if s['t'] != 'steps' else 'pop'
        if s['t'] == 'study' and k == 'at': name = 'type'
        sfx.append((t, name, 0.38)); last = t

# word timings (final)
words = []
for i, v in enumerate(vos):
    for m in re.finditer(r'\S+', v):
        a = T0(starts[i] + m.start()) + off[i]; b = T1(starts[i] + m.end() - 1) + off[i]
        words.append({'w': m.group(), 's': round(a, 3), 'e': round(b, 3), 'i': i})
# cues: <= 44 chars, break on punctuation
cues, cur = [], []
for k, w in enumerate(words):
    cur.append(w); line = ' '.join(x['w'] for x in cur)
    nxt = words[k + 1] if k + 1 < len(words) else None
    if (not nxt or nxt['i'] != w['i'] or len(line) + 1 + len(nxt['w']) > 44 or (w['w'][-1] in '.?!:' and len(line) >= 10) or (w['w'][-1] in ',;' and len(line) >= 26)):
        cues.append(cur); cur = []
cl = []
for n, c in enumerate(cues):
    a = c[0]['s']; b = c[-1]['e'] + 0.25
    if n + 1 < len(cues): b = min(b, cues[n + 1][0]['s'] - 0.02)
    cl.append({'s': round(a, 3), 'e': round(max(b, a + 0.6), 3), 'w': [[x['w'], x['s'], x['e']] for x in c]})

def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s_:02d},{ms:03d}'
def srt(shift):
    return '\n'.join(f"{n+1}\n{ts(c['s']+shift)} --> {ts(c['e']+shift)}\n{' '.join(w[0] for w in c['w'])}\n" for n, c in enumerate(cl))
(out / 'subtitles_nointro.srt').write_text(srt(0), encoding='utf-8')
(out / 'subtitles.srt').write_text(srt(13.0), encoding='utf-8')
# chapters (with intro offset 13s)
def mmss(t): t = int(t); return f'{t//60}:{t%60:02d}'
ch = ['0:00 Intro kênh Tiếng Anh Không Khó', f'{mmss(13)} Học từ vựng tiếng Anh qua bài đọc: có nhớ lâu không?']
for i, s in enumerate(scenes):
    if s['t'] == 'chapter':
        title = s['title'] if not s.get('reward') else 'Phần thưởng: quy trình Đọc → Đoán → Kiểm tra → Ghi cụm → Ôn lại'
        ch.append(f"{mmss(tl[i]['start'] + 13)} {title.replace('“','').replace('”','')}")
(out / 'chapters.txt').write_text('\n'.join(ch) + '\n', encoding='utf-8')

json.dump({'total': round(total, 3), 'scenes': tl, 'cues': cl, 'sfx': [[round(a, 3), b, c] for a, b, c in sorted(sfx)], 'pauses': [p for p in pauses if p]}, open(out / 'timeline.json', 'w'), ensure_ascii=False)

# ---------- audio mix ----------
def load(p):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(p), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'])
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
N = int(total * SR) + SR
mix = np.zeros((N, 2), np.float32)
voice = load(out / 'voice.mp3')
for i in range(len(scenes)):
    a = int(vb[i] * SR); b = int(vb[i + 1] * SR); seg = voice[a:b]
    d = int((vb[i] + off[i]) * SR); mix[d:d + len(seg)] += seg[:max(0, N - d)]
# music with envelope: base .10, .30 during pauses (ramps 0.5s)
env = np.full(N, 0.10, np.float32)
t = np.arange(N) / SR
for i, p in enumerate(pauses):
    if not p: continue
    a = tl[i]['start']; b = a + p
    up = np.clip((t - a) / 0.5, 0, 1) * np.clip((b - t) / 0.5 + 0.0, 0, 1)
    env = np.maximum(env, 0.10 + 0.20 * np.clip(up, 0, 1))
fade = np.clip((total - t) / 3.0, 0, 1); env *= fade
env = np.minimum(env, np.clip(t / 1.0, 0, 1) * 0.3 + 0.0001)
mp = out / 'music.mp3'
if mp.exists():
    mu = load(mp)
    # crossfaded loop
    xf = int(2 * SR); reps = [mu]
    L = len(mu)
    while sum(len(r) for r in reps) - xf * (len(reps) - 1) < N: reps.append(mu)
    acc = reps[0].copy()
    for r in reps[1:]:
        w = np.linspace(0, 1, xf)[:, None]
        acc[-xf:] = acc[-xf:] * (1 - w) + r[:xf] * w
        acc = np.concatenate([acc, r[xf:]])
    mix += acc[:N] * env[:, None] * 1.2
for a, name, vol in sfx:
    f = pathlib.Path('sfx') / f'{name}.mp3'
    if not f.exists(): continue
    s_ = load(f); d = int(a * SR)
    s_ = s_[:max(0, N - d)]
    mix[d:d + len(s_)] += s_ * vol
peak = np.abs(mix).max(); mix *= min(1.0, 0.97 / max(peak, 1e-6))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'aac', '-b:a', '192k', str(out / 'mix.m4a')], input=mix.astype(np.float32).tobytes(), check=True)
print('total', total, 'pauses', len([p for p in pauses if p]), 'sfx', len(sfx), 'cues', len(cl))
