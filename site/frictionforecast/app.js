// Friction Forecast page. Fetches Open-Meteo straight from the browser (one request for all
// areas), scores it with score.js and keeps the last answer in localStorage, so the page
// still works on the walk-in with no signal.
import { AREAS, inSeason } from './areas.js';
import { fetchForecast, PAST_DAYS } from './openmeteo.js';
import { buildForecast } from './score.js';

const CACHE_KEY = 'ff:v1';
const FRESH_MS = 60 * 60 * 1000;      // reuse a forecast for an hour before asking again
const STALE_MS = 12 * 60 * 60 * 1000; // flag anything older than 12 hours
const LABEL = { good: 'Good', okay: 'Okay', bad: 'Bad', wet: 'Wet' };

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function readCache() {
  try {
    const c = JSON.parse(localStorage.getItem(CACHE_KEY));
    return c && Array.isArray(c.raw) && c.raw.length === AREAS.length ? c : null;
  } catch { return null; }
}
function writeCache(c) {
  try { localStorage.setItem(CACHE_KEY, JSON.stringify(c)); } catch { /* private mode or full */ }
}

// Returns { raw, fetchedAt, offline } or null.
async function load(force = false) {
  const cached = readCache();
  if (!force && cached && Date.now() - cached.fetchedAt < FRESH_MS) return { ...cached, offline: false };
  try {
    const raw = await fetchForecast(AREAS);
    const fresh = { raw, fetchedAt: Date.now() };
    writeCache(fresh);
    return { ...fresh, offline: false };
  } catch (err) {
    console.warn('Forecast fetch failed', err);
    return cached ? { ...cached, offline: true } : null;
  }
}

function ago(ms) {
  const m = Math.round(ms / 60000);
  if (m < 1) return 'just now';
  if (m < 60) return `${m} min ago`;
  const h = Math.round(m / 60);
  return h < 48 ? `${h} h ago` : `${Math.round(h / 24)} days ago`;
}

function weekday(date, i) {
  if (i === 0) return 'Today';
  return new Date(`${date}T12:00:00Z`).toLocaleDateString('en-GB', { weekday: 'short', timeZone: 'UTC' });
}
function longDay(date, i) {
  const d = new Date(`${date}T12:00:00Z`).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'short', timeZone: 'UTC' });
  return i === 0 ? `Today, ${d}` : d;
}
function localTime(tz) {
  try { return new Date().toLocaleTimeString('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit' }); } catch { return ''; }
}
const hasWindow = (day) => day.rating !== 'wet' && day.score > 0;

function pill(area, day, i) {
  return `<button type="button" class="pill ${day.rating}${i >= 4 ? ' later' : ''}" data-area="${area.id}" data-i="${i}" aria-pressed="false"
    aria-label="${esc(longDay(day.date, i))}: ${LABEL[day.rating]}, score ${day.score}">
    <span>${weekday(day.date, i)}</span><strong>${LABEL[day.rating]}</strong><span class="n">${day.score}</span></button>`;
}

function bestDay(area) {
  let best = null;
  area.days.forEach((d, i) => { if (hasWindow(d) && (!best || d.score > best.d.score)) best = { d, i }; });
  return best;
}

function card(area) {
  const season = inSeason(area);
  const best = bestDay(area);
  const bestLine = best && best.d.score >= 45
    ? `Best this week: <strong>${esc(longDay(best.d.date, best.i))}</strong>, ${best.d.window} (${LABEL[best.d.rating].toLowerCase()}, ${best.d.score})`
    : area.days.every((d) => d.rating === 'wet') ? 'Wet all week. Sandstone is weaker when wet.' : 'No good window this week.';
  return `<section class="card" id="${area.id}" aria-labelledby="${area.id}-h">
    <div class="card-head">
      <div><h2 id="${area.id}-h">${esc(area.name)}</h2>
      <p class="meta">${esc(area.place)} · ${esc(area.rock)} · local time ${localTime(area.tz)}</p></div>
      <span class="badge${season ? ' on' : ''}" title="Usually climbed ${esc(area.seasonText)}">${season ? 'In season' : 'Off season'}</span>
    </div>
    <p class="best">${bestLine}</p>
    <div class="strip" role="group" aria-label="${esc(area.name)}, next 7 days">${area.days.map((d, i) => pill(area, d, i)).join('')}</div>
    <div class="detail" aria-live="polite"></div>
  </section>`;
}

function detail(area, i) {
  const day = area.days[i];
  const hrs = day.hours;
  const winStart = hasWindow(day) ? Number(day.window.slice(0, 2)) : -1;
  const inWin = (h) => h.hour >= winStart && h.hour < winStart + 3;
  const cls = (h) => (h.wet && area.rock === 'sandstone' ? 'wet' : h.score >= 70 ? 'good' : h.score >= 45 ? 'okay' : 'bad');
  let head;
  let why;
  if (day.rating === 'wet') {
    head = `${longDay(day.date, i)}: wet`;
    why = 'Sandstone is weaker when wet. Give it time to dry: rain soaks in and the rock stays fragile for about a day after the surface looks dry.';
  } else if (!hasWindow(day)) {
    head = `${longDay(day.date, i)}: no window`;
    why = hrs.some((h) => h.rain) ? 'Rain through the scored hours.' : 'Nothing scores above zero.';
  } else {
    head = `${longDay(day.date, i)}: ${LABEL[day.rating].toLowerCase()}, best window ${day.window} (score ${day.score})`;
    const w = hrs.filter(inWin);
    const avg = (k) => Math.round(w.reduce((s, h) => s + h[k], 0) / w.length);
    why = `In the window: about ${avg('temp')} °C air (rock ${avg('rockTemp')} °C in the sun), ${avg('humidity')} % humidity, wind ${avg('wind')} km/h.`;
    if (area.rock === 'sandstone' && hrs.some((h) => h.wet)) why += ' Some hours count as wet; the window skips them.';
    else if (hrs.some((h) => h.wet)) why += ' The rock may be damp in some hours, which cuts their score.';
  }
  const row = (label, f, extra = () => '') =>
    `<span class="lab">${label}</span>${hrs.map((h) => `<span class="v ${extra(h)}">${f(h)}</span>`).join('')}`;
  const gusty = hrs.some((h) => h.gusts >= 50);
  return `<h3>${esc(head)}</h3><p class="why">${esc(why)}</p>
    <div class="hours" style="--cols:${hrs.length}" role="img" aria-label="Hourly scores from ${hrs[0].hour}:00 to ${hrs[hrs.length - 1].hour + 1}:00">
      <span class="lab">score</span>${hrs.map((h) => `<span class="bar${inWin(h) ? ' win' : ''}" title="${h.hour}:00 score ${h.score}"><i class="${cls(h)}" style="height:${Math.max(h.score, 2)}%"></i></span>`).join('')}
      ${row('', (h) => String(h.hour).padStart(2, '0'), () => 'h')}
      ${row('°C', (h) => h.temp)}
      ${row('RH %', (h) => h.humidity)}
      ${row('km/h', (h) => h.wind)}
      ${row('rain', (h) => (h.rain ? (h.precip >= 0.1 ? h.precip.toFixed(1) : '•') : ''), (h) => (h.rain ? 'rain' : ''))}
    </div>
    ${gusty ? '<p class="note">Gusts of 50 km/h or more in some hours: weigh down your pads.</p>' : ''}
    ${area.note ? `<p class="note">${esc(area.note)}</p>` : ''}`;
}

function select(section, area, i) {
  section.querySelectorAll('.pill').forEach((b) => b.setAttribute('aria-pressed', String(Number(b.dataset.i) === i)));
  section.querySelector('.detail').innerHTML = detail(area, i);
}

function render(forecast, info) {
  const age = Date.now() - info.fetchedAt;
  const parts = [`Updated ${ago(age)}`];
  if (info.offline) parts.push('<span class="warn">Offline: showing the last forecast</span>');
  if (age > STALE_MS) parts.push('<span class="warn">This forecast is out of date</span>');
  parts.push('<button type="button" id="refresh">Refresh</button>');
  $('#status').innerHTML = parts.join(' · ');
  $('#refresh').addEventListener('click', () => start(true));

  const root = $('#areas');
  root.innerHTML = forecast.areas.map(card).join('');
  forecast.areas.forEach((area) => {
    const section = root.querySelector(`#${area.id}`);
    section.querySelector('.strip').addEventListener('click', (e) => {
      const b = e.target.closest('.pill');
      if (b) select(section, area, Number(b.dataset.i));
    });
    select(section, area, 0);
  });
}

async function start(force = false) {
  $('#status').textContent = force ? 'Refreshing…' : 'Loading the forecast…';
  const info = await load(force);
  if (!info) {
    $('#status').textContent = 'No forecast available.';
    $('#areas').innerHTML = '<p class="empty">Could not reach the weather service, and there is no saved forecast on this device yet. Try again with signal.</p>';
    return;
  }
  try {
    render(buildForecast(info.raw, AREAS, PAST_DAYS), info);
  } catch (err) {
    console.error(err);
    $('#status').textContent = 'The forecast could not be read.';
    try { localStorage.removeItem(CACHE_KEY); } catch { /* ignore */ }
  }
}

start();
