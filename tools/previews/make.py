# يعيد رسم معاينات بنك الحركات (motion/moves/previews/NN.mp4) بهوية منصة بسيط.
#   python tools/previews/make.py                 ← كل الـ100 (يرسم ويقص ويبدّل المعاينات)
#   python tools/previews/make.py --only 1,8,51   ← حركات معيّنة بس
#   python tools/previews/make.py --sheet         ← ورقة لقطات للمراجعة بدل الفيديو (لقطة من نص كل حركة)
# يحتاج: node، ffmpeg، كروم أو إيدج، وpuppeteer-core (NODE_PATH أو node_modules قريب).
import json, os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SK = os.path.join(REPO, "video-ad-editor")
MO = os.path.join(SK, "motion")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "build", "proj")
DUR = 4.0

args = sys.argv[1:]
only = None
if "--only" in args:
    only = {int(x) for x in args[args.index("--only") + 1].split(",")}
SHEET = "--sheet" in args

cat = json.load(open(os.path.join(MO, "moves", "catalog.json"), encoding="utf-8"))["moves"]
moves = [{"n": m["n"], "id": m["id"]} for m in cat if (only is None or m["n"] in only)]
B = json.load(open(os.path.join(SK, "brand", "basit", "brand.json"), encoding="utf-8"))
col = B["colors"]
pal = {k: col[v] for k, v in B["theme"].items() if k in ("bg", "ink", "acc", "clay", "mut")}
pal["hi"] = col["white"]

# 1) المشروع
if os.path.isdir(PROJ):
    shutil.rmtree(PROJ)
os.makedirs(os.path.join(PROJ, "scenes")); os.makedirs(os.path.join(PROJ, "fonts"))
fam = B["font"]["family"]
for f in B["font"]["files"]:
    shutil.copyfile(os.path.join(SK, "brand", "basit", "fonts", f["file"]), os.path.join(PROJ, "fonts", f["file"]))
shutil.copyfile(os.path.join(SK, "brand", "basit", B["logo"]["onDark"]), os.path.join(PROJ, "logo-white.png"))
proj = {
    "name": "معاينات بنك الحركات — منصة بسيط", "fps": 60, "width": 1080, "height": 1920, "bpm": 120, "beatsPerBar": 4, "beatOffset": 0,
    "palette": pal, "fonts": {"display": fam, "body": fam, "num": "Inter"},
    "extraFonts": [{"family": fam, "file": "fonts/" + f["file"], "weight": str(f["weight"])} for f in B["font"]["files"]],
    "images": {"logo": "logo-white.png"}, "post": {"grain": 0, "vignette": 0},
    "scenes": [{"id": "m%d" % m["n"], "file": "scenes/all.js"} for m in moves],
}
json.dump(proj, open(os.path.join(PROJ, "project.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 2) الجدول الزمني + جمل الكابشن (للحركات اللي تقرا الكلام)
LINES = {1: "تعلّم المونتاج من الصفر ويّا منصة بسيط", 38: "كل مهارة تتعلّمها تفتحلك باب جديد"}
vo, scenes = [], []
for i, m in enumerate(moves):
    s = i * DUR
    scenes.append({"id": "m%d" % m["n"], "file": "scenes/all.js", "start": s, "end": s + DUR})
    if m["n"] in LINES:
        ws = LINES[m["n"]].split(); t0 = s + 0.3; step = 0.42
        vo.append({"id": "l%d" % m["n"], "text": LINES[m["n"]], "start": t0, "end": t0 + step * len(ws),
                   "words": [{"w": w, "s": round(t0 + k * step, 3), "e": round(t0 + (k + 1) * step - 0.04, 3)} for k, w in enumerate(ws)]})
total = DUR * len(moves)
json.dump({"duration": total, "bpm": 120, "beatsPerBar": 4, "scenes": scenes, "vo": vo},
          open(os.path.join(PROJ, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False)
demo = open(os.path.join(HERE, "demos.js"), encoding="utf-8").read()
open(os.path.join(PROJ, "scenes", "all.js"), "w", encoding="utf-8").write(
    "window.__CATALOG = " + json.dumps(moves, ensure_ascii=False) + ";\n" + demo)

# 3) الرسم
env = dict(os.environ)
if not env.get("CHROME"):
    for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              os.path.join(env.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]:
        if os.path.exists(c):
            env["CHROME"] = c; break
render = os.path.join(MO, "render.js")
if SHEET:
    ts = [str(i * DUR + 2.2) for i in range(len(moves))]
    r = subprocess.run(["node", render, PROJ, "preview", *ts, "--scale", "0.5"], env=env)
    if r.returncode: sys.exit("❌ الرسم فشل")
    print("✅ " + os.path.join(PROJ, "renders", "preview", "contact.png"))
    sys.exit(0)
r = subprocess.run(["node", render, PROJ, "all", "--scale", "0.5", "--fresh", "--workers", "3", "--crf", "18"], env=env)
if r.returncode: sys.exit("❌ الرسم فشل")
vid = os.path.join(PROJ, "renders", "video_s0.5.mp4")

# 4) القص لمعاينة لكل حركة
out = os.path.join(MO, "moves", "previews")
for i, m in enumerate(moves):
    dst = os.path.join(out, "%02d.mp4" % m["n"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % (i * DUR), "-i", vid, "-t", "%.3f" % DUR, "-an",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)
print("✅ انرسمت %d معاينة بـ%s" % (len(moves), out))
