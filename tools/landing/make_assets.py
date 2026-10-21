# يصمم صور صفحة المستودع (assets/) بهوية منصة بسيط — HTML ← صورة بكروم بلا واجهة.
#   python tools/landing/make_assets.py [<مجلد لقطات الريل>]
# اللقطات (اختيارية): f1.5.jpg f8.8.jpg f25.5.jpg cover.jpg من ريل حقيقي طلّعه البلقن.
import html, json, os, pathlib, shutil, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
R = pathlib.Path(__file__).resolve().parents[2]
SK = R / "video-ad-editor"; BR = SK / "brand" / "basit"; OUT = R / "assets"; OUT.mkdir(exist_ok=True)
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
B = json.loads((BR / "brand.json").read_text(encoding="utf-8")); C = B["colors"]
NAVY, DEEP, BLUE, SKY, CORAL, LIGHT, WHITE = C["navy"], C["deepBlue"], C["blue"], C["sky"], C["coral"], C["light"], C["white"]
uri = lambda p: pathlib.Path(p).resolve().as_uri()
FACES = "".join(f"@font-face{{font-family:'MA';src:url('{uri(BR / 'fonts' / f['file'])}');font-weight:{f['weight']}}}" for f in B["font"]["files"])
LOGO_W, LOGO_C = uri(BR / "logo-white.png"), uri(BR / "logo-color.png")
img = lambda n: uri(SRC / n) if SRC and (SRC / n).exists() else ""
CHROME = os.environ.get("CHROME") or next(c for c in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"] if os.path.exists(c))
BASE = f"""{FACES}*{{margin:0;padding:0;box-sizing:border-box}}html,body{{font-family:'MA',sans-serif;direction:rtl;-webkit-font-smoothing:antialiased}}
.chip{{display:inline-flex;align-items:center;gap:10px;padding:14px 26px;border-radius:999px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.14);color:{WHITE};font-weight:600;font-size:26px}}
.code{{direction:ltr;font-family:Consolas,'Courier New',monospace;font-weight:700;background:#0B2F47;color:{SKY};border-radius:14px;padding:12px 18px;font-size:19px;display:inline-block}}"""


def shot(name, w, h, body, css="", bg=NAVY):
    d = tempfile.mkdtemp(); p = os.path.join(d, "p.html")
    open(p, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg}}}{css}</style></head><body>{body}</body></html>")
    out = OUT / name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", "--virtual-time-budget=5000", f"--screenshot={out}", uri(p)], capture_output=True)
    shutil.rmtree(d, ignore_errors=True)
    print(("✅ " if out.exists() else "❌ ") + name)


# 1) الغلاف الرئيسي
phone = lambda src, rot, x, y, z: (f"<div class='ph' style='left:{x}px;top:{y}px;transform:rotate({rot}deg);z-index:{z}'>"
                                   + (f"<img src='{src}'>" if src else "<div class='ph0'></div>") + "</div>")
shot("hero.png", 1600, 720, f"""
<div class='glow'></div>
{phone(img('f8.8.jpg'), -9, 30, 130, 1)}{phone(img('f1.5.jpg'), 0, 225, 85, 3)}{phone(img('f25.5.jpg'), 9, 420, 130, 2)}
<div class='tx'>
 <div class='k'><img src='{LOGO_W}'><span>بلقن الفيديو · لـ Claude Code</span></div>
 <h1>تحچي للكاميرا…<br>وتستلم ريل جاهز للنشر</h1>
 <p>يشيل السكتات، يكتب كابشن عربي يمشي ويّا كلامك، ويرسم موشن<br>قرافيكس بهوية بسيط — بلا برنامج مونتاج، وبالعراقي.</p>
 <div class='chips'><span class='chip'>🎙️ ريل من فيديو كلام</span><span class='chip'>🎧 بودكاست</span><span class='chip'>🎞️ مونتاج</span><span class='chip'>✨ موشن</span><span class='chip'>🖼️ كفر وثمبنيل</span></div>
</div>""", f"""
body{{background:linear-gradient(120deg,#0B2F47 0%,{NAVY} 55%,{DEEP} 100%);position:relative}}
.glow{{position:absolute;width:700px;height:700px;border-radius:50%;left:-120px;top:-60px;background:radial-gradient(circle,rgba(35,161,211,.35),rgba(35,161,211,0) 65%)}}
.ph{{position:absolute;width:228px;height:476px;border-radius:34px;background:#071E2E;padding:9px;box-shadow:0 30px 70px rgba(0,0,0,.45)}}
.ph img,.ph0{{width:100%;height:100%;border-radius:26px;object-fit:cover;display:block;background:{DEEP}}}
.tx{{position:absolute;right:70px;top:58px;width:850px;color:{WHITE}}}
.k{{display:flex;align-items:center;gap:16px;color:{SKY};font-weight:800;font-size:28px}} .k img{{height:46px}}
h1{{font-weight:900;font-size:64px;line-height:1.2;margin:22px 0 18px}}
p{{font-weight:500;font-size:26px;line-height:1.6;color:{LIGHT};opacity:.92}}
.chips{{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}} .chip{{font-size:22px;padding:11px 20px}}""")

# 2) زر التنصيب
shot("btn-install.png", 832, 148, "<div class='b'><span>⚡</span> نصّبه بأمر واحد — ويتحدّث لحاله</div>", f"""
html,body{{background:transparent}} .b{{margin:14px auto;width:800px;height:120px;border-radius:60px;background:{CORAL};color:{WHITE};
display:flex;align-items:center;justify-content:center;gap:16px;font-weight:900;font-size:42px;box-shadow:0 12px 30px rgba(251,87,52,.35)}}""", bg="transparent")

shot("btn-download.png", 832, 148, "<div class='b'><span>⬇️</span> حمّل الملف — لتطبيق كلود</div>", f"""
html,body{{background:transparent}} .b{{margin:14px auto;width:800px;height:120px;border-radius:60px;background:{WHITE};color:{NAVY};border:5px solid {SKY};
display:flex;align-items:center;justify-content:center;gap:16px;font-weight:900;font-size:40px;box-shadow:0 12px 30px rgba(21,85,127,.18)}}""", bg="transparent")

# 3) ثلاث خطوات
card = lambda n, t, s, extra, foot: (f"<div class='c'><div class='n'>{n}</div><h2>{t}</h2><p>{s}</p>{extra}<div class='f'>{foot}</div></div>")
shot("start-steps.png", 1600, 640, "<div class='row'>"
     + card(1, "الصق أمر واحد بالطرفية", "ويندوز (PowerShell) أو ماك/لينكس — من أي مكان بجهازك:",
            "<div class='code'>irm https://raw.githubusercontent.com/basitplatform/basit-video/main/install.ps1 | iex</div>", "دقيقة وحدة · يشغّل التحديث التلقائي")
     + card(2, "افتح جلسة جديدة", "بـClaude Code بالطرفية، أو تبويب Code بتطبيق كلود.", "<div class='pill'>claude</div>", "الطرفية أو التطبيق — نفس الشي")
     + card(3, "أرفق الفيديو واكتب جملة", "وكلود يكمّل الشغل كله ويّاك بالعراقي:", "<div class='pill'>«سويلي ريل من هالفيديو»</div>", "أول مرة يجهّز الأدوات ويّاك")
     + "</div>", f"""
body{{background:{LIGHT}}} .row{{display:flex;gap:34px;padding:44px 40px}}
.c{{flex:1;background:{WHITE};border-radius:34px;padding:38px 38px 30px;height:552px;position:relative;box-shadow:0 14px 40px rgba(21,85,127,.10)}}
.n{{width:78px;height:78px;border-radius:50%;background:{NAVY};color:{WHITE};font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:center}}
h2{{font-weight:900;font-size:44px;color:{NAVY};margin:26px 0 14px;line-height:1.25}} p{{font-weight:500;font-size:25px;color:#3C5A70;line-height:1.55;margin-bottom:20px}}
.code{{font-size:15.5px;white-space:normal;word-break:break-all;line-height:1.5}}
.pill{{display:inline-block;background:rgba(35,161,211,.14);color:{DEEP};font-weight:800;font-size:31px;border-radius:18px;padding:14px 22px}}
.f{{position:absolute;bottom:30px;right:38px;left:38px;font-weight:600;font-size:21px;color:#7C93A4;border-top:2px solid {LIGHT};padding-top:18px}}""")

# 4) بطاقات السكلات (9:16)
def skill(name, emoji, title, lines, art):
    shot(name, 540, 960, f"<div class='e'>{emoji}</div><h3>{title}</h3><div class='art'>{art}</div><ul>{''.join(f'<li>{l}</li>' for l in lines)}</ul><img class='lg' src='{LOGO_W}'>", f"""
body{{background:linear-gradient(170deg,{NAVY},#0B2F47);color:{WHITE};padding:56px 46px;position:relative}}
.e{{font-size:64px}} h3{{font-weight:900;font-size:50px;line-height:1.2;margin:14px 0 26px}}
.art{{height:380px;border-radius:28px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;gap:16px;padding:20px}}
ul{{list-style:none;margin-top:30px}} li{{font-weight:600;font-size:27px;line-height:1.5;color:{LIGHT};padding-right:30px;position:relative;margin-bottom:10px}}
li:before{{content:'';position:absolute;right:0;top:15px;width:14px;height:14px;border-radius:50%;background:{SKY}}}
.lg{{position:absolute;bottom:44px;left:46px;height:44px;opacity:.9}}
.b{{border-radius:16px;background:{SKY}}} .w{{background:{WHITE};border-radius:16px}} .c{{background:{CORAL};border-radius:16px}}""")

skill("card-podcast.png", "🎧", "بودكاست<br>ومقابلات",
      ["كاميرتين أو أكثر ← ريلات عمودية", "هوك مكتوب أول كل ريل", "الحلقة كاملة 16:9 لليوتيوب"],
      "<div class='w' style='width:250px;height:142px;position:relative'><div class='b' style='position:absolute;inset:14px;opacity:.5'></div></div><div style='font-size:54px;color:#23A1D3'>←</div><div class='w' style='width:88px;height:156px;position:relative'><div class='c' style='position:absolute;left:10px;right:10px;bottom:12px;height:22px'></div></div>")
skill("card-montage.png", "🎞️", "مونتاج<br>على الإيقاع",
      ["مجلد مقاطع بلا كلام ← فيديو واحد", "يختار أحلى لحظة من كل مقطع", "يقطع على نبضات الصوت"],
      "".join(f"<div class='{c}' style='width:62px;height:{h}px'></div>" for c, h in [("b", 120), ("w", 230), ("b", 170), ("c", 290), ("w", 150), ("b", 250)]))
skill("card-motion.png", "✨", "شرح<br>بالموشن",
      ["فيلم موشن من نص أو فكرة", "صوت مولّد عراقي أو صوتك", "شرح موقع أو تطبيق داخل جوال"],
      f"<div style='text-align:center'><div style='font-weight:900;font-size:86px;color:{SKY}'>بسيط</div><div style='font-weight:600;font-size:30px;color:{WHITE};opacity:.85;margin-top:10px'>تعلّم لتصنع الفرق</div></div>")
skill("card-thumb.png", "🖼️", "كفر<br>وثمبنيل",
      ["كفر الريل = أول فريم", "ينقرا بشبكة البروفايل", "ثمبنيل يوتيوب بثلاث أفكار"],
      (f"<img src='{img('cover.jpg')}' style='height:340px;border-radius:18px'>" if img("cover.jpg") else "<div class='w' style='width:190px;height:338px'></div>"))

# 5) العراقي
bub = lambda who, t: f"<div class='m {who}'>{t}</div>"
shot("dialect.png", 1600, 560, "<div class='l'><h2>يحچي عراقي…<br>وبأي لهجة تريدها</h2><p>الدردشة، الأسئلة، الهوك، الكروت، ورسائل الشغل — كلها عراقي. تريد خليجي أو مصري أو فصحى؟ بس كولها.</p></div><div class='chat'>"
     + bub("u", "سويلي ريل من هالفيديو") + bub("a", "شلت السكتات — نص الفيديو راح. هسه دا أفرّغ كلامك، 3 دقايق.") + bub("a", "اكو مشكلة بالإضاءة، أعدّلها؟")
     + bub("u", "إي. ومن هسه احچي خليجي") + bub("a", "أبشر، من الحين أكلمك خليجي 👌") + "</div>", f"""
body{{background:{LIGHT};display:flex;align-items:center;gap:60px;padding:0 80px}} .l{{width:620px}}
h2{{font-weight:900;font-size:64px;line-height:1.2;color:{NAVY}}} p{{font-weight:500;font-size:28px;line-height:1.6;color:#3C5A70;margin-top:20px}}
.chat{{flex:1;display:flex;flex-direction:column;gap:14px}}
.m{{max-width:620px;padding:18px 26px;border-radius:26px;font-weight:600;font-size:28px;line-height:1.45}}
.u{{align-self:flex-start;background:{NAVY};color:{WHITE};border-bottom-right-radius:8px}}
.a{{align-self:flex-end;background:{WHITE};color:{NAVY};border-bottom-left-radius:8px;box-shadow:0 8px 24px rgba(21,85,127,.10)}}""")

# 6) بانر بسيط بالآخر
shot("basit-banner.png", 1600, 480, f"""<img class='lg' src='{LOGO_W}'><div class='t'><h2>تخيّل شكد تكدر تبدع أكثر<br>لما تتعلّم الأدوات الصح</h2>
<p>دورات وورش تطبيقية بالمحتوى والتصميم والذكاء الاصطناعي.</p><div class='cta'>basit.tv ←</div></div>""", f"""
body{{background:linear-gradient(110deg,{DEEP},{NAVY});color:{WHITE};display:flex;align-items:center;gap:70px;padding:0 90px;position:relative;overflow:hidden}}
body:after{{content:'';position:absolute;left:-80px;top:-120px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(35,161,211,.4),rgba(35,161,211,0) 65%)}}
.lg{{height:170px;position:relative;z-index:1}} h2{{font-weight:900;font-size:58px;line-height:1.25}} p{{font-weight:500;font-size:28px;color:{LIGHT};margin:18px 0 26px}}
.cta{{display:inline-block;background:{CORAL};color:{WHITE};font-weight:900;font-size:34px;border-radius:999px;padding:14px 38px;direction:ltr}}""")
print("✔ الصور بـ", OUT)
