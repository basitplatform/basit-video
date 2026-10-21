<div dir="rtl">

# بلقن الفيديو — منصة بسيط

بلقن منصة بسيط لـ Claude Code، يحچي عراقي ويطلّع كل فيديو بهوية بسيط. فيه 5 سكلات:

| السكل | شيسوي |
|---|---|
| `video-ad-editor` | ريل عمودي من فيديو كلام: يشيل السكتات، كابشن عربي بتوقيت الكلمة، وموشن قرافيكس |
| `motion-video` | فيديو شرح موشن 3D من نص، بلا شخص |
| `podcast-video` | بودكاست بكاميرتين أو أكثر، الحلقة كاملة أو ريلات منها |
| `montage-video` | مونتاج مقاطع على الإيقاع، بلا كلام |
| `thumbnail-video` | كفرات الريلات وثمبنيلات يوتيوب |

## التنصيب — أمر واحد، من أي مكان
افتح الطرفية والصق السطر حسب جهازك. ما يحتاج تنزّل ملف ولا تحطه بمكان معيّن:

**ويندوز** (PowerShell):
```
irm https://raw.githubusercontent.com/basitplatform/basit-video/main/install.ps1 | iex
```

**ماك ولينكس** (Terminal):
```
curl -fsSL https://raw.githubusercontent.com/basitplatform/basit-video/main/install.sh | bash
```

السكربت يتأكد إن Claude Code منصّب، وينصّب البلقن، ويشغّل التحديث التلقائي، ويعطّل بلقن `majed-video` لو موجود حتى ما تتكرر السكلات.
بعدها افتح جلسة جديدة واكتب مثلاً «سويلي ريل من هالفيديو».

**التحديثات توصلك لحالها:** كل ما ينزل إصدار جديد، Claude Code يجيبه بأول جلسة.

<details><summary>تنصيب يدوي (بدون السكربت)</summary>

```
claude plugin install basit-video --marketplace basitplatform/basit-video
```
وبعدين شغّل التحديث التلقائي مرة وحدة: افتح `claude` ← `/plugin` ← **Marketplaces** ← **basit** ← **Enable auto-update**.
</details>

## نشر تحديث (لمنصة بسيط)
بعد أي تعديل:
```
python tools/release.py            # 3.5.0 ← 3.5.1
python tools/release.py minor      # 3.5.0 ← 3.6.0
```
يرفع رقم الإصدار، يفحص البلقن، ويرفعه لقيت هب. المستخدمين يوصلهم التحديث لحاله.
⚠️ لازم يتغيّر رقم الإصدار حتى يوصل التحديث — `release.py` يسويها لحاله.

**أول مرة بس — ربط المستودع:**
```
python tools/set_repo.py <حسابك>/basit-video
git remote add origin https://github.com/<حسابك>/basit-video.git
```

**ملف `.plugin` (بلا نت، اختياري):** `python tools/build.py` يطلّع `dist/basit-video.plugin` للرفع اليدوي بتطبيق كلود (هالطريقة ما تتحدّث لحالها).

## معاينات بنك الحركات
المعاينات الـ100 (`video-ad-editor/motion/moves/previews/`) مرسومة بهوية بسيط بأداة `tools/previews/make.py` (ما تدخل بملف البلقن):
```
python tools/previews/make.py --sheet            # ورقة لقطات للمراجعة
python tools/previews/make.py                    # يرسم الـ100 ويبدّلها
python tools/previews/make.py --only 15,46      # حركات معيّنة بس
```
تحتاج node وffmpeg وكروم، وpuppeteer-core (حط مساره بـ`NODE_PATH`).

## الهوية
كل الإعدادات البصرية (الألوان، خط Montserrat Arabic، الشعار، الروابط، كرت الختام) بملف `video-ad-editor/brand/basit/brand.json`. عدّلها هناك بس، و`scripts/00_brand.py` يركّبها بكل فيديو.

## روابط منصة بسيط
- الموقع: https://basit.tv
- إنستغرام: https://www.instagram.com/basit_platform/
- فيسبوك: https://facebook.com/basit.platform/

## الحقوق والتراخيص
- **المشروع:** رخصة MIT، بحقوق منصة بسيط على التعديلات والتطويرات. إشعار الحقوق الأصلي محفوظ داخل `LICENSE` لأن الرخصة تفرض بقاءه.
- **الخطوط:** خط منصة بسيط الرسمي **Montserrat Arabic** بكل أوزانه (رخصة SIL OFL 1.1 — `video-ad-editor/brand/basit/fonts/OFL.txt`)، وباقي الخطوط برخصها OFL (`video-ad-editor/motion/fonts/LICENSES.txt`).
- **المكونات التقنية:** مكتبة three.js برخصة MIT (`video-ad-editor/motion/vendor/three/LICENSE`).
- **مصادر الحركات:** مراجع إلهام، والحركات مكتوبة من جديد بهوية بسيط (`video-ad-editor/motion/moves/CREDITS.md`).
- **الأمثلة:** نماذج تطبيقية لمنصة بسيط، ونسب كل عمل أصلي لصاحبه محفوظ (`video-ad-editor/references/examples.md`).

</div>
