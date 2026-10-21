# يبني ملف البلقن من آخر كوميت:   python tools/build.py   →   dist/basit-video.plugin
# يشتغل على ويندوز بلا zip ولا python3. ما ينشر شي.
import io, json, os, shutil, subprocess, sys, tarfile, tempfile, zipfile
sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = [".claude-plugin", "video-ad-editor", "motion-video", "podcast-video", "montage-video", "thumbnail-video"]
MAX_FILES = 200  # حد رفع الملف بتطبيق كلود


def git(*args, binary=False):
    return subprocess.run(["git", "-C", REPO, "-c", "core.autocrlf=false", *args], check=True, capture_output=True,
                          text=not binary).stdout


def fail(msg):
    print("❌ " + msg); sys.exit(1)


if git("status", "--porcelain", "--", *PARTS).strip():
    fail("اكو تعديلات مو مكومتة — سوّي commit أول")

tmp = tempfile.mkdtemp()
try:
    tarfile.open(fileobj=io.BytesIO(git("archive", "HEAD", *PARTS, binary=True))).extractall(tmp, filter="data")
    p = os.path.join(tmp, "video-ad-editor")
    # مو للتشغيل: صور الشرح وملفات npm
    shutil.rmtree(os.path.join(p, "img"), ignore_errors=True)
    for f in ["package.json", "package-lock.json", os.path.join("motion", ".gitignore")]:
        if os.path.exists(os.path.join(p, f)):
            os.remove(os.path.join(p, f))
    # نجمع المجلدات الكبيرة بملف zip واحد (السكربتات تفكها أول مرة) علمود ما نتعدى حد الـ200 ملف
    for parent, name in [(os.path.join(p, "motion", "moves"), "previews"), (os.path.join(p, "motion"), "vendor")]:
        src = os.path.join(parent, name)
        if os.path.isdir(src):
            with zipfile.ZipFile(os.path.join(parent, name + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
                for root, _, files in os.walk(src):
                    for f in files:
                        full = os.path.join(root, f)
                        z.write(full, os.path.relpath(full, parent).replace(os.sep, "/"))
            shutil.rmtree(src)
    os.remove(os.path.join(tmp, ".claude-plugin", "marketplace.json"))

    v = open(os.path.join(p, "VERSION"), encoding="utf-8").read().strip()
    pv = json.load(open(os.path.join(tmp, ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"]
    if v != pv:
        fail(f"VERSION ({v}) ≠ plugin.json ({pv})")

    os.makedirs(os.path.join(REPO, "dist"), exist_ok=True)
    out = os.path.join(REPO, "dist", "basit-video.plugin")
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(REPO, "LICENSE"), "LICENSE"); count += 1   # رخصة MIT لازم تنتقل ويّا أي نسخة
        for part in PARTS:
            for root, _, files in os.walk(os.path.join(tmp, part)):
                for f in files:
                    if f == ".DS_Store":
                        continue
                    full = os.path.join(root, f)
                    z.write(full, os.path.relpath(full, tmp).replace(os.sep, "/"))
                    count += 1
    if count > MAX_FILES:
        fail(f"البلقن فيه {count} ملف (الحد {MAX_FILES})")
    if shutil.which("claude"):
        r = subprocess.run(["claude", "plugin", "validate", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            fail("فحص الـplugin فشل:\n" + r.stdout + r.stderr)
    print(f"✅ v{v} جاهز: dist/basit-video.plugin — {count} ملف، {os.path.getsize(out) / 1e6:.1f} ميقا")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
