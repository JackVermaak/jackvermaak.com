// Open-Meteo requests. One request covers every area: comma-separated coordinates and
// timezones, answered with one object per area in the same order.
// Free API, non-commercial use, credit required (CC BY 4.0): https://open-meteo.com/en/terms

export const PAST_DAYS = 3; // history for the wetness model
export const FORECAST_DAYS = 7;

export const HOURLY = [
  'temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
  'wind_speed_10m', 'wind_gusts_10m', 'precipitation',
  'precipitation_probability', 'cloud_cover', 'shortwave_radiation', 'is_day',
];

// The archive has no rain probability; the scoring treats the missing value as 0.
export const ARCHIVE_HOURLY = [
  'temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
  'wind_speed_10m', 'wind_gusts_10m', 'precipitation', 'shortwave_radiation',
];

function locations(areas) {
  return {
    latitude: areas.map((a) => a.lat).join(','),
    longitude: areas.map((a) => a.lon).join(','),
    timezone: areas.map((a) => a.tz).join(','),
  };
}

export function forecastUrl(areas) {
  const q = new URLSearchParams({
    ...locations(areas),
    hourly: HOURLY.join(','),
    past_days: String(PAST_DAYS),
    forecast_days: String(FORECAST_DAYS),
  });
  return `https://api.open-meteo.com/v1/forecast?${q}`;
}

export function archiveUrl(areas, startDate, endDate) {
  const q = new URLSearchParams({
    ...locations(areas),
    hourly: ARCHIVE_HOURLY.join(','),
    start_date: startDate,
    end_date: endDate,
  });
  return `https://archive-api.open-meteo.com/v1/archive?${q}`;
}

async function getJson(url, fetchImpl = fetch) {
  const res = await fetchImpl(url);
  if (!res.ok) throw new Error(`Open-Meteo ${res.status}: ${await res.text()}`);
  const json = await res.json();
  return Array.isArray(json) ? json : [json]; // one object per area, same order
}

export const fetchForecast = (areas, fetchImpl) => getJson(forecastUrl(areas), fetchImpl);
export const fetchArchive = (areas, start, end, fetchImpl) => getJson(archiveUrl(areas, start, end), fetchImpl);
