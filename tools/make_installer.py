# يولّد install.ps1 (أحرف إنقليزية بس — ASCII) من install.src.ps1 (عربي مقروء):
#   python tools/make_installer.py
# ليش: PowerShell 5.1 (المنصّب ويّا ويندوز) يقرا الملف بلا BOM بترميز ANSI فيتخربط العربي ويطيح السكربت.
# النصوص العربية تنحفظ base64 وتنفك وقت التشغيل، والتعليقات العربية تنشال.
import base64, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(R, "install.src.ps1"), encoding="utf-8").read()
AR = re.compile(r"[^\x00-\x7F]")
out = ["# Basit video plugin installer (Windows). Generated from install.src.ps1 by tools/make_installer.py -- edit the source, not this file.",
       "# Usage:  irm https://raw.githubusercontent.com/__REPO_LINE__/main/install.ps1 | iex",
       "function D($b) { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($b)) }"]
repo = re.search(r"\$Repo = '([^']*)'", src).group(1)
out[1] = out[1].replace("__REPO_LINE__", repo)
enc = lambda s: "(D '" + base64.b64encode(s.encode("utf-8")).decode() + "')"
for line in src.split("\n"):
    st = line.strip()
    if st.startswith("#"):
        continue                                   # تعليقات المصدر (عربي) ما تنقل
    if "#" in line and AR.search(line.split("#", 1)[1] if "'" not in line.split("#", 1)[1] else ""):
        line = line.split("#", 1)[0].rstrip()      # تعليق عربي بآخر السطر
    line = re.sub(r"'((?:[^']|'')*)'", lambda m: enc(m.group(1).replace("''", "'")) if AR.search(m.group(1)) else m.group(0), line)
    line = re.sub(r'"([^"]*)"', lambda m: enc(m.group(1)) if AR.search(m.group(1)) and "$" not in m.group(1) else m.group(0), line)
    if AR.search(line):
        sys.exit("❌ سطر بيه عربي ما انحوّل: " + line)
    out.append(line)
open(os.path.join(R, "install.ps1"), "w", encoding="ascii", newline="\r\n").write("\n".join(out).rstrip() + "\n")
print("✅ install.ps1 (ASCII) من install.src.ps1")
