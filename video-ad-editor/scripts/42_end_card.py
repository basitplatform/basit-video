# -*- coding: utf-8 -*-
"""كرت ختام منصة بسيط بآخر أي فيديو (مونتاج · حلقة بالعرض · فيلم موشن) — نفس كرت الريل: الشعار + الدعوة + الكلمة + الموقع.
  python3 scripts/42_end_card.py <in.mp4> <out.mp4> [--work <مجلد فيه theme.json>] [--dur 3.5]
         [--l1 "سطر فوق"] [--l2 "سطر ثاني"] [--cta "اكتب بالتعليقات"] [--word "دورات"] [--sub "basit.tv"]
  - النصوص والألوان والخط والشعار من theme.json ← outro (00_brand.py يكتبها)، وإلا من brand/basit/brand.json.
  - المقاس من الفيديو نفسه (طولي أو عرضي)، والكرت يدخل بتلاشي ناعم، والصوت يخلص بهدوء."""
import sys as _sys_u8   # ويندوز: الطباعة بالعربي بـUTF-8
try: _sys_u8.stdout.reconfigure(encoding="utf-8", errors="replace"); _sys_u8.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
import html, json, os, pathlib, shutil, subprocess, sys, tempfile

SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
if len(args) < 2: sys.exit(__doc__)
SRC, OUT = os.path.abspath(args[0]), os.path.abspath(args[1])
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
DUR = float(opt("--dur", 3.5))


def die(m): print("⛔ " + m); sys.exit(1)


if not os.path.exists(SRC): die(f"ما لكيت {SRC}")
# 1) الهوية والنصوص
B = json.load(open(os.path.join(SK, "brand", "basit", "brand.json"), encoding="utf-8"))
th, base = {}, os.path.join(SK, "brand", "basit")
if opt("--work") and os.path.exists(os.path.join(opt("--work"), "theme.json")):
    th = json.load(open(os.path.join(opt("--work"), "theme.json"), encoding="utf-8")); base = os.path.abspath(opt("--work"))
C = B["colors"]
bg = th.get("bg") or C[B["theme"]["bg"]]; ink = th.get("ink") or C[B["theme"]["ink"]]; acc = th.get("acc") or C[B["theme"]["acc"]]
mut = th.get("mut") or C[B["theme"]["mut"]]; on = th.get("onAcc") or "#111111"
o = dict(B.get("outro") or {}); o.update(th.get("outro") or {} if isinstance(th.get("outro"), dict) else {})
for k in ("l1", "l2", "cta", "word", "sub"):
    if opt("--" + k) is not None: o[k] = opt("--" + k)
fam = th.get("font") or B["font"]["family"]
if th.get("fontFiles"):
    files = [(os.path.join(base, f["src"]), f.get("weight", 400)) for f in th["fontFiles"]]
else:
    files = [(os.path.join(SK, "brand", "basit", "fonts", f["file"]), f["weight"]) for f in B["font"]["files"]]
logo = os.path.join(base, th["logo"]) if th.get("logo") else os.path.join(SK, "brand", "basit", B["logo"]["onDark"])

# 2) مقاس الفيديو
pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                     "-of", "json", SRC], capture_output=True, text=True)
st = json.loads(pr.stdout)["streams"][0]; Wd, Ht = int(st["width"]), int(st["height"])
num, den = (st.get("r_frame_rate") or "30/1").split("/"); FPS = round(float(num) / float(den or 1), 3) or 30
wide = Wd > Ht; u = (Ht if wide else Wd) / 1080   # وحدة القياس

# 3) الكرت (HTML ← صورة بكروم بلا واجهة)
uri = lambda p: pathlib.Path(p).resolve().as_uri()
faces = "".join(f"@font-face{{font-family:'{fam}';src:url('{uri(p)}');font-weight:{w}}}" for p, w in files if os.path.exists(p))
e = lambda k: html.escape(str(o.get(k) or ""))
page = f"""<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>{faces}
*{{margin:0;box-sizing:border-box}} html,body{{width:{Wd}px;height:{Ht}px;overflow:hidden;background:{bg};font-family:'{fam}',sans-serif}}
.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{int(34*u)}px;text-align:center;color:{ink}}}
.lg{{width:{int(300*u)}px}} .s{{font-weight:500;font-size:{int(44*u)}px;color:{mut};line-height:1.45}}
.cta{{font-weight:900;font-size:{int(92*u)}px;margin-top:{int(30*u)}px}}
.w{{font-weight:900;font-size:{int(100*u)}px;background:{acc};color:{on};padding:{int(6*u)}px {int(56*u)}px {int(20*u)}px;border-radius:{int(40*u)}px}}
.sub{{font-weight:700;font-size:{int(42*u)}px;color:{ink};opacity:.85;direction:ltr}}
</style></head><body><div class="c"><img class="lg" src="{uri(logo)}">
<div class="s">{e('l1')}<br>{e('l2')}</div><div class="cta">{e('cta')}</div>{f'<div class="w">{e("word")}</div>' if o.get('word') else ''}
<div class="sub">{e('sub')}</div></div></body></html>"""
tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, "card.html"); png = os.path.join(tmp, "card.png")
open(hp, "w", encoding="utf-8").write(page)
chrome = os.environ.get("CHROME") or next((c for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
          os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"), r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
          "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", shutil.which("google-chrome") or "", shutil.which("chromium") or ""] if c and os.path.exists(c)), None)
if not chrome: die("ما لكيت كروم — حط مساره بـCHROME")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--force-device-scale-factor=1",
                f"--window-size={Wd},{Ht}", "--virtual-time-budget=4000", f"--screenshot={png}", uri(hp)], capture_output=True)
if not os.path.exists(png): die("كروم ما طلّع صورة الكرت")

# 4) التجميع: الفيديو + الكرت بتلاشي، والصوت يخلص بهدوء
has_a = "audio" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout.strip())
X = 0.45   # مدة التلاشي
fc = (f"[1:v]scale={Wd}:{Ht},fps={FPS},format=yuv420p,setsar=1[c];[0:v]fps={FPS},format=yuv420p,setsar=1[v];"
      f"[v][c]xfade=transition=fade:duration={X}:offset={max(0.0, D - X):.3f}[vo]")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", SRC, "-loop", "1", "-t", f"{DUR + X:.3f}", "-i", png]
if has_a:
    fc += f";[0:a]afade=t=out:st={max(0.0, D - 1.2):.3f}:d=1.2,apad=pad_dur={DUR:.3f}[ao]"
    cmd += ["-filter_complex", fc, "-map", "[vo]", "-map", "[ao]", "-c:a", "aac", "-b:a", "192k"]
else:
    cmd += ["-filter_complex", fc, "-map", "[vo]"]
cmd += ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT]
r = subprocess.run(cmd)
shutil.rmtree(tmp, ignore_errors=True)
if r.returncode: die("ffmpeg فشل بالتجميع")
print(f"✅ {OUT} — كرت ختام منصة بسيط ({DUR:.1f} ث) بآخر الفيديو · {'عرضي' if wide else 'طولي'} {Wd}×{Ht}")
