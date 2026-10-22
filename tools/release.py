# ينشر تحديث للمستخدمين بأمر واحد:
#   python tools/release.py            ← يرفع رقم الإصدار (3.5.0 ← 3.5.1)
#   python tools/release.py minor      ← (3.5.0 ← 3.6.0)    · major ← (4.0.0)
#   python tools/release.py --dry      ← يفحص بس، بلا حفظ ولا رفع
# يسوّي: يرفع الرقم بـplugin.json وVERSION ← يفحص البلقن ← commit ← tag ← push (الفرع main وعلامة الإصدار بس). المستخدمين يوصلهم التحديث لحاله.
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def publish_release(ver):
    """يسوّي Release على قيت هب ويرفع dist/basit-video.plugin (زر «حمّل الملف» بالصفحة) — بتسجيل الدخول المحفوظ بقيت."""
    import urllib.request, urllib.error
    repo = "basitplatform/basit-video"
    cr = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n", capture_output=True, text=True, timeout=60)
    tok = next((l.split("=", 1)[1] for l in cr.stdout.splitlines() if l.startswith("password=")), None)
    if not tok:
        print(f"⚠️ ما لكيت تسجيل دخول قيت هب محفوظ — ارفع الملف بإيدك: https://github.com/{repo}/releases/new (العلامة v{ver})"); return
    H = {"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json", "User-Agent": "basit-release", "X-GitHub-Api-Version": "2022-11-28"}
    def call(url, data=None, method="GET", extra=None):
        req = urllib.request.Request(url, data=data, method=method, headers={**H, **(extra or {})})
        try:
            with urllib.request.urlopen(req, timeout=300) as f: return f.status, json.loads(f.read() or b"{}")
        except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b"{}")
    body = (f"## basit-video v{ver}\n\n**تنصيب ويتحدّث لحاله** — ويندوز: `irm https://raw.githubusercontent.com/{repo}/main/install.ps1 | iex` · "
            f"ماك/لينكس: `curl -fsSL https://raw.githubusercontent.com/{repo}/main/install.sh | bash`\n\n"
            "أو حمّل `basit-video.plugin` من تحت وارفعه بتطبيق كلود (Customize ← Plugins ← Upload plugin).")
    st, rel = call(f"https://api.github.com/repos/{repo}/releases", json.dumps({"tag_name": f"v{ver}", "name": f"basit-video v{ver}", "body": body, "make_latest": "true"}).encode(), "POST", {"Content-Type": "application/json"})
    if st not in (200, 201):
        print(f"⚠️ ما كدرت أسوّي الـRelease ({st} {rel.get('message', '')}) — ارفع الملف بإيدك من https://github.com/{repo}/releases/new"); return
    data = open(os.path.join(R, "dist", "basit-video.plugin"), "rb").read()
    st, a = call(rel["upload_url"].split("{")[0] + "?name=basit-video.plugin", data, "POST", {"Content-Type": "application/zip"})
    print(f"✅ زر «حمّل الملف» صار على v{ver}: {rel.get('html_url')}" if st in (200, 201) else f"⚠️ الـRelease انسوّى بس الملف ما انرفع ({st}) — ارفعه بإيدك: {rel.get('html_url')}")


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
    p = run("git", "push", "origin", "HEAD:main")   # الفرع بس — مو --tags (حتى ما ترتفع علامات قديمة)
    if not p.returncode: p = run("git", "push", "origin", f"v{new}")
    if p.returncode: sys.exit(f"❌ الرفع لقيت هب ما نجح — تأكد إنك مسجّل دخول وأعد: git push origin HEAD:main && git push origin v{new}")
    print(f"✅ v{new} انرفع — المستخدمين يوصلهم التحديث بأول جلسة (خلال دقايق من بدايتها).")
    run(sys.executable, os.path.join(R, "tools", "build.py"), check=True)
    publish_release(new)
else:
    print(f"✅ v{new} انحفظ محلياً. ماكو origin — اربط المستودع أول (شوف README).")
