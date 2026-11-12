/* ExpressFind.com — site script (no dependencies) */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) { localStorage.removeItem(k); return; } localStorage.setItem(k, v); } catch (e) { return null; } }
  function sstore(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  function money(n) { return (n < 0 ? '-' : '') + '$' + Math.round(Math.abs(n)).toLocaleString('en-US'); }
  function r5(n) { return n < 100 ? Math.round(n / 5) * 5 : n < 1000 ? Math.round(n / 10) * 10 : Math.round(n / 50) * 50; }
  function qp(name) { var m = new RegExp('[?&]' + name + '=([^&#]*)').exec(location.search); return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : ''; }
  var ROOT = (document.body && document.body.getAttribute('data-root')) || '';

  /* ---------- Private inbox routing (the address is never written in the page) ---------- */
  var _k = [64, 66, 78, 3, 65, 68, 76, 64, 74, 109, 28, 76, 94, 70, 95, 66, 90, 79, 72, 90];
  function inbox() { return String.fromCharCode.apply(null, _k.map(function (c) { return c ^ 45; })).split('').reverse().join(''); }
  function endpoint() { return 'https://formsubmit.co/ajax/' + inbox(); }

  $$('[data-mail]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var s = a.getAttribute('data-mail') || 'Inquiry from ExpressFind.com';
      window.location.href = 'mailto:' + inbox() + '?subject=' + encodeURIComponent(s);
    });
  });

  /* ---------- Theme ---------- */
  var html = document.documentElement;
  var tb = $('#themeBtn');
  if (tb) tb.addEventListener('click', function () {
    var cur = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', cur); store('ef-theme', cur);
  });

  /* ---------- Menu ---------- */
  var burger = $('#burger'), menu = $('#menu');
  if (burger && menu) burger.addEventListener('click', function () {
    var o = menu.classList.toggle('open'); burger.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  var here = location.pathname.replace(/index\.html$/, '');
  $$('#menu a').forEach(function (a) {
    var p = new URL(a.getAttribute('href'), location.href).pathname.replace(/index\.html$/, '');
    var sec = p.replace(/\.html$/, '/');
    if (p === here || (sec.length > 2 && here.indexOf(sec) === 0)) { a.classList.add('active'); a.setAttribute('aria-current', 'page'); }
  });

  /* ---------- Reveal ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { threshold: 0.1 });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else { $$('.reveal').forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- Cookie notice ---------- */
  var ck = $('#cookie');
  if (ck && !store('ef-cookie')) ck.classList.add('show');
  $$('[data-cookie]').forEach(function (b) { b.addEventListener('click', function () { store('ef-cookie', b.getAttribute('data-cookie')); ck.classList.remove('show'); }); });

  /* ---------- Small things ---------- */
  $$('.year').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  var sticky = $('#stickyCta');
  if (sticky) window.addEventListener('scroll', function () { sticky.classList.toggle('show', window.scrollY > 480); }, { passive: true });
  $$('[data-print]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });
  $$('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var d = { title: document.title, url: location.href };
      if (navigator.share) { navigator.share(d).catch(function () {}); return; }
      try { navigator.clipboard.writeText(location.href); b.textContent = 'Link copied ✓'; } catch (e) { window.prompt('Copy this link', location.href); }
    });
  });
  var mon = new Date().getMonth();
  $$('[data-month]').forEach(function (el) { if (+el.getAttribute('data-month') === mon) el.hidden = false; });

  /* ---------- Hero finder ---------- */
  $$('form.finder').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var s = f.service.value, z = (f.zip.value || '').trim();
      var url = (f.getAttribute('action') || ROOT + 'get-quotes.html') + '?service=' + encodeURIComponent(s) + (z ? '&zip=' + encodeURIComponent(z) : '') + (f.getAttribute('data-urgency') ? '&urgency=' + f.getAttribute('data-urgency') : '');
      location.href = url;
    });
  });

  /* ---------- YouTube facades ---------- */
  $$('.video[data-yt]').forEach(function (v) {
    var id = v.getAttribute('data-yt'), t = v.getAttribute('data-title') || 'Video';
    v.innerHTML = '<img loading="lazy" alt="' + t.replace(/"/g, '') + '" src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg"><div class="play"><span aria-hidden="true">▶</span></div>';
    v.setAttribute('role', 'button'); v.setAttribute('tabindex', '0'); v.setAttribute('aria-label', 'Play video: ' + t);
    function play() { v.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" title="' + t.replace(/"/g, '') + '" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>'; }
    v.addEventListener('click', play, { once: true });
    v.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
  });

  /* ---------- Generic AJAX forms ---------- */
  function utm() {
    var o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid'].forEach(function (k) {
      var v = qp(k) || sstore('ef-' + k); if (v) { o[k] = v; sstore('ef-' + k, v); }
    });
    if (!sstore('ef-ref') && document.referrer) sstore('ef-ref', document.referrer);
    if (sstore('ef-ref')) o.referrer = sstore('ef-ref');
    return o;
  }
  utm();
  function collect(f) {
    var d = {};
    new FormData(f).forEach(function (v, k) { if (k === '_honey') return; d[k] = d[k] ? d[k] + ', ' + v : v; });
    return d;
  }
  function send(data, subject) {
    var u = utm(); for (var k in u) data[k] = u[k];
    data._subject = subject; data._template = 'table'; data._captcha = 'false';
    data.page = location.href; data.submitted = new Date().toString();
    return fetch(endpoint(), { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json().catch(function () { return {}; }); });
  }
  $$('form.js-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f._honey && f._honey.value) return;
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var msg = $('.form-msg', f), btn = $('button[type=submit]', f), old = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      var data = collect(f);
      var subj = (f.getAttribute('data-subject') || 'ExpressFind form') + ' — ' + (data.name || data.business || data.email || '');
      send(data, subj).then(function () {
        if (f.getAttribute('data-redirect')) { sstore('ef-ty', f.getAttribute('data-type') || 'form'); location.href = f.getAttribute('data-redirect'); return; }
        if (msg) { msg.className = 'form-msg ok'; msg.textContent = f.getAttribute('data-ok') || 'Received — we will reply within one business day.'; }
        if (f.getAttribute('data-unlock')) { var u = $(f.getAttribute('data-unlock')); if (u) u.hidden = false; }
        f.reset();
      }).catch(function () {
        if (msg) { msg.className = 'form-msg err'; msg.innerHTML = 'Network error — please try again in a minute.'; }
      }).then(function () { if (btn) { btn.disabled = false; btn.innerHTML = old; } });
    });
  });

  /* ---------- Quote funnel ---------- */
  var qf = $('#quoteForm');
  if (qf) {
    var steps = $$('.step', qf), bars = $$('.progress span'), lab = $('#stepLabel'), cur = 0;
    var DRAFT = 'ef-quote-draft';
    var names = ['Service', 'Urgency', 'Location', 'Details', 'Contact'];
    function show(n) {
      cur = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, i) { s.classList.toggle('active', i === cur); });
      bars.forEach(function (b, i) { b.classList.toggle('on', i <= cur); });
      if (lab) lab.textContent = 'Step ' + (cur + 1) + ' of ' + steps.length + ' · ' + names[cur];
      var top = qf.getBoundingClientRect().top + window.scrollY - 110;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: 'smooth' });
      var first = $('input:not([type=hidden]),select,textarea', steps[cur]); if (first && cur > 0) try { first.focus({ preventScroll: true }); } catch (e) {}
    }
    function valid(i) {
      var s = steps[i], ok = true;
      $$('input,select,textarea', s).some(function (x) {
        if (x.type === 'radio') { var g = qf.querySelectorAll('input[name="' + x.name + '"]'); if (x.required && !Array.prototype.some.call(g, function (r) { return r.checked; })) { x.reportValidity(); ok = false; return true; } return false; }
        if (!x.checkValidity()) { x.reportValidity(); ok = false; return true; }
        return false;
      });
      if (ok && i === 2) {
        var z = qf.zip; var v = (z.value || '').trim();
        if (!/^\d{5}(-\d{4})?$/.test(v) && !/^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$/.test(v)) { z.setCustomValidity('Enter a 5-digit US ZIP or a Canadian postal code (A1A 1A1).'); z.reportValidity(); z.setCustomValidity(''); ok = false; }
      }
      return ok;
    }
    $$('[data-next]', qf).forEach(function (b) { b.addEventListener('click', function () { if (valid(cur)) { save(); show(cur + 1); } }); });
    $$('[data-prev]', qf).forEach(function (b) { b.addEventListener('click', function () { show(cur - 1); }); });
    $$('.svc input', qf).forEach(function (r) { r.addEventListener('change', function () { save(); setTimeout(function () { if (cur === 0) show(1); }, 180); }); });
    function save() { var d = collect(qf); delete d.consent; store(DRAFT, JSON.stringify(d)); }
    function fill(d) {
      Object.keys(d).forEach(function (k) {
        var els = qf.querySelectorAll('[name="' + k + '"]');
        Array.prototype.forEach.call(els, function (el) {
          if (el.type === 'radio' || el.type === 'checkbox') { if (String(d[k]).split(', ').indexOf(el.value) > -1) el.checked = true; }
          else el.value = d[k];
        });
      });
    }
    var draft = null; try { draft = JSON.parse(store(DRAFT) || 'null'); } catch (e) {}
    if (draft) fill(draft);
    var pre = { service: qp('service'), urgency: qp('urgency'), zip: qp('zip') };
    var map = { 'emergency': 'Emergency — right now', '24h': 'Within 24 hours', 'week': 'This week', 'planning': 'Planning / flexible' };
    if (pre.service) { var sr = qf.querySelector('input[name="service"][value="' + pre.service.replace(/"/g, '') + '"]'); if (sr) sr.checked = true; }
    if (pre.urgency && map[pre.urgency]) { var ur = qf.querySelector('input[name="urgency"][value="' + map[pre.urgency] + '"]'); if (ur) ur.checked = true; }
    if (pre.zip) qf.zip.value = pre.zip;
    if (pre.service && pre.zip) show(1); else if (pre.service) show(1); else show(0);
    qf.addEventListener('change', save);

    function score(d) {
      var s = 0, u = d.urgency || '';
      s += /Emergency/.test(u) ? 40 : /24/.test(u) ? 30 : /week/.test(u) ? 20 : 8;
      s += /own/i.test(d.ownership || '') ? 20 : /manage/i.test(d.ownership || '') ? 16 : 8;
      var b = d.budget || ''; s += /^\$5,000\+/.test(b) ? 20 : /^\$1,000/.test(b) ? 15 : /^\$500/.test(b) ? 10 : /Under/.test(b) ? 6 : 4;
      if ((d.details || '').length > 40) s += 10;
      if ((d.phone || '').replace(/\D/g, '').length >= 10) s += 10;
      return Math.min(100, s);
    }
    qf.addEventListener('submit', function (e) {
      e.preventDefault();
      if (qf._honey && qf._honey.value) return;
      if (!valid(cur)) return;
      var btn = $('button[type=submit]', qf), msg = $('.form-msg', qf), old = btn.innerHTML;
      btn.disabled = true; btn.textContent = 'Sending your request…';
      var d = collect(qf), sc = score(d), tag = sc >= 75 ? 'HOT' : sc >= 50 ? 'WARM' : 'COOL';
      var ref = 'EF-' + Date.now().toString(36).toUpperCase().slice(-6);
      d.lead_score = sc + ' (' + tag + ')'; d.reference = ref;
      send(d, '[' + tag + ' ' + sc + '] ' + (d.service || 'Quote') + ' — ' + (d.zip || '') + ' — ' + (d.urgency || ''))
        .then(function () {
          store(DRAFT, null); sstore('ef-ty', 'quote'); sstore('ef-ref-no', ref); sstore('ef-svc', d.service || ''); sstore('ef-urg', d.urgency || '');
          location.href = ROOT + 'thank-you.html';
        })
        .catch(function () { msg.className = 'form-msg err'; msg.textContent = 'Network error — please try again. If this is dangerous, call 911 now.'; btn.disabled = false; btn.innerHTML = old; });
    });
  }

  /* ---------- Thank-you page ---------- */
  var ty = $('#tyBox');
  if (ty) {
    var t = sstore('ef-ty') || 'form';
    $$('[data-ty]').forEach(function (el) { el.hidden = el.getAttribute('data-ty') !== t; });
    var rn = $('#refNo'); if (rn && sstore('ef-ref-no')) rn.textContent = sstore('ef-ref-no');
    var em = $('#tyEmergency'); if (em && /Emergency/.test(sstore('ef-urg') || '')) em.hidden = false;
  }

  /* ---------- Emergency triage ---------- */
  var tri = $('#triage');
  if (tri) {
    $$('.tile[data-key]', tri).forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-key');
        $$('.tile', tri).forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        $$('[data-panel]', tri).forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== k; });
        var p = $('[data-panel="' + k + '"]', tri); if (p) p.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    });
  }

  /* ---------- Mold clock ---------- */
  var mc = $('#moldClock');
  if (mc) {
    var inp = $('input', mc), out = $('.mc-out', mc), KEY = 'ef-moldclock';
    if (store(KEY)) inp.value = store(KEY);
    function tick() {
      if (!inp.value) { out.innerHTML = '<p>Enter when the water started to see your drying window.</p>'; return; }
      var start = new Date(inp.value), h = (Date.now() - start) / 36e5;
      if (isNaN(h)) return;
      var to24 = 24 - h, to48 = 48 - h;
      var line = h < 0 ? 'That time is in the future — check the date.' : to24 > 0 ? '<b>' + to24.toFixed(1) + ' h</b> left in the 24-hour window. Start drying now.' : to48 > 0 ? '24 hours passed. <b>' + to48.toFixed(1) + ' h</b> left before the 48-hour mark — call a restoration pro today.' : 'More than 48 hours have passed. Assume mold risk; get a professional moisture inspection.';
      out.innerHTML = '<small>Time since water started</small><div class="big">' + Math.max(0, h).toFixed(1) + ' hours</div><p>' + line + '</p><div class="meter"><i style="width:' + Math.min(100, Math.max(0, h / 48 * 100)) + '%"></i></div>';
    }
    inp.addEventListener('input', function () { store(KEY, inp.value); tick(); });
    var nb = $('[data-now]', mc); if (nb) nb.addEventListener('click', function () { var d = new Date(Date.now() - new Date().getTimezoneOffset() * 6e4); inp.value = d.toISOString().slice(0, 16); store(KEY, inp.value); tick(); });
    tick(); setInterval(tick, 60000);
  }

  /* ---------- Estimator data ---------- */
  var EST = null; var ed = $('#estData'); if (ed) { try { EST = JSON.parse(ed.textContent); } catch (e) {} }

  /* ---------- Cost estimator ---------- */
  var es = $('#estimator');
  if (es && EST) {
    var svcSel = $('#e-service', es);
    if (qp('service') && EST.services[qp('service')]) svcSel.value = qp('service');
    function calc() {
      var s = EST.services[svcSel.value]; if (!s) return;
      var sev = ($('input[name="e-sev"]:checked', es) || {}).value || 'moderate';
      var tm = +$('#e-time', es).value, rg = +$('#e-region', es).value;
      var base = s.sev[sev];
      var lo = r5(base[0] * tm * rg * EST.factor), hi = r5(base[1] * tm * rg * EST.factor);
      $('#e-range', es).textContent = money(lo) + ' – ' + money(hi);
      $('#e-mid', es).textContent = money(r5((lo + hi) / 2));
      $('#e-desc', es).textContent = s.sevText[sev];
      $('#e-prem', es).textContent = tm > 1 ? '+' + Math.round((tm - 1) * 100) + '% timing premium' : 'Standard hours';
      $('#e-reg', es).textContent = rg === 1 ? 'National average' : (rg > 1 ? '+' : '') + Math.round((rg - 1) * 100) + '% regional adjustment';
      $('#e-bar', es).style.width = Math.min(100, hi / s.cap * 100) + '%';
      var g = $('#e-guide', es); g.href = ROOT + 'costs/' + s.guide + '.html'; g.textContent = 'Read the full ' + s.name.toLowerCase() + ' cost guide →';
      var q = $('#e-quote', es); q.href = ROOT + 'get-quotes.html?service=' + encodeURIComponent(s.quote) + (tm >= 1.5 ? '&urgency=emergency' : '');
    }
    $$('input,select', es).forEach(function (x) { x.addEventListener('input', calc); x.addEventListener('change', calc); });
    calc();
  }

  /* ---------- Inline mini estimators on guides ---------- */
  $$('.mini-est').forEach(function (m) {
    if (!EST) return;
    var s = EST.services[m.getAttribute('data-svc')]; if (!s) return;
    function c() {
      var sev = $('select[name=sev]', m).value, tm = +$('select[name=tm]', m).value;
      var b = s.sev[sev];
      $('.mini-out', m).textContent = money(r5(b[0] * tm * EST.factor)) + ' – ' + money(r5(b[1] * tm * EST.factor));
    }
    $$('select', m).forEach(function (x) { x.addEventListener('change', c); }); c();
  });

  /* ---------- Quote checker ---------- */
  var qc = $('#quoteChecker');
  if (qc && EST) {
    $('#qc-run', qc).addEventListener('click', function () {
      var s = EST.services[$('#qc-service', qc).value];
      var lo = r5(s.typical[0] * EST.factor), hi = r5(s.typical[1] * EST.factor);
      var quotes = [1, 2, 3].map(function (i) { return { n: ($('#qc-n' + i, qc).value || 'Quote ' + i).trim(), v: parseFloat($('#qc-v' + i, qc).value) }; }).filter(function (q) { return q.v > 0; });
      var o = $('#qc-out', qc);
      if (!quotes.length) { o.innerHTML = '<p class="flag low">Enter at least one quote amount.</p>'; return; }
      var vals = quotes.map(function (q) { return q.v; }).sort(function (a, b) { return a - b; });
      var med = vals.length % 2 ? vals[(vals.length - 1) / 2] : (vals[vals.length / 2 - 1] + vals[vals.length / 2]) / 2;
      var h = '<div class="out"><small>Typical ' + s.name.toLowerCase() + ' range</small><div class="big">' + money(lo) + ' – ' + money(hi) + '</div><p>Median of your quotes: <b>' + money(med) + '</b>' + (vals.length > 1 ? ' · spread ' + money(vals[vals.length - 1] - vals[0]) : '') + '</p></div>';
      quotes.forEach(function (q) {
        var cls, t;
        if (q.v < lo * 0.8) { cls = 'low'; t = 'well below the typical range. Ask exactly what is excluded (parts, permits, disposal, warranty) and confirm license and insurance.'; }
        else if (q.v > hi * 1.25) { cls = 'high'; t = 'well above the typical range. Ask for an itemized breakdown and get at least one more quote.'; }
        else { cls = 'ok'; t = 'within or near the typical range. Compare warranty, start date and what is included.'; }
        if (vals.length > 1 && q.v > med * 1.5) t += ' It is also 50%+ above your median quote.';
        h += '<p class="flag ' + cls + '">' + q.n.replace(/</g, '') + ' (' + money(q.v) + '): ' + t + '</p>';
      });
      o.innerHTML = h;
    });
  }

  /* ---------- Repair or replace ---------- */
  var rr = $('#ror');
  if (rr) {
    var SYS = JSON.parse($('#rorData').textContent);
    var sel = $('#r-sys', rr);
    function preset() { var s = SYS[sel.value]; $('#r-new', rr).value = s.replace; $('#r-life', rr).textContent = s.life + ' years'; }
    sel.addEventListener('change', function () { preset(); run(); });
    function run() {
      var s = SYS[sel.value], age = +$('#r-age', rr).value || 0, rep = +$('#r-rep', rr).value || 0, nw = +$('#r-new', rr).value || 1;
      var p5000 = age * rep, pct = rep / nw * 100, lifePct = age / s.life * 100, votes = 0, why = [];
      if (p5000 > 5000) { votes++; why.push('Age × repair cost = ' + money(p5000) + ' (over the $5,000 rule of thumb).'); } else why.push('Age × repair cost = ' + money(p5000) + ' (under $5,000).');
      if (pct >= 50) { votes++; why.push('The repair is ' + pct.toFixed(0) + '% of replacement cost (50%+ favors replacing).'); } else why.push('The repair is ' + pct.toFixed(0) + '% of replacement cost.');
      if (lifePct >= 75) { votes++; why.push('At ' + age + ' years it has used ' + Math.min(100, lifePct).toFixed(0) + '% of a typical ' + s.life + '-year life.'); } else why.push('It has used about ' + lifePct.toFixed(0) + '% of a typical ' + s.life + '-year life.');
      var v = votes >= 2 ? 'Replace' : votes === 1 ? 'Get a second opinion' : 'Repair';
      $('#r-verdict', rr).textContent = v;
      $('#r-why', rr).innerHTML = why.map(function (w) { return '<li>' + w + '</li>'; }).join('');
      $('#r-bar', rr).style.width = Math.min(100, votes / 3 * 100) + '%';
    }
    $$('input', rr).forEach(function (x) { x.addEventListener('input', run); });
    preset(); run();
  }

  /* ---------- Filters (hubs, license list, videos) ---------- */
  $$('[data-filter]').forEach(function (inp) {
    var target = $(inp.getAttribute('data-filter'));
    inp.addEventListener('input', function () {
      var q = inp.value.toLowerCase().trim();
      $$('[data-item]', target).forEach(function (c) { c.hidden = q && c.textContent.toLowerCase().indexOf(q) === -1; });
    });
  });
  $$('.chips[data-chips]').forEach(function (bar) {
    var target = $(bar.getAttribute('data-chips'));
    $$('.chip', bar).forEach(function (c) {
      c.addEventListener('click', function () {
        $$('.chip', bar).forEach(function (x) { x.classList.toggle('on', x === c); x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        var cat = c.getAttribute('data-cat');
        $$('[data-cat]', target).forEach(function (it) { if (it.classList.contains('chip')) return; it.hidden = cat !== 'all' && (' ' + it.getAttribute('data-cat') + ' ').indexOf(' ' + cat + ' ') === -1; });
      });
    });
  });

  /* ---------- Checklists with saved progress ---------- */
  $$('[data-checklist]').forEach(function (list) {
    var KEY = 'ef-cl-' + list.getAttribute('data-checklist'), st = {};
    try { st = JSON.parse(store(KEY) || '{}'); } catch (e) {}
    var boxes = $$('input[type=checkbox]', list), pct = $('[data-pct="' + list.getAttribute('data-checklist') + '"]');
    function upd() {
      var d = boxes.filter(function (b) { return b.checked; }).length;
      boxes.forEach(function (b) { b.closest('li').classList.toggle('done', b.checked); });
      if (pct) { var p = Math.round(d / boxes.length * 100); pct.textContent = p + '% complete (' + d + '/' + boxes.length + ')'; var bar = $('[data-bar="' + list.getAttribute('data-checklist') + '"]'); if (bar) bar.style.width = p + '%'; }
    }
    boxes.forEach(function (b) { b.checked = !!st[b.id]; b.addEventListener('change', function () { st[b.id] = b.checked; store(KEY, JSON.stringify(st)); upd(); }); });
    upd();
  });
  $$('[data-reset]').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = b.getAttribute('data-reset'); if (!confirmReset()) return;
      store('ef-cl-' + k, null); $$('[data-checklist="' + k + '"] input[type=checkbox]').forEach(function (x) { x.checked = false; x.dispatchEvent(new Event('change')); });
    });
  });
  function confirmReset() { return true; }

  /* ---------- Saved fields (fridge card) ---------- */
  $$('[data-save]').forEach(function (el) {
    var k = 'ef-f-' + el.getAttribute('data-save');
    if (store(k)) el.value = store(k);
    el.addEventListener('input', function () { store(k, el.value); });
  });

  /* ---------- Maintenance calendar ---------- */
  var cal = $('#cal');
  if (cal) {
    var hemi = store('ef-hemi') || 'north';
    function mark() {
      var m = new Date().getMonth(); if (hemi === 'south') m = (m + 6) % 12;
      $$('.month', cal).forEach(function (el) { var on = +el.getAttribute('data-m') === m; el.classList.toggle('now', on); var b = $('.badge', el); if (b) b.hidden = !on; });
      $$('[data-hemi]').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-hemi') === hemi); });
    }
    $$('[data-hemi]').forEach(function (b) { b.addEventListener('click', function () { hemi = b.getAttribute('data-hemi'); store('ef-hemi', hemi); mark(); }); });
    mark();
    var ics = $('#icsBtn');
    if (ics) ics.addEventListener('click', function () {
      var now = $('.month.now', cal); if (!now) return;
      var tasks = $$('li label', now).map(function (l) { return l.textContent.trim(); });
      var d = new Date(), y = d.getFullYear(), mo = d.getMonth() + 1, pad = function (n) { return (n < 10 ? '0' : '') + n; };
      var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//ExpressFind//Maintenance//EN'];
      tasks.forEach(function (t, i) {
        var day = pad(Math.min(28, 1 + i * 3));
        lines.push('BEGIN:VEVENT', 'UID:ef-' + y + mo + i + '@expressfind.com', 'DTSTAMP:' + y + pad(mo) + '01T000000Z', 'DTSTART;VALUE=DATE:' + y + pad(mo) + day, 'SUMMARY:' + t.replace(/[,;]/g, ' '), 'DESCRIPTION:Home maintenance reminder from ExpressFind.com', 'END:VEVENT');
      });
      lines.push('END:VCALENDAR');
      var blob = new Blob([lines.join('\r\n')], { type: 'text/calendar' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'expressfind-maintenance-' + y + '-' + pad(mo) + '.ics'; document.body.appendChild(a); a.click(); a.remove();
    });
  }

  /* ---------- Contest countdown ---------- */
  var cd = $('#contestCountdown');
  if (cd) {
    var nowD = new Date(), end = new Date(nowD.getFullYear(), nowD.getMonth() + 1, 0, 23, 59, 59);
    var ml = $('#contestMonth'); if (ml) ml.textContent = nowD.toLocaleString('en-US', { month: 'long', year: 'numeric' });
    var dl = $('#contestDeadline'); if (dl) dl.textContent = end.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) + ', 11:59 p.m. (your local time)';
    (function t() {
      var ms = Math.max(0, end - new Date()), d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4), s = Math.floor(ms % 6e4 / 1e3);
      cd.textContent = d + 'd ' + (h < 10 ? '0' : '') + h + 'h ' + (m < 10 ? '0' : '') + m + 'm ' + (s < 10 ? '0' : '') + s + 's';
      setTimeout(t, 1000);
    })();
  }

  /* ---------- Pro ROI calculator ---------- */
  var roi = $('#roi');
  if (roi) {
    function rc() {
      var job = +$('#roi-job', roi).value || 0, close = (+$('#roi-close', roi).value || 0) / 100, leads = +$('#roi-leads', roi).value || 0, cpl = +$('#roi-cpl', roi).value || 0, margin = (+$('#roi-margin', roi).value || 0) / 100;
      var jobs = leads * close, rev = jobs * job, cost = leads * cpl, profit = rev * margin - cost;
      $('#roi-jobs', roi).textContent = jobs.toFixed(1);
      $('#roi-rev', roi).textContent = money(rev);
      $('#roi-cost', roi).textContent = money(cost);
      $('#roi-profit', roi).textContent = money(profit);
      $('#roi-x', roi).textContent = cost > 0 ? (rev / cost).toFixed(1) + '× revenue per $1 of leads' : '—';
      $('#roi-cpa', roi).textContent = jobs > 0 ? money(cost / jobs) : '—';
    }
    $$('input', roi).forEach(function (x) { x.addEventListener('input', rc); }); rc();
  }

  /* ---------- License search ---------- */
  /* handled by data-filter */

  /* ---------- Exit-intent lead magnet ---------- */
  var lm = $('#leadMagnet');
  function closeLm() { lm.classList.remove('show'); }
  if (lm) {
    $$('[data-close]', lm).forEach(function (b) { b.addEventListener('click', closeLm); });
    lm.addEventListener('click', function (e) { if (e.target === lm) closeLm(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLm(); });
    var skip = /get-quotes|thank-you/.test(location.pathname) || store('ef-lm-done');
    if (!skip && window.matchMedia && window.matchMedia('(pointer:fine)').matches) {
      document.addEventListener('mouseout', function h(e) {
        if (!e.relatedTarget && e.clientY <= 0 && !sstore('ef-lm')) { sstore('ef-lm', '1'); lm.classList.add('show'); document.removeEventListener('mouseout', h); }
      });
    }
    $$('[data-open-magnet]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); lm.classList.add('show'); }); });
    var lf = $('form', lm); if (lf) lf.addEventListener('submit', function () { store('ef-lm-done', '1'); });
  }
})();
