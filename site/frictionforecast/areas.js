// One point per area. Rock type, timezone and the hours worth scoring all change the result.
// season: months (1–12) when the area is usually climbed, for the "in season" badge.
// Areas are grouped by country; the page's country filter lists countries in this order.
// Coordinates for the areas added after the plan come from thetopo.com / 27crags crag pages.
export const AREAS = [
  // South Africa
  { id: 'rocklands', name: 'Rocklands', place: 'The Pass, Cederberg', country: 'South Africa',
    lat: -32.1497, lon: 19.0295, tz: 'Africa/Johannesburg', rock: 'sandstone', hours: [10, 17],
    season: [3, 4, 5, 6, 7, 8, 9, 10, 11], seasonText: 'autumn to spring',
    note: 'Scored 10:00–17:00, the CapeNature sign-in hours on The Pass.' },
  { id: 'topside', name: 'Topside', place: 'Kalk Bay mountains, Cape Town', country: 'South Africa',
    lat: -34.1073, lon: 18.4394, tz: 'Africa/Johannesburg', rock: 'sandstone', hours: [8, 19],
    season: [3, 4, 5, 9, 10, 11], seasonText: 'autumn and spring, between the winter rain and the summer heat',
    note: 'Table Mountain National Park land, spread over several sectors with long walk-ins. The point sits above Echo Valley.' },

  // Switzerland
  { id: 'magic-wood', name: 'Magic Wood', place: 'Ausserferrera, Graubünden', country: 'Switzerland',
    lat: 46.5632, lon: 9.4368, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 20],
    season: [6, 7, 8, 9], seasonText: 'summer',
    note: 'A forested ravine around 1,290 m, likely damper and cooler than the forecast grid.' },
  { id: 'cresciano', name: 'Cresciano', place: 'Riviera, Ticino', country: 'Switzerland',
    lat: 46.2896, lon: 9.0055, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 19],
    season: [10, 11, 12, 1, 2, 3, 4], seasonText: 'autumn to spring' },
  { id: 'chironico', name: 'Chironico', place: 'Leventina, Ticino', country: 'Switzerland',
    lat: 46.4266, lon: 8.8473, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 19],
    season: [10, 11, 12, 1, 2, 3, 4], seasonText: 'autumn to spring',
    note: 'Mostly in shady forest, so it stays damp longer than the forecast grid suggests.' },
  { id: 'brione', name: 'Brione', place: 'Val Verzasca, Ticino', country: 'Switzerland',
    lat: 46.2902, lon: 8.7936, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 19],
    season: [10, 11, 12, 1, 2, 3, 4], seasonText: 'autumn to spring' },
  { id: 'val-bavona', name: 'Val Bavona', place: 'Vallemaggia, Ticino', country: 'Switzerland',
    lat: 46.3949, lon: 8.5386, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 20],
    season: [3, 4, 5, 9, 10, 11], seasonText: 'spring and autumn' },
  { id: 'sustenpass', name: 'Sustenpass', place: 'Sustenbrüggli, Uri', country: 'Switzerland',
    lat: 46.7482, lon: 8.4652, tz: 'Europe/Zurich', rock: 'granite', hours: [8, 20],
    season: [7, 8, 9], seasonText: 'summer',
    note: 'High alpine granite. The pass road is closed in winter, usually until June.' },

  // Germany
  { id: 'avalonia', name: 'Avalonia', place: 'Herdecke, Ruhr', country: 'Germany',
    lat: 51.404, lon: 7.398, tz: 'Europe/Berlin', rock: 'sandstone', hours: [8, 20],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring',
    note: 'Sandstone with siltstone and claystone, so it gets the sandstone wet stop.' },
  { id: 'glees', name: 'Glees', place: 'Eifel', country: 'Germany',
    lat: 50.4433, lon: 7.2656, tz: 'Europe/Berlin', rock: 'basalt', hours: [9, 19],
    season: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], seasonText: 'year-round, best when cool',
    note: 'Scored 09:00–19:00: the hunting rule limits access to those hours.' },
  { id: 'goettinger-wald', name: 'Göttinger Wald', place: 'Wiesental, Thalwenden', country: 'Germany',
    lat: 51.364, lon: 9.995, tz: 'Europe/Berlin', rock: 'sandstone', hours: [8, 20],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring',
    note: 'Bouldering is only allowed in some zones; the point sits at the Wiesental boulders.' },

  // France
  { id: 'font', name: 'Fontainebleau', place: 'Bas Cuvier', country: 'France',
    lat: 48.446, lon: 2.638, tz: 'Europe/Paris', rock: 'sandstone', hours: [8, 19],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring' },

  // Austria
  { id: 'zillertal', name: 'Zillertal', place: 'near Mayrhofen, Tyrol', country: 'Austria',
    lat: 47.1626, lon: 11.8586, tz: 'Europe/Vienna', rock: 'gneiss', hours: [8, 20],
    season: [4, 5, 6, 9, 10], seasonText: 'spring and autumn' },

  // Italy
  { id: 'val-masino', name: 'Val Masino', place: 'San Martino, Lombardy', country: 'Italy',
    lat: 46.2337, lon: 9.6353, tz: 'Europe/Rome', rock: 'granite', hours: [8, 20],
    season: [4, 5, 6, 9, 10], seasonText: 'spring and autumn',
    note: 'The boulders around San Martino, at the foot of Val di Mello.' },

  // Spain
  { id: 'albarracin', name: 'Albarracín', place: 'Pinares de Rodeno, Teruel', country: 'Spain',
    lat: 40.3881, lon: -1.4081, tz: 'Europe/Madrid', rock: 'sandstone', hours: [8, 19],
    season: [10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring',
    note: 'A protected landscape: check the current access rules and any seasonal closures before you go.' },
];

export function inSeason(area, date = new Date()) {
  return area.season.includes(date.getMonth() + 1);
}

// URL-safe key for a country, used by the filter (?country=south-africa).
export const countryKey = (name) => name.toLowerCase().normalize('NFD').replace(/[^a-z]+/g, '-');

// Countries in the order they first appear above, with how many areas each has.
export const COUNTRIES = [...new Set(AREAS.map((a) => a.country))]
  .map((name) => ({ name, key: countryKey(name), count: AREAS.filter((a) => a.country === name).length }));
