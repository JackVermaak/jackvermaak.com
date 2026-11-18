(function () {
  var root = document.documentElement;

  // Theme toggle: flips between light and dark and remembers the choice in this browser.
  var toggle = document.querySelector('.theme-toggle');
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function label() { if (toggle) toggle.setAttribute('aria-label', isDark() ? 'Switch to light theme' : 'Switch to dark theme'); }
  if (toggle) {
    label();
    toggle.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      label();
    });
  }

  // Mobile menu
  var menu = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.site-nav');
  if (menu && nav) {
    menu.addEventListener('click', function () {
      var open = menu.getAttribute('aria-expanded') === 'true';
      menu.setAttribute('aria-expanded', String(!open));
      menu.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      nav.classList.toggle('open', !open);
    });
  }

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Copy buttons
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-copy'));
      if (!target) return;
      var text = target.textContent.trim(), original = btn.textContent;
      function done() { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = original; }, 1600); }
      function fallback() {
        var r = document.createRange(); r.selectNodeContents(target);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        btn.textContent = 'Selected';
        setTimeout(function () { btn.textContent = original; }, 1600);
      }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
        else fallback();
      } catch (e) { fallback(); }
    });
  });

  // Project filters
  var chips = document.querySelectorAll('.chip[data-filter]');
  var rows = document.querySelectorAll('li[data-kind]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      rows.forEach(function (r) { r.hidden = !(f === 'all' || r.getAttribute('data-kind') === f); });
    });
  });

  // Forest fire snapshot: the project's rules (density 0.6, p = 0.5, 8 neighbours, wind 0.9,
  // ember jump 0.5, firebreak rows 30 to 34), wind blowing south, fixed seed.
  var canvases = document.querySelectorAll('canvas.fire-canvas');
  if (!canvases.length) return;
  var N = 50, EMPTY = 0, TREE = 1, FIRE = 2;
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function simulate() {
    var rand = rng(838), g = [], r, c;
    for (r = 0; r < N; r++) { g.push([]); for (c = 0; c < N; c++) g[r].push(rand() < 0.6 ? TREE : EMPTY); }
    for (r = 30; r < 35; r++) for (c = 0; c < N; c++) g[r][c] = EMPTY;
    for (r = 6; r < 8; r++) for (c = 22; c < 28; c++) g[r][c] = FIRE;
    for (var step = 0; step < 23; step++) {
      var next = g.map(function (row) { return row.slice(); });
      for (r = 0; r < N; r++) for (c = 0; c < N; c++) {
        if (g[r][c] === FIRE) { next[r][c] = EMPTY; continue; }
        if (g[r][c] !== TREE) continue;
        var near = false;
        for (var dr = -1; dr <= 1 && !near; dr++) for (var dc = -1; dc <= 1; dc++) {
          var rr = r + dr, cc = c + dc;
          if (rr >= 0 && rr < N && cc >= 0 && cc < N && g[rr][cc] === FIRE) { near = true; break; }
        }
        var upwind = r > 0 && g[r - 1][c] === FIRE;
        if (near && rand() < (upwind ? 0.9 : 0.5)) next[r][c] = FIRE;
        else if (r > 1 && g[r - 1][c] === EMPTY && g[r - 2][c] === FIRE && rand() < 0.5) next[r][c] = FIRE;
      }
      g = next;
    }
    return g;
  }
  var grid = simulate();
  function draw() {
    var cs = getComputedStyle(root);
    var col = [cs.getPropertyValue('--ground').trim(), cs.getPropertyValue('--tree').trim(), cs.getPropertyValue('--fire').trim()];
    canvases.forEach(function (canvas) {
      var ctx = canvas.getContext('2d'), s = canvas.width / N;
      for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) { ctx.fillStyle = col[grid[r][c]]; ctx.fillRect(c * s, r * s, s, s); }
    });
  }
  draw();
  try { window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw); } catch (e) {}
  try { new MutationObserver(draw).observe(root, { attributes: true, attributeFilter: ['data-theme'] }); } catch (e) {}
})();
