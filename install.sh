#!/usr/bin/env bash
# تنصيب بلقن الفيديو مال منصة بسيط (ماك ولينكس) — من أي مكان، بأمر واحد:
#   curl -fsSL https://raw.githubusercontent.com/basitplatform/basit-video/main/install.sh | bash
# يسوّي: يتأكد من Claude Code ← ينصّب basit-video من متجر بسيط ← يشغّل التحديث التلقائي ← يعطّل بلقن majed-video لو موجود.
set -u
REPO='basitplatform/basit-video'; PLUGIN='basit-video'; MARKET='basit'
echo ""
echo "🎬 تنصيب بلقن الفيديو — منصة بسيط"

# 1) Claude Code
if ! command -v claude >/dev/null 2>&1; then
  echo "⛔ Claude Code مو منصّب على هالجهاز."
  echo "   نصّبه بهالأمر، وبعدين افتح نافذة طرفية جديدة وأعد أمر التنصيب:"
  echo "   curl -fsSL https://claude.ai/install.sh | bash"
  exit 1
fi
VER="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
echo "✅ Claude Code ${VER:-?}"
newer() { [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -1)" = "$2" ]; }   # $1 >= $2

# 2) بلقن ماجد الأصلي يسوّي نسخ مكررة من نفس السكلات — نعطّله
LIST="$(claude plugin list 2>/dev/null)"
if echo "$LIST" | grep -q "majed-video"; then
  echo "⚠️ لكيت بلقن majed-video — راح أعطّله حتى ما تتكرر السكلات (تكدر ترجعه بعدين)."
  claude plugin disable "majed-video@majed-plugins" >/dev/null 2>&1 || true
fi

# 3) التنصيب (أو التحديث لو منصّب)
if echo "$LIST" | grep -q "$PLUGIN@$MARKET"; then
  echo "🔄 البلقن منصّب من قبل — دا أحدّثه…"
  claude plugin update "$PLUGIN@$MARKET" || { echo "⛔ التحديث ما نجح — شوف الرسالة فوق."; exit 1; }
elif [ -n "${VER:-}" ] && newer "$VER" "2.1.292"; then
  claude plugin install "$PLUGIN" --marketplace "$REPO" || { echo "⛔ التنصيب ما نجح — تأكد من النت وأعد الأمر."; exit 1; }
else
  claude plugin marketplace add "$REPO" && claude plugin install "$PLUGIN@$MARKET" || { echo "⛔ التنصيب ما نجح — تأكد من النت وأعد الأمر."; exit 1; }
fi

# 4) التحديث التلقائي: extraKnownMarketplaces.basit.autoUpdate = true
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"; SP="$CFG/settings.json"; mkdir -p "$CFG"
[ -f "$SP" ] && cp "$SP" "$SP.bak-basit"   # نسخة احتياطية قبل أي تعديل
JS='const fs=require("fs"),p=process.argv[1],m=process.argv[2],r=process.argv[3];let s={};try{s=JSON.parse(fs.readFileSync(p,"utf8"))}catch(e){}
s.extraKnownMarketplaces=s.extraKnownMarketplaces||{};s.extraKnownMarketplaces[m]=s.extraKnownMarketplaces[m]||{source:{source:"github",repo:r}};
s.extraKnownMarketplaces[m].autoUpdate=true;fs.writeFileSync(p,JSON.stringify(s,null,2));'
PYS='import json,sys,os
p,m,r=sys.argv[1:4]; s=json.load(open(p)) if os.path.exists(p) else {}
k=s.setdefault("extraKnownMarketplaces",{}); e=k.setdefault(m,{"source":{"source":"github","repo":r}}); e["autoUpdate"]=True
json.dump(s,open(p,"w"),ensure_ascii=False,indent=2)'
if command -v python3 >/dev/null 2>&1 && python3 -c "import json" >/dev/null 2>&1 && python3 -c "$PYS" "$SP" "$MARKET" "$REPO" 2>/dev/null; then
  echo "✅ التحديث التلقائي شغّال — أي نسخة جديدة توصلك لحالها."
elif command -v node >/dev/null 2>&1 && node -e "$JS" "$SP" "$MARKET" "$REPO" 2>/dev/null; then
  echo "✅ التحديث التلقائي شغّال — أي نسخة جديدة توصلك لحالها."
else
  echo "⚠️ ما كدرت أشغّل التحديث التلقائي بروحي. شغّله مرة وحدة: افتح claude ← /plugin ← Marketplaces ← basit ← Enable auto-update"
fi

echo ""
echo "🎉 خلص! افتح جلسة جديدة بـClaude Code (أو تبويب Code بتطبيق كلود) وجرّب:"
echo "   «سويلي ريل من هالفيديو» وأرفق فيديو."
echo "   بأول استخدام كلود يفحص الأدوات اللي يحتاجها (ffmpeg، بايثون، كروم) ويجهّزها ويّاك."
