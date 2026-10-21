# تنصيب بلقن الفيديو مال منصة بسيط (ويندوز) — من أي مكان، بأمر واحد:
#   irm https://raw.githubusercontent.com/basitplatform/basit-video/main/install.ps1 | iex
# يسوّي: يتأكد من Claude Code ← ينصّب basit-video من متجر بسيط ← يشغّل التحديث التلقائي ← يعطّل بلقن majed-video لو موجود.
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$Repo = 'basitplatform/basit-video'; $Plugin = 'basit-video'; $Market = 'basit'

function Say($m) { Write-Host $m }
Say ''
Say '🎬 تنصيب بلقن الفيديو — منصة بسيط'

# 1) Claude Code
$cl = Get-Command claude -ErrorAction SilentlyContinue
if (-not $cl) {
  Say '⛔ Claude Code مو منصّب على هالجهاز.'
  Say '   نصّبه بهالأمر، وبعدين سكّر النافذة وافتح وحدة جديدة وأعد أمر التنصيب:'
  Say '   irm https://claude.ai/install.ps1 | iex'
  return
}
$verText = (& claude --version 2>$null | Out-String)
$m = [regex]::Match($verText, '\d+\.\d+\.\d+')
$ver = if ($m.Success) { [version]$m.Value } else { [version]'0.0.0' }
Say ("✅ Claude Code " + $m.Value)

# 2) بلقن ماجد الأصلي يسوّي نسخ مكررة من نفس السكلات — نعطّله
$list = (& claude plugin list 2>$null | Out-String)
if ($list -match 'majed-video') {
  Say '⚠️ لكيت بلقن majed-video — راح أعطّله حتى ما تتكرر السكلات (تكدر ترجعه بعدين).'
  & claude plugin disable 'majed-video@majed-plugins' 2>$null | Out-Null
}

# 3) التنصيب (أو التحديث لو منصّب)
if ($list -match "$Plugin@$Market") {
  Say '🔄 البلقن منصّب من قبل — دا أحدّثه…'
  & claude plugin update "$Plugin@$Market"
} elseif ($ver -ge [version]'2.1.292') {
  & claude plugin install $Plugin --marketplace $Repo
} else {
  & claude plugin marketplace add $Repo
  & claude plugin install "$Plugin@$Market"
}
if ($LASTEXITCODE -ne 0) { Say '⛔ التنصيب ما نجح — شوف الرسالة فوق، أو تأكد من النت وأعد الأمر.'; return }

# 4) التحديث التلقائي: extraKnownMarketplaces.basit.autoUpdate = true
$cfg = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE '.claude' }
$sp = Join-Path $cfg 'settings.json'
try {
  if (Test-Path $sp) { Copy-Item $sp "$sp.bak-basit" -Force }   # نسخة احتياطية قبل أي تعديل
  $s = if (Test-Path $sp) { Get-Content $sp -Raw -Encoding UTF8 | ConvertFrom-Json } else { [pscustomobject]@{} }
  if (-not ($s.PSObject.Properties.Name -contains 'extraKnownMarketplaces')) { $s | Add-Member -NotePropertyName extraKnownMarketplaces -NotePropertyValue ([pscustomobject]@{}) }
  $k = $s.extraKnownMarketplaces
  if (-not ($k.PSObject.Properties.Name -contains $Market)) {
    $k | Add-Member -NotePropertyName $Market -NotePropertyValue ([pscustomobject]@{ source = [pscustomobject]@{ source = 'github'; repo = $Repo } })
  }
  $e = $k.$Market
  if ($e.PSObject.Properties.Name -contains 'autoUpdate') { $e.autoUpdate = $true } else { $e | Add-Member -NotePropertyName autoUpdate -NotePropertyValue $true }
  New-Item -ItemType Directory -Force (Split-Path $sp) | Out-Null
  [System.IO.File]::WriteAllText($sp, ($s | ConvertTo-Json -Depth 50), (New-Object System.Text.UTF8Encoding($false)))
  Say '✅ التحديث التلقائي شغّال — أي نسخة جديدة توصلك لحالها.'
} catch {
  Say '⚠️ ما كدرت أشغّل التحديث التلقائي بروحي. شغّله مرة وحدة: افتح claude ← /plugin ← Marketplaces ← basit ← Enable auto-update'
}

Say ''
Say '🎉 خلص! افتح جلسة جديدة بـClaude Code (أو تبويب Code بتطبيق كلود) وجرّب:'
Say '   «سويلي ريل من هالفيديو» وأرفق فيديو.'
Say '   بأول استخدام كلود يفحص الأدوات اللي يحتاجها (ffmpeg، بايثون، كروم) ويجهّزها ويّاك.'
