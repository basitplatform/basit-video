# Basit video plugin installer (Windows). Generated from install.src.ps1 by tools/make_installer.py -- edit the source, not this file.
# Usage:  irm https://raw.githubusercontent.com/basitplatform/basit-video/main/install.ps1 | iex
function D($b) { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($b)) }
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$Repo = 'basitplatform/basit-video'; $Plugin = 'basit-video'; $Market = 'basit'

function Say($m) { Write-Host $m }
Say ''
Say (D '8J+OrCDYqtmG2LXZitioINio2YTZgtmGINin2YTZgdmK2K/ZitmIIOKAlCDZhdmG2LXYqSDYqNiz2YrYtw==')

$cl = Get-Command claude -ErrorAction SilentlyContinue
if (-not $cl) {
  Say (D '4puUIENsYXVkZSBDb2RlINmF2Ygg2YXZhti12ZHYqCDYudmE2Ykg2YfYp9mE2KzZh9in2LIu')
  Say (D 'ICAg2YbYtdmR2KjZhyDYqNmH2KfZhNij2YXYsdiMINmI2KjYudiv2YrZhiDYs9mD2ZHYsSDYp9mE2YbYp9mB2LDYqSDZiNin2YHYqtitINmI2K3Yr9ipINis2K/Zitiv2Kkg2YjYo9i52K8g2KPZhdixINin2YTYqtmG2LXZitioOg==')
  Say '   irm https://claude.ai/install.ps1 | iex'
  return
}
$verText = (& claude --version 2>$null | Out-String)
$m = [regex]::Match($verText, '\d+\.\d+\.\d+')
$ver = if ($m.Success) { [version]$m.Value } else { [version]'0.0.0' }
Say ((D '4pyFIENsYXVkZSBDb2RlIA==') + $m.Value)

$list = (& claude plugin list 2>$null | Out-String)
if ($list -match 'majed-video') {
  Say (D '4pqg77iPINmE2YPZitiqINio2YTZgtmGIG1hamVkLXZpZGVvIOKAlCDYsdin2K0g2KPYudi32ZHZhNmHINit2KrZiSDZhdinINiq2KrZg9ix2LEg2KfZhNiz2YPZhNin2KogKNiq2YPYr9ixINiq2LHYrNi52Ycg2KjYudiv2YrZhiku')
  & claude plugin disable 'majed-video@majed-plugins' 2>$null | Out-Null
}

if ($list -match "$Plugin@$Market") {
  Say (D '8J+UhCDYp9mE2KjZhNmC2YYg2YXZhti12ZHYqCDZhdmGINmC2KjZhCDigJQg2K/YpyDYo9it2K/Zkdir2YfigKY=')
  & claude plugin update "$Plugin@$Market"
} elseif ($ver -ge [version]'2.1.292') {
  & claude plugin install $Plugin --marketplace $Repo
} else {
  & claude plugin marketplace add $Repo
  & claude plugin install "$Plugin@$Market"
}
if ($LASTEXITCODE -ne 0) { Say (D '4puUINin2YTYqtmG2LXZitioINmF2Kcg2YbYrNitIOKAlCDYtNmI2YEg2KfZhNix2LPYp9mE2Kkg2YHZiNmC2Iwg2KPZiCDYqtij2YPYryDZhdmGINin2YTZhtiqINmI2KPYudivINin2YTYo9mF2LEu'); return }

$cfg = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE '.claude' }
$sp = Join-Path $cfg 'settings.json'
try {
  if (Test-Path $sp) { Copy-Item $sp "$sp.bak-basit" -Force }
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
  Say (D '4pyFINin2YTYqtit2K/ZitirINin2YTYqtmE2YLYp9im2Yog2LTYutmR2KfZhCDigJQg2KPZiiDZhtiz2K7YqSDYrNiv2YrYr9ipINiq2YjYtdmE2YMg2YTYrdin2YTZh9inLg==')
} catch {
  Say (D '4pqg77iPINmF2Kcg2YPYr9ix2Kog2KPYtNi62ZHZhCDYp9mE2KrYrdiv2YrYqyDYp9mE2KrZhNmC2KfYptmKINio2LHZiNit2YouINi02LrZkdmE2Ycg2YXYsdipINmI2K3Yr9ipOiDYp9mB2KrYrSBjbGF1ZGUg4oaQIC9wbHVnaW4g4oaQIE1hcmtldHBsYWNlcyDihpAgYmFzaXQg4oaQIEVuYWJsZSBhdXRvLXVwZGF0ZQ==')
}

Say ''
Say (D '8J+OiSDYrtmE2LUhINin2YHYqtitINis2YTYs9ipINis2K/Zitiv2Kkg2KjZgENsYXVkZSBDb2RlICjYo9mIINiq2KjZiNmK2KggQ29kZSDYqNiq2LfYqNmK2YIg2YPZhNmI2K8pINmI2KzYsdmR2Kg6')
Say (D 'ICAgwqvYs9mI2YrZhNmKINix2YrZhCDZhdmGINmH2KfZhNmB2YrYr9mK2YjCuyDZiNij2LHZgdmCINmB2YrYr9mK2Ygu')
Say (D 'ICAg2KjYo9mI2YQg2KfYs9iq2K7Yr9in2YUg2YPZhNmI2K8g2YrZgdit2LUg2KfZhNij2K/ZiNin2Kog2KfZhNmE2Yog2YrYrdiq2KfYrNmH2KcgKGZmbXBlZ9iMINio2KfZitir2YjZhtiMINmD2LHZiNmFKSDZiNmK2KzZh9mR2LLZh9inINmI2YrZkdin2YMu')
