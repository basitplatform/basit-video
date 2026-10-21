# يحط اسم مستودع قيت هب بسكربتات التنصيب والـREADME (مرة وحدة):
#   python tools/set_repo.py <حساب>/basit-video
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2 or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", sys.argv[1]):
    sys.exit("الاستخدام: python tools/set_repo.py <حساب>/<مستودع>   مثل: basit-platform/basit-video")
repo = sys.argv[1]
for f in ("install.src.ps1", "install.sh", "README.md"):
    p = os.path.join(REPO_ROOT, f); s = open(p, encoding="utf-8").read()
    s2 = re.sub(r"__REPO__|[A-Za-z0-9_.-]+/basit-video(?=[/#\s'\"`)])", repo, s)
    open(p, "w", encoding="utf-8", newline="\n").write(s2)
    print(("✅ " if s2 != s else "— ") + f)
print("المستودع:", repo)
import subprocess; subprocess.run([sys.executable, os.path.join(REPO_ROOT, "tools", "make_installer.py")], check=True)
