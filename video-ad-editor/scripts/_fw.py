# -*- coding: utf-8 -*-
"""بديل faster-whisper بنفس شكل ناتج وِسبر — للويندوز وبلا torch.
   from _fw import transcribe   ←   transcribe(صوت 16k float32 أو مسار ملف) = {"text", "segments":[{start,end,text,words:[{word,start,end,probability}]}]}"""
import os
_M = None


def transcribe(audio, model=None, **_):
    global _M
    from faster_whisper import WhisperModel
    if _M is None:
        _M = WhisperModel(model or os.environ.get("FW_MODEL", "medium"), device="cpu", compute_type="int8", cpu_threads=os.cpu_count())
    segs, _info = _M.transcribe(audio, language="ar", word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
    out = []
    for s in segs:
        out.append({"start": s.start, "end": s.end, "text": s.text,
                    "words": [{"word": w.word, "start": w.start, "end": w.end, "probability": w.probability} for w in (s.words or [])]})
    return {"text": "".join(x["text"] for x in out), "segments": out}
