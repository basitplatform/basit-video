# -*- coding: utf-8 -*-
"""هوية منصة بسيط ← مجلد الشغل.
  python3 scripts/00_brand.py <work>            ← يركّب الهوية (يكمّل اللي ناقص بـtheme.json، وما يغيّر شي موجود)
  python3 scripts/00_brand.py <work> --force    ← يكتب الهوية فوق الموجود (بس لو المستخدم طلب)
  python3 scripts/00_brand.py <work> --brand <اسم>  ← هوية ثانية من brand/<اسم>/brand.json

يسوّي:
  - ينسخ ملفات الخط لـ<work>/fonts/ والشعار لـ<work>/
  - يكتب بـ<work>/theme.json: الألوان (bg ink acc clay mut coverBg)، الخط (font + fontFiles)، الشعار، الحساب، كرت الختام، والروابط
  - يحسب onAcc (لون النص فوق لون التمييز)

كل القيم البصرية بملف brand/<اسم>/brand.json — عدّلها هناك، مو بالكود."""
import importlib.util, json, os, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def die(m):
    print("⛔ " + m); sys.exit(1)


args = sys.argv[1:]
if not args or args[0].startswith("-"):
    die(__doc__)
W = os.path.abspath(args[0]); FORCE = "--force" in args
name = args[args.index("--brand") + 1] if "--brand" in args else "basit"
BD = os.path.join(SK, "brand", name)
bp = os.path.join(BD, "brand.json")
if not os.path.exists(bp):
    die(f"ما لكيت هوية باسم «{name}» ({bp})")
if not os.path.isdir(W):
    die(f"مجلد الشغل {W} مو موجود")
B = json.load(open(bp, encoding="utf-8"))
C = B["colors"]
col = lambda k: C.get(k, k) if not str(k).startswith("#") else k

# 1) الخط والشعار ← مجلد الشغل
fd = os.path.join(W, "fonts"); os.makedirs(fd, exist_ok=True)
files = []
for f in B["font"]["files"]:
    src = os.path.join(BD, "fonts", f["file"])
    if not os.path.exists(src):
        die(f"ملف الخط ناقص: {src}")
    dst = os.path.join(fd, f["file"])
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
    files.append({"src": "fonts/" + f["file"], "weight": f["weight"]})
logos = {}
for k, fn in (B.get("logo") or {}).items():
    src = os.path.join(BD, fn)
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(W, fn)); logos[k] = fn

# 2) theme.json
brand = {k: col(v) for k, v in B["theme"].items()}
brand.update({
    "font": B["font"]["family"], "fontFiles": files,
    "handle": B.get("handle", ""),
    "outro": B.get("outro") or 0,
    "brand": {"name": B.get("name", ""), "tagline": B.get("tagline", ""), "links": B.get("links", {}), "id": name},
})
if logos.get("onDark"): brand["logo"] = logos["onDark"]
if logos.get("onLight"): brand["logoLight"] = logos["onLight"]

tp = os.path.join(W, "theme.json")
t = {}
if os.path.exists(tp):
    try:
        t = json.load(open(tp, encoding="utf-8"))
    except Exception:
        die(f"ما كدرت أقرا {tp}")
kept = []
for k, v in brand.items():
    if k in t and not FORCE:
        if t[k] != v: kept.append(k)
        continue
    t[k] = v

# 3) onAcc — نفس حسبة صفحة التعارف
spec = importlib.util.spec_from_file_location("onboard", os.path.join(SK, "scripts", "00_onboard.py"))
ob = importlib.util.module_from_spec(spec); spec.loader.exec_module(ob)
ob.set_on_acc(t)

tmp = tp + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(t, fh, ensure_ascii=False, indent=2)
os.replace(tmp, tp)
# 4) مشروع موشن (project.json)؟ نفس الهوية بصيغة محرّك الموشن
pp = os.path.join(W, "project.json")
if os.path.exists(pp):
    try:
        pj = json.load(open(pp, encoding="utf-8"))
    except Exception:
        die(f"ما كدرت أقرا {pp}")
    fam = B["font"]["family"]
    mot = {
        "palette": {"bg": t["bg"], "ink": t["ink"], "acc": t["acc"], "clay": t["clay"], "mut": t["mut"], "hi": col("white")},
        "fonts": {"display": fam, "body": fam, "num": "Inter"},
        "extraFonts": [{"family": fam, "file": f["src"], "weight": str(f["weight"])} for f in files],
    }
    pkept = []
    for k, v in mot.items():
        if k in pj and not FORCE:
            if pj[k] != v: pkept.append(k)
            continue
        pj[k] = v
    with open(pp + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(pj, fh, ensure_ascii=False, indent=1)
    os.replace(pp + ".tmp", pp)
    print(f"✅ وركّبتها بمشروع الموشن ({pp})" + (" — تركت: " + "، ".join(pkept) if pkept else ""))

print(f"✅ ركّبت هوية {B.get('name', name)} بـ{tp}")
print(f"   الألوان: خلفية {t.get('bg')} · نص {t.get('ink')} · تمييز {t.get('acc')} · إبراز {t.get('clay')} — الخط {t.get('font')} ({len(files)} أوزان)")
if kept:
    print("ℹ️ تركت هالقيم مثل ما هي لأنها موجودة من قبل: " + "، ".join(kept) + " (‎--force حتى أكتب فوقها، بس لو المستخدم طلب)")
