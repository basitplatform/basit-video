/* ═══ معاينات بنك الحركات بهوية منصة بسيط — مشهد لكل حركة (4 ث) ═══
   يبنيه tools/previews/make.py: مشروع موشن بـ100 مشهد، كل مشهد ينادي FX.<id> بنفس دالته بالبلقن.
   العالم المرسوم: جدار فاتح + شخص مرسوم (سلويت) يتحرك شوية + ألواح كحلي بشعار بسيط. كل النصوص محتوى منصة بسيط بالعراقي. */
(function () {
  const W = 1080, H = 1920, DUR = 4;
  const C = { wall: '#125B8D', line: 'rgba(255,255,255,0.06)', person: '#0C344F', navy: '#15557F', sky: '#23A1D3', coral: '#FB5734', white: '#FFFFFF' };
  const sway = t => Math.sin(t * 1.3) * 7, bob = t => Math.sin(t * 2.1) * 3;
  let T = 0;                                   // الزمن الحالي (يتحدّث كل فريم)
  let CTX = null;

  /* ── العالم ── */
  function wall(Y) {
    Y.fillStyle = C.wall; Y.fillRect(0, 0, W, H);
    Y.fillStyle = C.line; for (let x = 120; x < W; x += 240) Y.fillRect(x, 0, 3, H);
    Y.fillStyle = 'rgba(35,161,211,0.40)'; Y.beginPath(); Y.arc(860, 470, 125, 0, 6.2832); Y.fill();
    Y.fillStyle = 'rgba(255,255,255,0.07)'; Y.fillRect(0, 1240, W, 10);
  }
  function personShape(Y, t, hand) {
    const dx = sway(t), dy = bob(t);
    Y.save(); Y.fillStyle = C.person;
    Y.beginPath(); Y.ellipse(540 + dx, 760 + dy, 148, 182, 0, 0, 6.2832); Y.fill();                 // الراس
    Y.fillRect(540 + dx - 62, 900 + dy, 124, 110);                                                     // الرقبة
    Y.beginPath(); Y.moveTo(130 + dx * 0.6, H); Y.bezierCurveTo(130 + dx * 0.6, 1130 + dy, 300 + dx, 1000 + dy, 540 + dx, 1000 + dy);
    Y.bezierCurveTo(780 + dx, 1000 + dy, 950 + dx * 0.6, 1130 + dy, 950 + dx * 0.6, H); Y.closePath(); Y.fill();  // الكتوف والجسم
    if (hand) { const p = hand; Y.lineWidth = 92; Y.lineCap = 'round'; Y.strokeStyle = C.person;
      Y.beginPath(); Y.moveTo(300 + dx, 1250); Y.quadraticCurveTo(220, 1450, p.x, p.y + 60); Y.stroke();
      Y.beginPath(); Y.arc(p.x, p.y, 70, 0, 6.2832); Y.fill(); }
    Y.restore();
  }
  const palmPath = t => { const lt = t - Math.floor(t / DUR) * DUR; const up = lt > 0.6 && lt < 3.3; return { x: 300 + Math.sin(lt * 1.4) * 40, y: 1380 - (up ? 120 : 0), c: up ? 1 : 0 }; };
  const video = (Y, R) => { if (R) { Y.save(); Y.beginPath(); Y.rect(R.x, R.y, R.w, R.h); Y.clip(); }
    wall(Y); personShape(Y, T, CUR.hand ? palmPath(T) : null); if (R) Y.restore(); };
  const videoAt = (Y, t) => { const k = T; T = t; video(Y); T = k; return true; };
  const person = (Y) => { personShape(Y, T, CUR.hand ? palmPath(T) : null); return true; };
  person.ok = () => true;
  const personAt = (Y, t) => { personShape(Y, t, null); return true; };
  const face = t => ({ x: 540 + sway(t) - 148, y: 578 + bob(t), w: 296, h: 364, mx: 540 + sway(t), my: 860 + bob(t) });

  /* ── ألواح بسيط ── */
  const txt = (Y, s, x, y, o) => CTX.text(Y, s, x, y, Object.assign({ family: 'display', weight: 800, size: 100, color: C.white, align: 'center' }, o || {}));
  function logo(Y, x, y, w) { const im = CTX.img('logo'); if (!im) return; const h = w * im.height / im.width; Y.drawImage(im, x - w / 2, y - h / 2, w, h); }
  function panelB(Y) {
    Y.fillStyle = C.navy; Y.fillRect(0, 0, W, H);
    Y.fillStyle = 'rgba(35,161,211,0.18)'; Y.beginPath(); Y.arc(900, 300, 260, 0, 6.2832); Y.fill();
    logo(Y, 540, 560, 360);
    txt(Y, 'منصة بسيط', 540, 960, { size: 140 });
    txt(Y, 'تعلّم لتصنع الفرق', 540, 1090, { family: 'body', weight: 500, size: 64, color: C.sky });
  }
  function panelC(Y) {
    Y.fillStyle = C.sky; Y.fillRect(0, 0, W, H);
    txt(Y, 'دورات وورش', 540, 900, { size: 130, color: C.navy });
    txt(Y, 'تطبيقية', 540, 1050, { size: 130, color: C.white });
  }
  function card(Y, title, sub) {
    Y.save(); Y.fillStyle = C.navy; Y.beginPath(); Y.roundRect(160, 1360, 760, 230, 44); Y.fill(); Y.restore();
    txt(Y, title, 540, 1460, { size: 78 }); if (sub) txt(Y, sub, 540, 1545, { family: 'body', weight: 500, size: 44, color: C.sky });
  }

  /* ── إعدادات كل حركة (s = بداية المشهد) ── */
  const TR = s => ({ s: s + 1.4, A: video, B: panelB });
  const CUR = {};
  const D = {
    1: s => ({ line: 'l1', s: s + 0.3 }),
    2: s => ({ text: 'تعلّم بلا تعقيد', s: s + 0.3, accent: [1] }),
    3: s => ({ text: 'ابدي رحلتك هسه', s: s + 0.3, accent: [2] }),
    4: s => ({ lead: 'تعلّم', words: ['التصوير', 'المونتاج', 'التصميم', 'المحتوى'], s: s + 0.3 }),
    5: s => ({ text: 'المهارة تبدي بخطوة وحدة', s: s + 0.3, seq: [0, 2, 3] }),
    6: s => ({ text: 'منصة بسيط', s: s + 0.3 }),
    7: s => ({ value: '100', s: s + 0.3, label: 'درس تطبيقي' }),
    8: TR, 9: TR, 10: TR, 11: TR,
    12: s => ({ s: s + 0.6, focus: [540, 760], draw: video }),
    13: s => ({ s: s + 0.6, from: 1.25, focus: [540, 760], draw: video }),
    14: TR,
    15: s => ({ items: [['منصة بسيط', 'دورة جديدة نزلت'], ['ورشة المونتاج', 'تبدي باچر'], ['شهادتك جاهزة', 'مبروك!']], s: s + 0.3 }),
    16: s => ({ text: 'تعلّم واصنع الفرق', s: s + 0.3, mark: 2, under: 0 }),
    17: s => ({ s: s + 0.3, draw: Y => { video(Y); card(Y, 'منصة بسيط', 'تعلّم لتصنع الفرق'); } }),
    21: s => ({ text: 'سجّل بالدورة هسه', s: s + 0.3 }),
    22: s => ({ text: 'بسيط', s: s + 0.3 }),
    23: s => ({ s: s + 1.4, A: video, B: panelB, dot: [820, 1480] }),
    24: TR, 25: TR, 26: TR, 27: TR, 28: TR, 29: TR, 30: TR,
    31: s => ({ s: s, draw: video }),
    32: s => ({ s: s, dur: 4, from: [540, 860, 1.04], to: [540, 760, 1.22], draw: video }),
    33: s => ({ s: s + 0.8, focus: [540, 760], back: s + 2.8, draw: video }),
    34: s => ({ s: s + 1.2, draw: video }),
    35: s => ({ s: s + 1.2, back: video, front: Y => card(Y, 'منصة بسيط', 'تعلّم لتصنع الفرق'), to: 'front' }),
    36: s => ({ s: s + 0.3, layers: [{ draw: wall, depth: 0.2 }, { draw: person, depth: 0.6 }, { draw: Y => card(Y, 'دورات بسيط'), depth: 1 }] }),
    37: s => ({ s: s + 0.5, back: wall, front: person }),
    38: s => ({ line: 'l38', s: s + 0.3 }),
    39: s => ({ text: 'خلّي الفيديو يحچي عنك', s: s + 0.3, out: s + 2.9, accent: [1] }),
    40: s => ({ text: 'سجّل!', s: s + 0.5 }),
    41: s => ({ text: 'بسيط', s: s + 0.3 }),
    42: s => ({ a: 'لوحدك', b: 'ويّا مختصين', s: s + 0.3, win: 1, winAt: s + 2 }),
    43: s => ({ words: ['فكرة', 'تصوير', 'مونتاج', 'نشر'], s: s + 0.3 }),
    44: s => ({ name: 'اسم المدرب', title: 'مدرب المونتاج · منصة بسيط', s: s + 0.4, out: s + 3.4 }),
    45: s => ({ items: ['التصوير', 'المونتاج', 'التصميم', 'النشر'], s: s + 0.3 }),
    46: s => ({ old: 100, now: 60, s: s + 0.3, label: 'سعر الدورة' }),
    47: s => ({ text: 'سجّل هسه', s: s + 0.4, tap: s + 2.4 }),
    48: s => ({ s: s + 0.4, A: video, B: panelB }),
    49: s => ({ value: 85, s: s + 0.3, label: 'من الدورة خلصت' }),
    50: s => ({ data: [['تصوير', 40], ['مونتاج', 75], ['تصميم', 55], ['نشر', 90]], s: s + 0.3, hi: 3, suffix: '%' }),
    51: s => ({ s: s + 0.3, out: s + 3.5, person, video, words: ['تصوير', 'مونتاج', 'تصميم', 'ذكاء', 'نشر', 'محتوى'], hi: 1 }),
    52: s => ({ s: s + 0.3, out: s + 3.6, person, video, posts: [['دورة المونتاج', '12K'], ['ورشة التصميم', '9K'], ['أسرار التصوير', '48K'], ['أول ريل', '31K'], ['الذكاء الاصطناعي', '64K']], handle: '@basit_platform' }),
    53: s => ({ s: s + 0.3, out: s + 3.6, person, video }),
    54: s => ({ s: s + 0.3, out: s + 3.6, person, video, text: 'بسيط' }),
    55: s => ({ s: s + 0.3, out: s + 3.6, person, video, items: ['الذكاء الاصطناعي يغيّر المحتوى', 'المونتاج صار أسهل', 'دورات بسيط الجديدة', 'تعلّم من جوالك'] }),
    56: s => ({ s: s + 0.3, out: s + 3.6, person, video }),
    57: s => ({ s: s + 0.3, out: s + 3.6, person, video, title: 'بسيط', issue: 'منصة بسيط', big: 'تعلّم لتصنع الفرق', lines: [['3', 'دورات جديدة'], ['+', 'ورش تطبيقية']] }),
    58: s => ({ s: s + 0.3, out: s + 3.6, draw: video, text: 'تعلّم', sub: 'ويّا منصة بسيط' }),
    59: s => ({ s: s + 0.3, out: s + 3.6, video, title: 'بسيط', handle: '@basit_platform' }),
    60: s => ({ s: s + 0.3, out: s + 3.6, person, video, source: panelB }),
    61: s => ({ s: s + 0.3, out: s + 3.6, person, video, text: 'تعلّم' }),
    62: s => ({ text: 'تعلّم', s: s + 0.3, accent: [0] }),
    63: s => ({ text: 'بسيط', s: s + 0.3 }),
    64: s => ({ text: 'بسيط', s: s + 0.3, out: s + 2.8, video }),
    65: s => ({ s: s + 1.0, out: s + 3.4, person, personAt, video, videoAt }),
    66: s => ({ text: 'منصة', s: s + 0.3, at: s + 1.6 }),
    67: s => ({ text: 'بسيط', s: s + 0.3 }),
    68: s => ({ s: s + 0.3, hub: { label: 'بسيط', icon: 'spark' }, nodes: [{ label: 'تصوير', icon: 'doc' }, { label: 'مونتاج', icon: 'folder' }, { label: 'تصميم', icon: 'sheet' }, { label: 'نشر', icon: 'mail' }, { label: 'محتوى', icon: 'chat' }] }),
    69: TR,
    70: s => ({ s: s + 0.3, out: s + 3.6, person, video }),
    71: s => ({ s: s + 0.5, out: s + 3, video, title: 'الدرس الثاني', num: '2' }),
    72: s => ({ s: s + 0.4, out: s + 3, video, title: 'درس جديد نزل', sub: 'منصة بسيط', value: null, icon: 'check' }),
    73: s => ({ text: 'السر هو الاستمرار بالتعلّم', s: s + 0.3, hide: [2], at: [s + 2] }),
    74: s => ({ s: s + 0.3, text: 'أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ', surah: 'الرعد', ayah: 28 }),
    75: s => ({ s: s + 0.6, out: s + 3.6, person, personAt, video, videoAt }),
    76: TR,
    77: s => ({ s: s + 0.3, out: s + 3.8, cities: [{ name: 'البصرة', lon: 47.8, lat: 30.5, value: 320, side: 'b' }, { name: 'أربيل', lon: 44.0, lat: 36.2, value: 210, side: 't' }, { name: 'عمّان', lon: 35.9, lat: 31.9, value: 140, side: 'l' }, { name: 'دبي', lon: 55.3, lat: 25.2, value: 180, side: 'r' }], total: { value: 4, label: 'مدن' } }),
    78: s => ({ s: s + 0.3, out: s + 3.6, person, video }),
    79: s => ({ s: s + 0.3, A: video, B: panelB }),
    80: s => ({ from: 'صعب', to: 'بسيط', s: s + 0.3, at: s + 1.8 }),
    81: s => ({ s: s + 0.3, cmd: 'claude "build a course page for Basit"', note: '# خلصت صفحة الدورة بدقيقة' }),
    82: TR,
    83: s => ({ s: s + 0.3 }),
    84: s => ({ s: s + 0.3, out: s + 3.6, video, person }),
    85: s => ({ s: s + 0.5, out: s + 3.6, text: 'كلت بخاطري: لازم أتعلّم', face, thought: true, accent: [3] }),
    86: s => ({ s: s + 0.8, out: s + 3.2, video, face }),
    87: s => ({ s: s + 1.2, A: video, B: panelB }),
    88: s => ({ s: s + 0.3, out: s + 3.7, text: 'تعلّمت المونتاج بأسبوع ويّا منصة بسيط', name: 'منصة بسيط', handle: '@basit_platform', avatar: (Y, R) => { Y.fillStyle = C.navy; Y.fillRect(R.x, R.y, R.w, R.h); logo(Y, R.x + R.w / 2, R.y + R.h / 2, R.w * 0.8); }, video }),
    89: s => ({ s: s + 0.3, out: s + 3.7, video, face }),
    90: s => ({ text: 'بسيط', s: s + 0.3, out: s + 3.2 }),
    91: s => ({ s: s + 0.5, out: s + 3.4, palm: palmPath, video, value: '100', label: 'درس' }),
    92: s => ({ s: s + 1.2, A: video, B: panelB, tiles: [{ big: '4', small: 'مجالات' }, { big: '×2', small: 'أسرع تعلّم' }] }),
    93: s => ({ s: s + 0.3, out: s + 3.7 }),
    94: s => ({ s: s + 0.3, out: s + 3.8, video }),
    95: s => ({ s: s + 0.8, video }),
    96: s => ({ text: 'تعلّم بلا حدود', s: s + 0.3, out: s + 3.5 }),
    97: s => ({ s: s + 1.4, A: video, B: panelB }),
    98: s => ({ s: s + 0.3, out: s + 3.8, draw: Y => { panelB(Y); Y.fillStyle = C.sky; Y.beginPath(); Y.roundRect(330, 1235, 420, 130, 65); Y.fill(); txt(Y, 'سجّل هسه', 540, 1325, { size: 62 }); }, from: [880, 1600], steps: [{ to: [540, 1300], dur: 0.9, click: true }] }),
    99: TR,
    100: s => ({ s: s + 0.8, dur: 0.8, video, videoAt, person, personAt }),
  };

  /* ── حركات القواعد (ماكو دالة رسم): 18 صوت يسبق · 19 قطع مطابق · 20 تبطيء الضربة ── */
  const RULES = {
    18(ctx, t, s) { const X = ctx.X; const cut = s + 2.0, lt = t - s;
      if (t < cut) video(X); else panelB(X);
      const k = Math.min(1, Math.max(0, (t - (cut - 0.7)) / 0.3));            // الصوت يبدي قبل القطع
      X.save(); X.globalAlpha = k; X.fillStyle = C.navy; X.beginPath(); X.roundRect(190, 1500, 700, 150, 40); X.fill();
      X.strokeStyle = C.sky; X.lineWidth = 10; X.lineCap = 'round';
      for (let i = 0; i < 18; i++) { const h = 20 + 45 * Math.abs(Math.sin(i * 1.7 + lt * 9)); X.beginPath(); X.moveTo(260 + i * 32, 1575 - h / 2); X.lineTo(260 + i * 32, 1575 + h / 2); X.stroke(); }
      X.restore(); txt(X, 'الصوت يسبق الصورة', 540, 1440, { size: 54, color: t < cut ? C.navy : C.white, alpha: k }); },
    19(ctx, t, s) { const X = ctx.X; const cut = s + 1.9;
      if (t < cut) { video(X); X.fillStyle = C.sky; X.beginPath(); X.arc(540, 760, 150 + 20 * Math.sin(t * 3), 0, 6.2832); X.globalAlpha = 0.35; X.fill(); X.globalAlpha = 1; }
      else { panelC(X); X.strokeStyle = C.white; X.lineWidth = 18; X.beginPath(); X.arc(540, 760, 170, 0, 6.2832); X.stroke(); } },
    20(ctx, t, s) { const X = ctx.X; const hit = s + 2.0; const tau = ctx.FX.ramp ? ctx.FX.ramp(t, { hit, low: 0.25 }) : t;
      panelB(X); const lt = Math.max(0, tau - s); const x = 120 + (lt * 260) % 840;
      X.fillStyle = C.coral; X.beginPath(); X.arc(x, 1450, 60, 0, 6.2832); X.fill();
      const f = Math.max(0, 1 - Math.abs(t - hit) * 3); if (f > 0) { X.fillStyle = 'rgba(255,255,255,' + (0.35 * f) + ')'; X.fillRect(0, 0, W, H); } },
  };

  const cat = window.__CATALOG || [];
  cat.forEach((m, i) => {
    const s = i * DUR;
    MOTION.scene({
      id: 'm' + m.n, start: s, end: s + DUR,
      draw(t, lt, ctx) {
        T = t; CTX = ctx; CUR.hand = m.n === 91;
        if (RULES[m.n]) return RULES[m.n](ctx, t, s);
        video(ctx.X);
        const fx = ctx.FX && ctx.FX[m.id];
        if (!fx) { txt(ctx.X, 'ماكو دالة: ' + m.id, 540, 960, { color: C.coral, size: 60 }); return; }
        const o = (D[m.n] || (s0 => ({ s: s0 + 0.3 })))(s);
        try { fx(ctx, t, o); } catch (e) { ctx.X.setTransform(1, 0, 0, 1, 0, 0); txt(ctx.X, '⚠ ' + m.n + ' ' + m.id, 540, 960, { color: C.coral, size: 50 }); txt(ctx.X, String(e.message).slice(0, 40), 540, 1040, { color: C.coral, size: 30, family: 'body' }); if (!window.__ERR) window.__ERR = {}; window.__ERR[m.n] = String(e.message); }
      },
    });
  });
})();
