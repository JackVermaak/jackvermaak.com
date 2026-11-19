// One point per area. Rock type, timezone and the hours worth scoring all change the result.
// season: months (1–12) when the area is usually climbed, for the "in season" badge.
export const AREAS = [
  { id: 'rocklands', name: 'Rocklands', place: 'The Pass, South Africa',
    lat: -32.1497, lon: 19.0295, tz: 'Africa/Johannesburg', rock: 'sandstone', hours: [10, 17],
    season: [3, 4, 5, 6, 7, 8, 9, 10, 11], seasonText: 'autumn to spring',
    note: 'Scored 10:00–17:00, the CapeNature sign-in hours on The Pass.' },
  { id: 'magic-wood', name: 'Magic Wood', place: 'Ausserferrera, Switzerland',
    lat: 46.5632, lon: 9.4368, tz: 'Europe/Zurich', rock: 'gneiss', hours: [8, 20],
    season: [6, 7, 8, 9], seasonText: 'summer',
    note: 'A forested ravine around 1,290 m, likely damper and cooler than the forecast grid.' },
  { id: 'font', name: 'Fontainebleau', place: 'Bas Cuvier, France',
    lat: 48.446, lon: 2.638, tz: 'Europe/Paris', rock: 'sandstone', hours: [8, 19],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring' },
  { id: 'avalonia', name: 'Avalonia', place: 'Herdecke, Germany',
    lat: 51.404, lon: 7.398, tz: 'Europe/Berlin', rock: 'sandstone', hours: [8, 20],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring',
    note: 'Sandstone with siltstone and claystone, so it gets the sandstone wet stop.' },
  { id: 'glees', name: 'Glees', place: 'Eifel, Germany',
    lat: 50.4433, lon: 7.2656, tz: 'Europe/Berlin', rock: 'basalt', hours: [9, 19],
    season: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], seasonText: 'year-round, best when cool',
    note: 'Scored 09:00–19:00: the hunting rule limits access to those hours.' },
  { id: 'goettinger-wald', name: 'Göttinger Wald', place: 'Wiesental, Thalwenden, Germany',
    lat: 51.364, lon: 9.995, tz: 'Europe/Berlin', rock: 'sandstone', hours: [8, 20],
    season: [9, 10, 11, 12, 1, 2, 3, 4, 5], seasonText: 'autumn to spring',
    note: 'Bouldering is only allowed in some zones; the point sits at the Wiesental boulders.' },
];

export function inSeason(area, date = new Date()) {
  return area.season.includes(date.getMonth() + 1);
}
