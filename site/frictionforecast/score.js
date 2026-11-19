// Friction Forecast scoring. Pure functions, no DOM: the page, the tests and the backtest
// script all import this file, so they can never disagree about a score.
//
// Every number here is a starting guess to tune against real sessions, not a physical constant.

// Per rock type: drying rate, soak time after the surface dries, whether wet rock is a hard
// stop, and a profile that overrides the defaults below.
export const ROCK = {
  sandstone: { dryRate: 0.15, soakHours: 24, wetStops: true,
    profile: { rhGood: 35, rhBad: 80, weights: { temp: 0.3, humidity: 0.5, wind: 0.2 } } },
  gneiss: { dryRate: 0.20, soakHours: 6, wetStops: false, profile: {} },
  granite: { dryRate: 0.30, soakHours: 0, wetStops: false,
    profile: { rhGood: 45, rhBad: 90, weights: { temp: 0.45, humidity: 0.35, wind: 0.2 } } },
  basalt: { dryRate: 0.30, soakHours: 0, wetStops: false,
    profile: { rhGood: 45, rhBad: 90, weights: { temp: 0.45, humidity: 0.35, wind: 0.2 } } },
};

export const DEFAULT_PROFILE = {
  tempIdeal: [2, 12], tempLimits: [-6, 24], // °C, estimated rock temperature
  tempGate: [-16, 34],                      // °C: past the limits the whole score fades to 0 here
  rhGood: 40, rhBad: 85,                    // % relative humidity
  windIdeal: [8, 25], windMax: 50,          // km/h at 10 m
  sunWarming: 8,                            // °C added to the rock at 1,000 W/m² of sun
  weights: { temp: 0.4, humidity: 0.4, wind: 0.2 },
  thresholds: { good: 70, okay: 45 },
};

export const WINDOW_HOURS = 3;
export const WET_CAP_MM = 3;

// default <- rock type <- a visitor's own settings (a later extension). Each layer only
// overrides what it sets.
export function profileFor(rock, custom = {}) {
  const rp = rock.profile || {};
  return {
    ...DEFAULT_PROFILE, ...rp, ...custom,
    weights: { ...DEFAULT_PROFILE.weights, ...rp.weights, ...custom.weights },
    thresholds: { ...DEFAULT_PROFILE.thresholds, ...rp.thresholds, ...custom.thresholds },
  };
}

const clamp01 = (x) => Math.min(1, Math.max(0, x));
export const ramp = (x, a, b) => clamp01((x - a) / (b - a)); // 0 at a, 1 at b, straight line between
const pad = (n) => String(n).padStart(2, '0');
const num = (x) => (x == null || Number.isNaN(x) ? 0 : x); // Open-Meteo sends null for missing values

// 1 inside [lo, hi], falling in a straight line to 0 at min and max.
export function band(x, [lo, hi], [min, max]) {
  if (x < lo) return ramp(x, min, lo);
  if (x > hi) return 1 - ramp(x, hi, max);
  return 1;
}

// 0.6 when calm, 1 in the ideal range, sliding to a floor of 0.3 at windMax and above.
export function windScore(w, p) {
  const [lo, hi] = p.windIdeal;
  if (w < lo) return 0.6 + 0.4 * (w / lo);
  if (w <= hi) return 1;
  return 1 - 0.7 * ramp(w, hi, p.windMax);
}

export const rockTemp = (h, i, p) => num(h.temperature_2m[i]) + (p.sunWarming * num(h.shortwave_radiation[i])) / 1000;

// Hour-by-hour drying in mm, before the bucket.
export function dryingRate(h, i, rock) {
  return rock.dryRate
    * (1 + 0.04 * Math.max(num(h.temperature_2m[i]), 0))
    * (1 + num(h.wind_speed_10m[i]) / 20)
    * (1.2 - num(h.relative_humidity_2m[i]) / 100)
    * (1 + num(h.shortwave_radiation[i]) / 400);
}

// Wetness bucket: rain fills it up to 3 mm (the rest runs off), drying empties it.
// Returns one boolean per hour: true while there is water in the bucket, and for
// soakHours after it empties, for porous rock that stays weak inside.
export function wetness(h, rock) {
  let water = 0;
  let dryFor = Infinity;
  return h.time.map((_, i) => {
    water = Math.min(WET_CAP_MM, Math.max(0, water + num(h.precipitation[i]) - dryingRate(h, i, rock)));
    dryFor = water > 0 ? 0 : dryFor + 1;
    return water > 0 || dryFor <= rock.soakHours;
  });
}

export const isRaining = (h, i) =>
  num(h.precipitation[i]) >= 0.2 || num(h.precipitation_probability?.[i]) >= 70;

// 0–100 for one hour: weighted comfort (rock temperature, humidity, wind) times the gates
// for extreme rock temperature, condensation, wet rock and rain.
//
// The temperature gate is not in the original plan. Without it the comfort sum lets dry air
// carry a scorching day: 35 °C rock at 25 % humidity scored 70, "good". With it, the score
// fades to 0 between tempLimits and tempGate.
export function hourScore(h, i, wet, rock, p) {
  if (isRaining(h, i)) return 0;
  const T = num(h.temperature_2m[i]);
  const rT = rockTemp(h, i, p);
  const w = p.weights;
  const comfort =
      w.temp * band(rT, p.tempIdeal, p.tempLimits)
    + w.humidity * (1 - ramp(num(h.relative_humidity_2m[i]), p.rhGood, p.rhBad))
    + w.wind * windScore(num(h.wind_speed_10m[i]), p);
  const tempGate = band(rT, p.tempLimits, p.tempGate);
  const dew = ramp(T - num(h.dew_point_2m[i]), 1, 4);
  const wetGate = wet ? (rock.wetStops ? 0 : 0.4) : 1;
  return Math.round(100 * comfort * tempGate * dew * wetGate);
}

export function ratingFor(score, p) {
  return score >= p.thresholds.good ? 'good' : score >= p.thresholds.okay ? 'okay' : 'bad';
}

// Rates each local day by its best 3-hour window inside the area's scored hours.
export function rateDays(h, area, custom = {}) {
  const rock = ROCK[area.rock];
  if (!rock) throw new Error(`Unknown rock type: ${area.rock}`);
  const p = profileFor(rock, custom);
  const wet = wetness(h, rock);
  const days = new Map();
  h.time.forEach((t, i) => {
    const [date, clock] = t.split('T');
    const hour = Number(clock.slice(0, 2));
    if (hour < area.hours[0] || hour >= area.hours[1]) return;
    if (!days.has(date)) days.set(date, []);
    days.get(date).push({
      hour,
      wet: wet[i],
      rain: isRaining(h, i),
      score: hourScore(h, i, wet[i], rock, p),
      temp: Math.round(num(h.temperature_2m[i])),
      rockTemp: Math.round(rockTemp(h, i, p)),
      humidity: Math.round(num(h.relative_humidity_2m[i])),
      wind: Math.round(num(h.wind_speed_10m[i])),
      gusts: Math.round(num(h.wind_gusts_10m?.[i])),
      precip: num(h.precipitation[i]),
    });
  });
  return [...days].map(([date, hrs]) => {
    let best = { score: 0, start: hrs[0].hour };
    for (let i = 0; i + WINDOW_HOURS <= hrs.length; i++) {
      let sum = 0;
      for (let k = 0; k < WINDOW_HOURS; k++) sum += hrs[i + k].score;
      const avg = sum / WINDOW_HOURS;
      if (avg > best.score) best = { score: Math.round(avg), start: hrs[i].hour };
    }
    const rating = rock.wetStops && hrs.every((x) => x.wet) ? 'wet' : ratingFor(best.score, p);
    const window = `${pad(best.start)}:00–${pad(best.start + WINDOW_HOURS)}:00`;
    return { date, rating, score: best.score, window, hours: hrs };
  });
}

// The forecast the page renders: one entry per area, history days dropped.
export function buildForecast(raw, areas, pastDays = 0, custom = {}) {
  return {
    updatedAt: new Date().toISOString(),
    areas: areas.map((area, i) => ({
      ...area,
      days: rateDays(raw[i].hourly, area, custom).slice(pastDays),
    })),
  };
}
