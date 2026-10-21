# -*- coding: utf-8 -*-
"""تفريغ الكلام بتوقيت الكلمة ← <work>/a.json (نفس صيغة وِسبر: segments → words {word, start, end})
  python3 scripts/02a_transcribe.py <work> [--model medium]
  - يستخدم faster-whisper (أسرع وأخف، ويشتغل على ويندوز بلا torch). ماكو؟ يرجع لـopenai-whisper.
  - يقرا <work>/a.wav (لو ماكو، يطلّعه من src.mov)."""
import sys as _sys_u8   # ويندوز: الطباعة بالعربي بـUTF-8
try: _sys_u8.stdout.reconfigure(encoding="utf-8", errors="replace"); _sys_u8.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
import json, os, subprocess, sys

args = sys.argv[1:]
if not args: sys.exit(__doc__)
W = os.path.abspath(args[0]); model = args[args.index("--model") + 1] if "--model" in args else "medium"
wav = os.path.join(W, "a.wav")
if not os.path.exists(wav):
    src = os.path.join(W, "src.mov")
    if not os.path.exists(src): sys.exit("❌ ماكو a.wav ولا src.mov بمجلد الشغل")
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-y", wav], check=True)
out = {"language": "ar", "text": "", "segments": []}
try:
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    segs, _ = m.transcribe(wav, language="ar", word_timestamps=True, vad_filter=False, beam_size=5)
    for s in segs:
        out["segments"].append({"id": len(out["segments"]), "start": s.start, "end": s.end, "text": s.text,
                                "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in (s.words or [])]})
    eng = "faster-whisper"
except ImportError:
    try:
        import whisper
    except ImportError:
        sys.exit("❌ ماكو أداة تفريغ — نصّب وحدة: pip install faster-whisper")
    r = whisper.load_model(model).transcribe(wav, language="ar", word_timestamps=True, fp16=False, verbose=False)
    out["segments"] = [{"id": i, "start": s["start"], "end": s["end"], "text": s["text"], "words": s.get("words", [])} for i, s in enumerate(r["segments"])]
    eng = "openai-whisper"
out["text"] = "".join(x["text"] for x in out["segments"])
json.dump(out, open(os.path.join(W, "a.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"✅ a.json ({eng} · {model}) — {len(out['segments'])} جملة، {sum(len(x['words']) for x in out['segments'])} كلمة")
