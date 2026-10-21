# ينشر تحديث للمستخدمين بأمر واحد:
#   python tools/release.py            ← يرفع رقم الإصدار (3.5.0 ← 3.5.1)
#   python tools/release.py minor      ← (3.5.0 ← 3.6.0)    · major ← (4.0.0)
#   python tools/release.py --dry      ← يفحص بس، بلا حفظ ولا رفع
# يسوّي: يرفع الرقم بـplugin.json وVERSION ← يفحص البلقن ← commit ← tag ← push. المستخدمين يوصلهم التحديث لحاله.
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]; part = next((a for a in args if a in ("patch", "minor", "major")), "patch"); DRY = "--dry" in args
run = lambda *c, **k: subprocess.run(list(c), cwd=R, **k)
if run("git", "status", "--porcelain", capture_output=True, text=True).stdout.strip() and not DRY:
    print("ℹ️ اكو تعديلات مو محفوظة — راح تنحفظ ويّا الإصدار.")
pj = os.path.join(R, ".claude-plugin", "plugin.json"); d = json.load(open(pj, encoding="utf-8"))
a, b, c = (int(x) for x in d["version"].split("."))
new = {"patch": f"{a}.{b}.{c + 1}", "minor": f"{a}.{b + 1}.0", "major": f"{a + 1}.0.0"}[part]
print(f"الإصدار: {d['version']} ← {new}")
v = run("claude", "plugin", "validate", R, capture_output=True, text=True, encoding="utf-8")
if v.returncode: sys.exit("❌ فحص البلقن فشل:\n" + v.stdout + v.stderr)
if DRY: sys.exit("✅ الفحص نجح (--dry: ما حفظت ولا رفعت)")
d["version"] = new; json.dump(d, open(pj, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
open(os.path.join(R, "video-ad-editor", "VERSION"), "w", encoding="utf-8", newline="\n").write(new + "\n")
run(sys.executable, os.path.join(R, "tools", "make_installer.py"), check=True)   # install.ps1 دايماً من المصدر
run("git", "add", "-A", check=True)
run("git", "commit", "-q", "-m", f"v{new}", check=True)
run("git", "tag", f"v{new}", check=True)
if not run("git", "remote", "get-url", "origin", capture_output=True).returncode:
    p = run("git", "push", "origin", "HEAD:main", "--tags")
    if p.returncode: sys.exit("❌ الرفع لقيت هب ما نجح — تأكد إنك مسجّل دخول وأعد: git push origin HEAD:main --tags")
    print(f"✅ v{new} انرفع — المستخدمين يوصلهم التحديث بأول جلسة (خلال دقايق من بدايتها).")
else:
    print(f"✅ v{new} انحفظ محلياً. ماكو origin — اربط المستودع أول (شوف README).")
